# gaapi4py
Google Analytics Reporting API v4 for Python 3

## Quick Start

```python
from gaapi4py import client

c = client.GAClient('path/to/service_account.json')

request_body = {
    'view_id': '123456789',
    'start_date': '2019-01-01',
    'end_date': '2019-02-01',
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