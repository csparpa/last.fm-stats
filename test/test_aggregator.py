import unittest
from lastfm_stats import aggregator
from mock import MagicMock


class TestAggregator(unittest.TestCase):

    ds = MagicMock()
    instance = aggregator.Aggregator(ds)

    def test_count_unique_tracks(self):
        expected = 100
        self.ds.count_unique_tracks = MagicMock(return_value=expected)
        result = self.instance.count_unique_tracks()
        self.assertEquals(1, len(self.ds.count_unique_tracks.call_args_list))
        self.assertEquals(expected, result)

    def test_top_five_favorite_artists(self):
        retrieved = [('U2', 78), ('Led Zeppelin', 65), ('Rolling Stones', 61),
            ('Bob Marley', 34), ('Kasabian', 22), ('Darkness', 9), ('Who', 4)]
        expected = ['U2', 'Led Zeppelin', 'Rolling Stones', 'Bob Marley',
                    'Kasabian']
        self.ds.ordered_artist_occurrences = MagicMock(return_value=retrieved)
        result = self.instance.top_five_favorite_artists()
        self.assertListEqual(expected, result)

    def test_daily_average_tracks(self):
        expected = 1
        utss = [(100,), (1234567,), (5687149,)]
        n_tracks = 3
        self.ds.get_all_listening_uts = MagicMock(return_value=utss)
        self.ds.count_tracks = MagicMock(return_value=n_tracks)
        result = self.instance.daily_average_tracks()
        self.assertEquals(expected, result)

    def test_daily_average_tracks_when_no_tracks_listened(self):
        expected = 0
        self.ds.get_all_listening_uts = MagicMock(return_value=[])
        self.ds.count_tracks = MagicMock(return_value=0)
        result = self.instance.daily_average_tracks()
        self.assertEquals(expected, result)

    def test_most_active_weekday(self):
        expected = "Thu"  # UTS=1413468998 -> Thu Jan 01, 1970
        utss = [(1413468998,), (1413478998,), (1413488998,)]
        self.ds.get_all_listening_uts = MagicMock(return_value=utss)
        result = self.instance.most_active_weekday()
        self.assertEquals(expected, result)

    def test_most_active_weekday_when_no_tracks_listened(self):
        expected = None
        self.ds.get_all_listening_uts = MagicMock(return_value=[])
        result = self.instance.most_active_weekday()
        self.assertEquals(expected, result)