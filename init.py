# This is the initial data gathering script from the first date with available data 
# to the freshest based on 'Received' status from API monitoring.

# As the data doesn't remain static after it is published, we should schedule an update of delta. 
# The question is how long it remains non-static - let's assume that data can be re-published only for the past month, 30 days until now.
# Also we will use the cron task for monitoring of new data published to website.
# Indeed we need to check if schema will change and there will be new borders (just to make scraper more flexible).

import psycopg2

from datetime import datetime, timedelta 

from pipeline import data_pipeline
from api import get_data_from_api, tz_converter

import os
from dotenv import load_dotenv


def init():
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
        date_available_from = tz_converter(
            datetime(2022, 6, 8, 0, 0, 0, 0), 
            from_tz='CET', 
            to_tz='UTC'
        )

        date_to = tz_converter(
            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=2), # borders data could be available 1 day ahead + 1 extra day to get the last hour of business day 
            from_tz='CET', 
            to_tz='UTC'
        )

        # Saving response's data into Python object
        data = get_data_from_api(
            url = 'https://publicationtool.jao.eu/core/api/data/',
            endpoint = 'maxExchanges',
            from_utc = date_available_from,
            to_utc=date_to,
            headers = {'X-REQUESTED-WITH': 'XMLHttpRequest'}
        )

        # Uploading data to TimescaleDB
        data_pipeline(
            connection=conn, 
            data=data, 
            schema_name=schema,
            table_name='maxbex',
            param='full-refresh',
        )
    
    except Exception as e:
        print(f'An exception occured while initiating data scraping process: {e}') 

if __name__=='__main__':
    init()
