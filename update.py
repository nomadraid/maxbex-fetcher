# Incremental run for gathering delta data (for the past 30 days)
# Running job will be orchestrated by cron on hourly-basis

import psycopg2

from datetime import datetime, timedelta 

from pipeline import data_pipeline
from api import get_data_from_api, monitoring, tz_converter

import os
from dotenv import load_dotenv

def update():
    try:
        # Loading environment variables
        load_dotenv()
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        database = os.getenv("POSTGRES_DB")
        port = os.getenv("DATABASE_PORT")
        schema = os.getenv("POSTGRES_SCHEMA")

        # Configuring connection to timescale db
        conn = psycopg2.connect(f"postgres://{user}:{password}@timescaledb:{port}/{database}")
        conn.autocommit = True

        # Applying filters for API endpoint
        # We assumed that data is not static and we will update it for 1 month (adding 1 hour as from_utc is inclusive)
        date_from = tz_converter(
            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=29) + timedelta(hours=1),
            from_tz='CET', 
            to_tz='UTC'
        )
        # Borders data could be available 1 day ahead + 1 extra day to get to the last hour of business day 
        date_to = tz_converter(
            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=2),
            from_tz='CET', 
            to_tz='UTC'
        )
        # From that business date we will check if new data received
        date_monitor_from = tz_converter(
            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1),
            from_tz='CET', 
            to_tz='UTC'
        )

        # Monitoring of new data published
        status = monitoring(
            url = 'https://publicationtool.jao.eu/core/api/system/',
            endpoint = 'monitoring',
            from_utc = date_monitor_from,
            to_utc=date_to,
            to_monitor='Max Exchanges (MaxBex)',
            headers = {'X-REQUESTED-WITH': 'XMLHttpRequest'}
        )

        if status == 'Received':
            print("API returned status 'Received' after monitoring request, proceeding to the GET request")

            # Saving response's data into Python object
            data = get_data_from_api(
                url = 'https://publicationtool.jao.eu/core/api/data/',
                endpoint = 'maxExchanges',
                from_utc = date_from,
                to_utc=date_to,
                headers = {'X-REQUESTED-WITH': 'XMLHttpRequest'}
            )

            # Updating database with fresh data for the past 30 days
            data_pipeline(
                connection=conn, 
                data=data, 
                schema_name=schema,
                table_name='maxbex',
                param='incremental'
            )

        elif status == 'Expected':
            print("API returned status 'Expected' after monitoring request, proceeding to the next scheduled run")

        else:
            print("API returned unknown status after monitoring request, please check documentation")

    except Exception as e:
        print(f'An exception occured while updating process: {e}') 


if __name__=='__main__':
    update()