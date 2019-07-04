from datetime import datetime, timedelta, date
import time
import pandas as pd
import httplib2 as lib2
from oauth2client import client
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
API_NAME = 'analyticsreporting'
API_VERSION = 'v4'
USER_AGENT = 'gapy/0.1'


class GAClient:
    """
    Client Instance.
    """

    def __init__(self, json_keyfile):
        """
        Read service key file and initialize the API client
        """
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            json_keyfile, scopes=SCOPES)
        self.client = build(API_NAME, API_VERSION, credentials=credentials)

    def set_view_id(self, view_id):
        """
        Specify View ID and use it in all requests, if not explicitly specified
        """
        self.view_id = view_id

    def set_dateranges(self, start_date, end_date):
        """
        Sets default dates to generate request bodies

        Args:
            start_date: string in format 'YYYY-MM-DD'
            end_date: string in format 'YYYY-MM-DD'
        """
        if isinstance(start_date, str):
            self.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        else:
            self.start_date = start_date
        if isinstance(end_date, str):
            self.end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            self.end_date = end_date

    def _generate_request_body(self, params):
        """
        Read request parameters in simplified form and generate
        proper request body for batch request
        """

        sd = params.get('start_date', self.start_date)
        ed = params.get('end_date', self.end_date)
        include_empty_rows = params.get('include_empty_rows', True)

        if isinstance(sd, date):
            start_date = datetime.strftime(sd, '%Y-%m-%d')

        if isinstance(ed, date):
            end_date = datetime.strftime(ed, '%Y-%m-%d')

        dimensions = list(map(lambda x: {'name': x}, params.get('dimensions')))

        metrics = list(map(lambda x: {'expression': x}, params.get('metrics')))

        segments = []
        if params.get('segments'):
            dimensions.append({
                'name': 'ga:segments'
            })
            segments.append({
                'segmentId': params.get('segments')
            })

        request_body = {
            'viewId': params.get('view_id', self.view_id),
            'dateRanges': {
                'startDate': start_date,
                'endDate': end_date
            },
            'dimensions': dimensions,
            'metrics': metrics,
            'filtersExpression': params.get('filter', None),
            'pageToken': params.get('pageToken', None),
            'samplingLevel': 'LARGE',
            'includeEmptyRows': include_empty_rows,
            'segments': segments,
            'pageSize': '10000'
        }

        return request_body

    def parse_response(self, response_obj):
        """
        Parses and prints the Analytics Reporting API V4 response
        """

        report = response_obj.get('reports', None)[0]
        report_data = report.get('data', {})

        result = {}
        data = []
        header_row = []

        column_header = report.get('columnHeader', {})
        metric_header = column_header.get(
            'metricHeader', {}).get('metricHeaderEntries', [])
        dimension_header = column_header.get('dimensions', [])

        for dheader in dimension_header:
            header_row.append(dheader)
        for mheader in metric_header:
            header_row.append(mheader['name'])

        rows = report_data.get('rows', [])
        for row in rows:
            row_temp = []
            dimensions = row.get('dimensions', [])
            metrics = row.get('metrics', [])
            for d in dimensions:
                row_temp.append(d)
            for m in metrics[0]['values']:
                row_temp.append(m)
            data.append(row_temp)

        result_df = pd.DataFrame(data, columns=header_row)
        result_df.columns = result_df.columns.str.replace('ga:', '')

        if not report_data.get('samplesReadCounts'):
            samples_read_counts = None
            sampling_space_sizes = None
        else:
            samples_read_counts = int(
                report_data.get('samplesReadCounts', [])[0])
            sampling_space_sizes = int(
                report_data.get('samplingSpaceSizes', [])[0])

        result['samplesReadCounts'] = samples_read_counts
        result['samplingSpaceSizes'] = sampling_space_sizes
        result['nextPageToken'] = report.get('nextPageToken')
        result['isDataGolden'] = report['data'].get('isDataGolden', False)
        result['queryCost'] = response_obj.get('queryCost', None)
        result['data'] = result_df

        return result

    def request_to_df(self, params):
        """ 
        Make a single request to GA API with specified parameters
        """
        request_body = self._generate_request_body(params)
        raw_response = self.client.reports().batchGet(body={
            'reportRequests': request_body
        }).execute()
        parsed = self.parse_response(raw_response)

        return parsed
