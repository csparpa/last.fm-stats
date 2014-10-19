
from lastfm_stats import HttpClient, Datastore, Aggregator, trackparser
from sqlalchemy import create_engine


class UserStats():

    def __init__(self, username, api_key):
        """
        Drives updates and storage of Last.fm user data and reports statistics.

        :param username: the Last.fm user you want stats for
        :type username: str
        :param api_key: the Last.fm API key
        :type api_key: str
        """
        self.username = username
        self.client = HttpClient(api_key)
        self.ds = Datastore(create_engine('sqlite:///%s.db' % (username,)))
        self.aggregator = Aggregator(self.ds)

    def acquire_track_history(self, before=None):
        """
        Calls once the Last.fm web API to retrieve track history data for the
        user, then parse the data and save to the datastore.

        :param before: if this value is not None, only retrieve track listens
            data before this UTC Unix timtestamp. If it is None, then tracks
            data dating back from the current time is retrieved.
        :type before: int
        """
        data = self.client.get_recent_tracks_for(self.username, before)
        if data is not None:
            self.ds.save_track_list(trackparser.parse_track_collection(data))

    def update_user_task_history(self, max_api_calls=5):
        """
        Polls the Last.fm web API a certain number of times trying to backfill
        as much historical track data as possible for the user.

        :param max_api_calls: max number of times the web API shall be invoked.
            Defaults to 5.
        :type max_api_calls: int
        """
        if max_api_calls > 5:
            max_api_calls = 5
        self.acquire_track_history()  # Retrieve recently listened-to tracks
        for _ in range(max_api_calls-1):
            # Identify oldest saved track for user
            uts = self.ds.oldest_listening_uts()
            if uts is None: # API has no data for this user: stop calling it
                break
            self.acquire_track_history(uts) # Backfill history of tracks

    def unique_tracks(self):
        """
        Prints to stdout the a quote containing the number of unique tracks
        listened-to so far by the user.
        """
        unique_tracks = self.aggregator.count_unique_tracks()
        if unique_tracks != 0:
            print 'You have listened to a total of %d tracks.' % (unique_tracks,)
        else:
            print 'You never listened to any track so far.'

    def top_five_favorite_artists(self):
        """
        Prints to stdout the a quote containing the names of the top five artists
        listened-to so far by the user.
        """
        top_five = self.aggregator.top_five_favorite_artists()
        if top_five:
            print 'Your top 5 favorite artists: %s.' % (", ".join(top_five),)
        else:
            print 'You haven\'t got favorite artists yet.'

    def daily_average_tracks(self):
        """
        Prints to stdout the a quote containing the average number of tracks
        listened-to per day by the user so far.
        """
        print 'You listen to an average of %d tracks a day.' % \
              (self.aggregator.daily_average_tracks(),)

    def most_active_weekday(self):
        """
        Prints to stdout the a quote containing the week day on which the user
        has done the biggest number of track listens so far.
        """
        day = self.aggregator.most_active_weekday()
        if day is not None:
            print 'Your most active day is %s.' % (day,)
        else:
            print 'You haven\'t had a most active day yet.'

    def analyse(self):
        """
        Prints to stdout a full stats report on the Last.fm user listening habits.
        """
        # Acquire user raw data and save it
        self.update_user_task_history()

        # Aggregate data from datastore
        self.unique_tracks()
        self.top_five_favorite_artists()
        self.daily_average_tracks()
        self.most_active_weekday()