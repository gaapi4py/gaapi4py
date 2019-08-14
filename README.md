# gaapi4py

Google Analytics Reporting API v4 for Python 3

## Prerequisites

To use this library, you need to have a project in Google Cloud Platform and a service account key that has access to Google Analytics account you want to get data from.

## Quick Start

```python
from gaapi4py import GAClient

c = GAClient('path/to/service_account.json')

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
    },
    'filter': 'ga:sourceMedium==google / organic' # optional filter clause
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

## Avoid sampling by taking tada day-by-day

>Important! Google Analytics reporting API has a limit of maximum 100 requests per 100 seconds. If you want to iterate over large period of days, you might consider adding `time.sleep(1)` at the end of the loop to avoid reaching this limit.

```python
from datetime import date, timedelta
from time import sleep

import pandas as pd
from gaapi4py import GAClient

c = GAClient('gaapi4py.json')
c.set_view_id('159274569')

start_date = date(2019,7,1)
end_date = date(2019,7,14)

df_list = []
iter_date = start_date
while iter_date <= end_date:
    c.set_dateranges(iter_date, iter_date)
    response = c.get_all_data({
        'dimensions': {
            'ga:sourceMedium',
            'ga:deviceCategory'
        },
        'metrics': {
            'ga:sessions'
        }
    })
    df = response['data']
    df['date'] = iter_date
    df_list.append(response['data'])
    iter_date = iter_date + timedelta(days=1)
    time.sleep(1)

all_data = pd.concat(df_list, ignore_index=True)

```

## Avoid "maximum 7 dimensions" restriction

If you store sessionId and/or hitId as custom dimensions ([Example implementation on Simo Ahava's blog](https://www.simoahava.com/analytics/improve-data-collection-with-four-custom-dimensions/)), you can circumvent restriction on maximum number of dimensions and metrics in one report. Example below:

> If sampling starts to appear, try to break the set of dimensions into smaller parts and run queries on them.

```python
one_day = date(2019,7,1)
c.set_dateranges(one_day, one_day)

SESSION_ID_CD_INDEX = '2'
HIT_ID_CD_INDEX = '5'

session_id = 'dimension' + SESSION_ID_CD_INDEX
hit_id = 'dimension' + HIT_ID_CD_INDEX


#Get session scope data
response_1 = c.get_all_data({
    'dimensions': {
        'ga:' + session_id,
        'ga:sourceMedium',
        'ga:campaign',
        'ga:keyword',
        'ga:adContent',
        'ga:userType',
        'ga:deviceCategory'
    },
    'metrics': {
        'ga:sessions'
    }
})

response2 = c.get_all_data({
    'dimensions': {
        'ga:' + session_id,
        'ga:landingPagePath',
        'ga:secondPagePath',
        'ga:exitPagePath',
        'ga:pageDepth',
        'ga:daysSinceLastSession',
        'ga:sessionCount'
    },
    'metrics': {
        'ga:hits',
        'ga:totalEvents',
        'ga:bounces',
        'ga:sessionDuration'
    }
})

all_data = response_1['data'].merge(response2['data'], on=session_id, how='left')

all_data.rename(index=str, columns={
    session_id: 'session_id'
}, inplace=True)

all_data.head()

# Get hit scope data
hits_response_1 = c.get_all_data({
    'dimensions': {
        'ga:' + session_id,
        'ga:' + hit_id,
        'ga:pagePath',
        'ga:previousPagePath',
        'ga:dateHourMinute'
    },
    'metrics': {
        'ga:hits',
        'ga:totalEvents',
        'ga:pageviews'
    }
})

hits_response_2 = c.get_all_data({
    'dimensions': {
        'ga:' + session_id,
        'ga:' + hit_id,
        'ga:eventCategory',
        'ga:eventAction',
        'ga:eventLabel'
    },
    'metrics': {
        'ga:totalEvents'
    }
})

all_hits_data = hits_response_1['data'].merge(hits_response_2['data'],
                                              on=[session_id, hit_id],
                                              how='left')
all_hits_data.rename(index=str, columns={
    session_id: 'session_id',
    hit_id: 'hit_id'
}, inplace=True)

all_hits_data.head()

```
