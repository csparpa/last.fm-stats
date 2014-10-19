import requests


class HttpClient():

    root_url = "http://ws.audioscrobbler.com/2.0"
    method = "user.getrecenttracks"

    def __init__(self, api_key):
        """
        An HTTP client for the Last.fm web API

        :param api_key: the API key to be associated to the request
        :type api_key: str
        """
        self.api_key = api_key

    def get_recent_tracks_for(self, username, before=None):
        """
        Retrieves the listened-to track history for a specific user

        :param username: the username
        :type username: str
        :param before: if this value is not None, only tracks listened to before
            this UTC Unix timtestamp are retrieved. If it is None, then tracks
            dating back from the current time are retrieved.
        :type before: int
        :returns: a dict representing the JSON payload of the HTTP response
        """
        query_params = dict(method=self.method, user=username,
                            api_key=self.api_key, format="json")
        if before is not None:
            query_params.update(dict(to=before))
        try:
            resp = requests.get(self.root_url, params=query_params)
        except requests.ConnectionError:
            print "Impossible to retrieve Last.fm web API: skipping request"
            return None
        return resp.json()