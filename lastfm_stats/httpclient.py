import requests

"""
Module containing an HTTP client for the Last.fm web API
"""

class HttpClient():

    root_url = "http://ws.audioscrobbler.com/2.0"
    method = "user.getrecenttracks"

    """
    Retrieves the listened-to track history for a specific user

    :param username: the username
    :type username: str
    :param api_key: the API key to be associated to the request
    :type api_key: str
    :param page: identifier for the results page that must be retrieved
    :returns: int
    """
    def get_track_history(self, username, api_key, page=1):
        query_params = dict(method=self.method, user=username,
                            api_key=api_key, format="json", page=str(page))
        resp = requests.get(self.root_url, params=query_params)
        return resp.json()
