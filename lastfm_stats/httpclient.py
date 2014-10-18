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
        query_params = self.build_query_params(username, before)
        try:
            resp = requests.get(self.root_url, params=query_params)
        except requests.ConnectionError:
            print "Impossible to retrieve Last.fm web API: skipping request"
            return None
        return resp.json()

    def build_query_params(self, username, before):
        """
        Builds a dict of query parameters for requesting recent tracks.
        The function adds more key-value couples to the ones passed as parameters:
        it specifies the object method used to query the API, the return format
        and the API key.

        :param username: the username
        :type username: str
        :param before: if this value is not None, it is mapped into the query
            parameters otherwise it is left out.
        :type before: int
        :returns: a dict representing the HTTP request query parameters
        """
        params = dict(method=self.method, user=username, api_key=self.api_key,
                      format="json")
        if before is not None:
            return dict(params, to=before)
        else:
            return params