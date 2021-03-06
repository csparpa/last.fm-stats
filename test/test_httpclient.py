import unittest
import requests
from mock import MagicMock
from lastfm_stats import httpclient


class TestHttpClient(unittest.TestCase):

    api_key = "test-api-key"
    username = "test"
    before = "1234567"
    instance = httpclient.HttpClient(api_key)

    def test_get_recent_tracks_for_invokes_issues_one_http_get(self):
        requests.get = MagicMock()
        self.instance.get_recent_tracks_for(self.username, self.before)
        self.assertEquals(1, len(requests.get.call_args_list))

    def test_get_recent_tracks_for_returns_none_when_connectivity_drops(self):
        requests.get = MagicMock(side_effect=requests.ConnectionError)
        result = self.instance.get_recent_tracks_for(self.username, self.before)
        self.assertIsNone(result)