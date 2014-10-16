import requests

"""
Module containing an HTTP client for the Last.fm web API
"""

class HttpClient():

    root_url = "http://ws.audioscrobbler.com/2.0"
    method = "user.getrecenttracks"

    def get_recent_tracks_for(self, username, api_key, before=None):
        """
        Retrieves the listened-to track history for a specific user

        :param username: the username
        :type username: str
        :param api_key: the API key to be associated to the request
        :type api_key: str
        :param before: if not None, only tracks listened to before this UTC Unix
            timtestamp are retrieved
        :type before: int
        :returns: a JSON Unicode string
        """
        query_params = dict(method=self.method, user=username,
                            api_key=api_key, format="json", to=before)
        resp = requests.get(self.root_url, params=query_params)
        return resp.json()
