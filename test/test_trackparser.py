import unittest
from lastfm_stats import trackparser
from lastfm_stats import datastore

class TestTrackParser(unittest.TestCase):
    artist1 = datastore.Artist(id="Led Zeppelin")
    artist2 = datastore.Artist(id="Johann Sebastian Bach")
    track1 = datastore.Track(name="Misty mountain hop",
                             listening_uts=1234567,
                             artist_id=artist1.id,
                             artist=artist1)
    track2 = datastore.Track(name="Toccata and fugue in D minor BWV565",
                             listening_uts=2345678,
                             artist_id=artist2.id,
                             artist=artist2)

    track1_blob = {
        "artist": {
            "#text": "Led Zeppelin"
        },
        "name": "Misty mountain hop",
        "date": {
            "uts": "1234567"
        }
    }

    track2_blob = {
        "artist": {
            "#text": "Johann Sebastian Bach"
        },
        "name": "Toccata and fugue in D minor BWV565",
        "date": {
            "uts": "2345678"
        }
    }

    response_blob = {
        "recenttracks": {
            "track": [track1_blob, track2_blob]
        }
    }

    malformed_response_blob = {
        "test": "value"
    }

    def assertTracksEqual(self, base, compared):
        self.assertEqual(base.artist_id, compared.artist_id)
        self.assertEqual(base.name, compared.name)
        self.assertEqual(base.listening_uts, compared.listening_uts)

    def test_build_track_from_builds_a_track(self):
        expected = self.track1
        result = trackparser.build_track_from(self.track1_blob)
        self.assertTracksEqual(expected, result)

    def test_build_track_from_with_malformed_blob(self):
        result = trackparser.build_track_from(self.malformed_response_blob)
        self.assertIsNone(result)

    def test_parse_returns_list_of_tracks(self):
        result_list = trackparser.parse(self.response_blob)
        self.assertEqual(2, len(result_list))
        self.assertTracksEqual(self.track1, result_list[0])
        self.assertTracksEqual(self.track2, result_list[1])

    def test_parse_with_malformed_blob(self):
        result = trackparser.parse(self.malformed_response_blob)
        self.assertEqual(0, len(result))