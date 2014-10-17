import math
from datetime import datetime

class Aggregator():

    def __init__(self, datastore):
        self.datastore = datastore

    def count_unique_tracks(self):
        return self.datastore.count_unique_tracks()

    def top_favorite_artists(self):
        occurrences = self.datastore.artist_occurrences()
        return [t[0] for t in occurrences[:5]]

    def daily_average_tracks(self):
        utss = self.datastore.get_all_listening_uts()
        dates = [datetime.fromtimestamp(uts[0]).date() for uts in utss]
        unique_dates = set(dates)
        n_utss = len(unique_dates)
        n_tracks = self.datastore.count_tracks()
        if n_utss != 0:
            return math.floor(n_tracks/n_utss)
        else:
            return None

    def most_active_weekday(self):
        pass
