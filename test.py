import unittest
from datetime import date

from googleapiclient.errors import HttpError


from gaapi4py import GAClient

from test_settings import settings

daterange_settings = settings.get("test_dateranges")


class TestClient(unittest.TestCase):
    def test_client_creation(self):
        """
        Test that client instance is initiated
        """
        client = GAClient(settings.get("path_to_service_account"))

        self.assertIs(type(client), GAClient)

    def test_should_fail_to_init_without_creds(self):
        with self.assertRaises(TypeError) as context:
            GAClient()
        self.assertTrue(
            "missing 1 required positional argument" in str(context.exception)
        )

    def test_set_view_id(self):

        client = GAClient(settings.get("path_to_service_account"))

        view_id = settings.get("view_id")
        client.set_view_id(view_id)
        self.assertEqual(client.view_id, view_id)

    def test_set_dateranges_strings(self):

        client = GAClient(settings.get("path_to_service_account"))

        start_date = daterange_settings.get("start_date")
        end_date = daterange_settings.get("end_date")

        client.set_dateranges(start_date, end_date)
        self.assertIsInstance(client.start_date, date)
        self.assertIsInstance(client.end_date, date)

        self.assertEqual(
            start_date,
            client.start_date.strftime("%Y-%m-%d"),
            msg="Start date is not equal",
        )
        self.assertEqual(
            end_date,
            client.end_date.strftime("%Y-%m-%d"),
            msg="Start date is not equal",
        )

    def test_should_error_on_request_with_no_dateranges(self):

        client = GAClient(settings.get("path_to_service_account"))

        base_request_body_no_dateranges = settings.get(
            "base_request_body_no_dateranges"
        )
        with self.assertRaises(HttpError) as context:
            client.get_all_data(base_request_body_no_dateranges)
        self.assertTrue("HttpError 400" in str(context.exception))

    def test_should_load_data_on_request_after_dateranges_set(self):
        base_request_body_no_dateranges = settings.get(
            "base_request_body_no_dateranges"
        )
        start_date = daterange_settings.get("start_date")
        end_date = daterange_settings.get("end_date")
        client = GAClient(settings.get("path_to_service_account"))
        client.set_view_id(settings.get("view_id"))
        client.set_dateranges(start_date, end_date)

        res = client.get_all_data(base_request_body_no_dateranges)

        self.assertIs(
            res["info"]["isDataGolden"], True, "info.isDataGolden should be True"
        )
        self.assertIsNone(res["info"]["nextPageToken"], "NextPageToken should be None")
        self.assertIsNone(
            res["info"]["samplingSpaceSizes"], "Data should not be sampled"
        )
        self.assertIsNone(
            res["info"]["samplesReadCounts"], "Data should not be sampled"
        )

        self.assertEqual(len(res["data"]), 7, "Result dataset should contain 7 rows")

    def test_should_load_data_with_overridden_view_id_and_dateranges(self):

        client = GAClient(settings.get("path_to_service_account"))
        client.set_view_id("1234567890")
        client.set_dateranges("2019-01-01", "2019-01-01")
        res = client.get_all_data(
            settings.get("base_request_body_with_dateranges_and_view_id")
        )
        self.assertEqual(len(res["data"]), 7, "Result dataset should contain 7 rows")

    def test_should_load_with_sampling(self):
        client = GAClient(settings.get("path_to_service_account"))
        res = client.get_all_data(settings.get("request_body_with_sampling"))
        self.assertIsNotNone(
            res["info"]["samplesReadCounts"], "Should have sampling size"
        )

    def test_should_have_more_than_100k_rows(self):
        client = GAClient(settings.get("path_to_service_account"))
        res = client.get_all_data(settings.get("request_body_with_100k_plus_rows"))
        self.assertGreater(len(res["data"]), 100000)

    """
    test cases which should cover future implementations
    """


if __name__ == "__main__":
    unittest.main()
