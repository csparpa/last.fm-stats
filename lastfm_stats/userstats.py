
from lastfm_stats import HttpClient, Datastore, Aggregator, trackparser
from sqlalchemy import create_engine

class UserStats():

    def __init__(self, username, api_key):
        self.username = username
        self.client = HttpClient(api_key)
        self.ds = Datastore(create_engine('sqlite:///%s.db' % (username,)))

    def acquire_track_history(self, before=None):
        json_blob = self.client.get_recent_tracks_for(self.username, before)
        if json_blob is not None:
            self.ds.save_track_list(trackparser.parse(json_blob))

    def update_user_task_history(self, max_api_calls=5):
        # Retrieve recently listened to tracks data from API
        self.acquire_track_history()
        for _ in range(max_api_calls-1):
            # Identify oldest saved track for user
            uts = self.ds.oldest_listening_uts()
            if uts is None: # API has no data for this user: stop calling it
                break
            self.acquire_track_history(uts) # Backfill history of tracks

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

    def analyse(self):
        # Acquire user raw data and save it
        self.update_user_task_history()

        # Aggregate data from datastore
        aggregator = Aggregator(self.ds)
        self.unique_tracks(aggregator)
        self.top_five_favorite_artists(aggregator)
        self.daily_average_tracks(aggregator)
        self.most_active_weekday(aggregator)