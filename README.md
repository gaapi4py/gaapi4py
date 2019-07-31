# gaapi4py

Google Analytics Reporting API v4 for Python 3

## Prerequisites

To use this library, you need to have a project in Google Cloud Platform and a service account key that has access to Google Analytics account you want to get data from.

## Quick Start

```python
from gaapi4py import client

c = client.GAClient('path/to/service_account.json')

request_body = {
    'view_id': '123456789',
    'start_date': '2019-01-01',
    'end_date': '2019-01-31',
    'dimensions': {
        'ga:sourceMedium',
        'ga:date'
    },
    'metrics': {
        'ga:sessions'
    }
}

response = c.get_all_data(request_body)

response['info'] # sampling and "golden" metadata

response['data'] # Pandas dataframe that contains data from GA
```

If you want to make many requests to a speficic view or with specific dateranges, you can set date ranges for all future requests:

```python
c.set_view_id('123456789')
c.set_dateranges('2019-01-01', '2019-01-31')

request_body_1 = {
    'dimensions': {
        'ga:sourceMedium',
        'ga:date'
    },
    'metrics': {
        'ga:sessions'
    }
}

request_body_2 = {
    'dimensions': {
        'ga:deviceCategory',
        'ga:date'
    },
    'metrics': {
        'ga:sessions'
    }
}

response_1 = c.get_all_data(request_body_1)
response_2 = c.get_all_data(request_body_2)
```
