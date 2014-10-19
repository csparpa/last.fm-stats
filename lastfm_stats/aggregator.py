from math import floor
from datetime import datetime

class Aggregator():

    WEEKDAYS_NAMES = {
        0: "Mon",
        1: "Tue",
        2: "Wed",
        3: "Thu",
        4: "Fri",
        5: "Sat",
        6: "Sun"
    }

    def __init__(self, datastore):
        """
        A statistics provider on the top of a datastore

        :param datastore: the datastore whose data are aggregated
        :type datastore: a lastfm_stats.datastore.Datastore instance
        """
        self.datastore = datastore


    def count_unique_tracks(self):
        """
        Counts the number of unique listened-to tracks.

        :returns: an int
        """
        return self.datastore.count_unique_tracks()

    def top_five_favorite_artists(self):
        """
        Works out the names of the top five listened-to artists.

        :returns: a list of str
        """
        occurrences = self.datastore.ordered_artist_occurrences()
        return [t[0] for t in occurrences[:5]]

    def daily_average_tracks(self):
        """
        Calculates the average number of tracks listened-to per day. The average
        is computed taking into account only the days for which data exist in
        the datastore. The average is rounded to the closest lower integer.

        :returns: an int
        """
        utss = self.datastore.get_all_listening_uts()
        if len(utss) == 0:
            return 0
        dates = [datetime.fromtimestamp(uts[0]).date() for uts in utss]
        unique_dates = set(dates)
        n_utss = len(unique_dates)
        n_tracks = self.datastore.count_tracks()
        return floor(n_tracks/n_utss)

    def most_active_weekday(self):
        """
        Identifies the week day in which most listens occurred.

        :returns: a str
        """
        utss = self.datastore.get_all_listening_uts()
        listens_per_weekday = \
            dict.fromkeys(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 0)
        for uts in utss:
            weekday_number = datetime.fromtimestamp(uts[0]).weekday()
            weekday_name = self.WEEKDAYS_NAMES[weekday_number]
            listens_per_weekday[weekday_name] += 1
        if any(listens_per_weekday.values()):
            return max(listens_per_weekday.iterkeys(),
                       key=(lambda key: listens_per_weekday[key]))
        else:
            return None