import math
from datetime import datetime

class Aggregator():



    def __init__(self, datastore):
        self.datastore = datastore
        self.weekdays_names = {
            0: "Mon",
            1: "Tue",
            2: "Wed",
            3: "Thu",
            4: "Fri",
            5: "Sat",
            6: "Sun"
        }

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
            return 0

    def most_active_weekday(self):
        utss = self.datastore.get_all_listening_uts()
        listens_per_weekday = \
            dict.fromkeys(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 0)
        for uts in utss:
            weekday_number = datetime.fromtimestamp(uts[0]).weekday()
            weekday_name = self.weekdays_names[weekday_number]
            listens_per_weekday[weekday_name] += 1
        if any(listens_per_weekday.values()):
            return max(listens_per_weekday.iterkeys(),
                       key=(lambda key: listens_per_weekday[key]))
        else:
            return None