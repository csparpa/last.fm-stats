
from lastfm_stats import HttpClient, TrackParser, Datastore, Aggregator
from sqlalchemy import create_engine

class UserStats():

    def __init__(self, username, api_key):
        self.username = username
        self.client = HttpClient(api_key)
        self.ds = Datastore(create_engine('sqlite:///%s.db' % (username,)))

    def analyse(self):
        # Call API
        self.get_task_history()

        # Aggregate data from datastore
        aggregator = Aggregator(self.ds)
        self.unique_tracks(aggregator)
        self.top_five_favorite_artists(aggregator)
        self.daily_average_tracks(aggregator)
        self.most_active_weekday(aggregator)

    def save_tracks_history(self, before=None):
        json_blob = self.client.get_recent_tracks_for(self.username, before)
        if json_blob is not None:
            self.ds.save_track_list(TrackParser.parse(json_blob))

    def get_task_history(self, max_api_calls=5):
        # Retrieve recently listened to tracks data from API
        self.save_tracks_history()

        # Identify oldest saved track for user, then retrieve historical listens
        # This is done exactly 4 times
        for _ in range(max_api_calls-1):
            uts = self.ds.oldest_listening_uts()
            self.save_tracks_history(uts)

    def unique_tracks(self, aggregator):
        unique_tracks = aggregator.count_unique_tracks()
        if unique_tracks != 0:
            print 'You have listened to a total of %d tracks.' % (unique_tracks,)
        else:
            print 'You never listened to any track so far.'

    def top_five_favorite_artists(self, aggregator):
        top_five = aggregator.top_five_favorite_artists()
        if top_five:
            print 'Your top 5 favorite artists: %s.' % (", ".join(top_five),)
        else:
            print 'You haven\'t got favorite artists yet.'

    def daily_average_tracks(self, aggregator):
        print 'You listen to an average of %d tracks a day.' % \
              (aggregator.daily_average_tracks(),)

    def most_active_weekday(self, aggregator):
        day = aggregator.most_active_weekday()
        if day is not None:
            print 'Your most active day is %s.' % (day,)
        else:
            print 'You haven\'t had a most active day yet.'