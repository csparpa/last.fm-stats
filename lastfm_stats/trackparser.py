from datastore import Track, Artist

class TrackParser():

    @staticmethod
    def parse(blob):
        result = []
        try:
            recent_tracks_blob = blob['recenttracks']['track']
            for track_blob in recent_tracks_blob:
                track = TrackParser.build_track_from(track_blob)
                if track is not None:
                    result.append(track)
        except KeyError:
            print "Impossible to parse user track data"
        finally:
            return result

    @staticmethod
    def build_track_from(track_blob):
        try:
            artist = Artist(id=track_blob['artist']['#text'])
            track = Track(name=track_blob['name'],
                          listening_uts=int(track_blob['date']['uts']),
                          artist_id=artist.id,
                          artist=artist)
            return track
        except KeyError:
            print "Impossible to parse data for this track: skipping"
            return None