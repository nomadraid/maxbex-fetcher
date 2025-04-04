# Data pipeline service

import psycopg2, psycopg2.extras

from datetime import datetime
from typing import Iterator, Dict, Any


def get_headers(data):
    try:
        headers = list(data[0].keys())
        id_time_columns = ', '.join([headers[0] + ' INT NOT NULL', headers[1] + ' TIMESTAMPTZ NOT NULL,'])
        borders_columns = ' INT NULL, '.join([border for border in headers[2:]]) + ' INT NULL,'
        pk_columns = ', '.join(headers[0:2])
        
        return headers, id_time_columns, borders_columns, pk_columns

    except Exception as e:
        print(f'An error occured while getting headers from API response: {e}')

# Defining a query execution for creating table at the initial step
def create_staging_table(
    cursor, 
    data: Iterator[Dict[str, Any]],
    schema_name: str,
    table_name: str,
    ) -> None:

    try:

        headers = get_headers(data)
        id_time_columns = headers[1]
        borders_columns = headers[2]
        pk_columns = headers[3]

        cursor.execute(f"""
        DO $$
        BEGIN

            IF NOT (
                SELECT EXISTS (
                    SELECT * FROM pg_tables 
                    WHERE schemaname='{schema_name}' 
                    AND tablename='{table_name}'
                )
            ) THEN

                CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
                    {id_time_columns}
                    {borders_columns}

                    dataflow_dttm TIMESTAMPTZ DEFAULT NOW(),

                    CONSTRAINT {table_name}_pk PRIMARY KEY({pk_columns})
                );

                PERFORM create_hypertable(
                    '{schema_name}.{table_name}', 
                    'datetimeutc',
                    chunk_time_interval => INTERVAL '1 day'
                );

            END IF;

        END;
        $$
        """)

    except Exception as e:
        print(f'An error occured while creating {schema_name}.{table_name} table: {e}')
        raise Exception("create_staging_table failed")

# Defining a query execution for truncating table 
# (not necessary, just in case if we want to re-run full-refresh)
def truncate_table(cursor, schema_name: str, table_name: str) -> None:
    try:
        cursor.execute(
            f"""
            TRUNCATE TABLE {schema_name}.{table_name};
            """
        )
    except Exception as e:
        print(f'An error occured while truncating {schema_name}.{table_name} table: {e}')
        raise Exception("truncate_table failed")

# Defining a query execution which drops the table 
# (not necessary, just in case if we want to re-build the model from scratch)
def drop_table(cursor, schema_name: str, table_name: str) -> None:
    try:
        cursor.execute(
            f"""
            DROP TABLE IF EXISTS {schema_name}.{table_name};
            """
        )
    except Exception as e:
        print(f'An error occured while deleting {schema_name}.{table_name} table: {e}')
        raise Exception("drop_table failed")

# Defining a query execution which drops the chunks with dates for last 30 days 
# (1 chunk = 1 day, it may not follow the best practices on how to choose the chunk size, but it can be suitable 
# for the large amounts of data per 1 day and also I found it convenient while working with delta)
def drop_chunks(cursor, schema_name: str, table_name: str) -> None:
    try:
        cursor.execute(
            f"""
            SELECT drop_chunks('{schema_name}.{table_name}', newer_than => INTERVAL '30 days');
            """
        )
    except Exception as e:
        print(f'An error occured while deleting chunks: {e}')
        raise Exception("drop_chunks failed")

# Defining a query execution with inserts of API response
# To reduce memory consumption we avoid storing data in-memory by using an iterator
def insert_execute_values_iterator(
    cursor, 
    data: Iterator[Dict[str, Any]],
    schema_name: str, 
    table_name: str,
    page_size: int = 1000 # choosed in case of current situation
    ) -> None:

    try:
        headers = get_headers(data)[0]

        psycopg2.extras.execute_values(
            cursor, 
            f"""
            INSERT INTO {schema_name}.{table_name} VALUES %s;
            """, 
            [
                tuple(
                    row[header] 
                    if header != 'dateTimeUtc' 
                    else datetime.strptime(row['dateTimeUtc'], '%Y-%m-%dT%H:%M:%SZ') # ! 
                    for header in headers
                )   
                for row in data
            ], 
            page_size=page_size
        )
    except Exception as e:
        print(f'An error occured while updating {schema_name}.{table_name} table: {e}')
        raise Exception("insert_execute_values_iterator failed")


# Here we build our workflow:
def data_pipeline(
    connection, 
    data: Iterator[Dict[str, Any]], 
    schema_name: str, 
    table_name: str, 
    param: str):

    try:
        assert data is not None, 'An error occured while processing data from API'

        with connection.cursor() as cursor:

            if param == 'full-refresh':
                create_staging_table(cursor, data, schema_name, table_name)
                truncate_table(cursor, schema_name, table_name)
                insert_execute_values_iterator(cursor, data, schema_name, table_name)
                print('Staging table with MaxBex data fully-refreshed')

            elif param == 'incremental':
                drop_chunks(cursor, schema_name, table_name)
                insert_execute_values_iterator(cursor, data, schema_name, table_name)
                print('Staging table with MaxBex data successfully updated')

            else:
                print('Provided parameter not supported by data pipeline')

    except Exception as e:
        print(f'An error occured in data pipeline: {e}')
