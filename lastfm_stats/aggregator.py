
class Aggregator():

    def __init__(self, datastore):
        self.datastore = datastore

    def count_unique_tracks(self):
        return self.datastore.count_unique_tracks()

    def top_favorite_artists(self):
        occurrences = self.datastore.artist_occurrences()
        return [t[0] for t in occurrences[:5]]


    def daily_average_tracks(self):
        pass

    def most_active_weekday(self):
        pass