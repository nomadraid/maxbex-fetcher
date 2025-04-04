# API request service

import requests as rq

import json
from typing import Iterator, Dict, Any

from datetime import datetime
from pytz import timezone


# Defining a function which converts dates from web portal timezone (here it's CWE in our case)
# to timezone, which is using in API endpoints (UTC in our case)
def tz_converter(
    dttm: datetime,
    from_tz: str,
    to_tz: str
    ) -> datetime:

    # Use the 'pytz.all_timezones' list to see all available timezones
    dttm_converted = timezone(to_tz).normalize(timezone(from_tz).localize(dttm)).replace(tzinfo=None)

    return dttm_converted

# Configuring a GET request and response processing
def get_data_from_api(
    url: str,
    endpoint: str, 
    from_utc: str, 
    to_utc: str,
    headers: dict,
    #login: str,
    #password: str,
    #page: int = 1 -- API doesn't support pagination

    ) -> Iterator[Dict[str, Any]]:
    
    try:
        print(f'GET request: {url}{endpoint}?FromUtc=%s&&ToUtc=%s' % (from_utc, to_utc))

        response = rq.get(
            (f'{url}{endpoint}?FromUtc=%s&&ToUtc=%s' % (from_utc, to_utc)).encode('utf-8'), 
            headers=headers,
            stream=True, 
            #auth=(login, password)
        ).content
        
        data = json.loads(response)['data']

        assert data is not None, 'API response is None'
        assert 'id' in data[0], 'Response does not have "id"' 
        assert 'dateTimeUtc' in data[1], 'Response does not have "dateTimeUtc"'
        
        return data

    except Exception as e:
        print(f'An error occured while getting data from API: {e}')

        return None

# Configuring a monitor function for updating table when new data published
# Notice: As the data doesn't remain static, we also will get the new data along with the data for the past month
def monitoring(
    url: str,
    endpoint: str, 
    from_utc: str, 
    to_utc: str,
    headers: dict,
    to_monitor: str,
    #login: str,
    #password: str,
    #page: int = 1 -- API doesn't support pagination

    ) -> str:
    
    try:
        print(f'Monitoring request: {url}{endpoint}?FromUtc=%s&&ToUtc=%s' % (from_utc, to_utc))

        response = rq.get(
            (f'{url}{endpoint}?FromUtc=%s&&ToUtc=%s' % (from_utc, to_utc)).encode('utf-8'), 
            headers=headers,
            stream=True, 
            #auth=(login, password)
        ).content

        data = [obj['status'] for obj in json.loads(response)['data'] if obj['page'] == to_monitor]

        return data[0]

    except Exception as e:
        print(f'An error occured while monitoring request: {e}')