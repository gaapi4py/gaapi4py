VIEW_ID = "<insert your view_id>"
PATH_TO_SERVICE_ACCOUNT = "/path/to/service_account.json"

settings = {
    "view_id": VIEW_ID,
    "path_to_service_account": PATH_TO_SERVICE_ACCOUNT,
    "test_dateranges": {"start_date": "2019-01-01", "end_date": "2019-01-07"},
    "base_request_body_no_dateranges": {
        "dimensions": ["ga:date"],
        "metrics": ["ga:sessions"],
    },
    "base_request_body_with_dateranges_and_view_id": {
        "view_id": VIEW_ID,
        "start_date": "2019-01-01",
        "end_date": "2019-01-07",
        "dimensions": ["ga:date"],
        "metrics": ["ga:sessions"],
    },
    "request_body_with_sampling": {
        "view_id": VIEW_ID,
        "start_date": "2019-01-01",
        "end_date": "2019-06-07",
        "dimensions": ["ga:date"],
        "metrics": ["ga:hits"],
        # added filter clause to engage more dimensions and trigger sampling
        "filter": "ga:sourceMedium==google / organic,ga:pagePath=~/login",
    },
    "request_body_with_100k_plus_rows": {
        "view_id": VIEW_ID,
        "start_date": "2019-01-01",
        "end_date": "2019-01-07",
        "dimensions": ["ga:dimension5"],  # dimension with high cardinality, e.g. hit_id
        "metrics": ["ga:hits"],
    },
}
