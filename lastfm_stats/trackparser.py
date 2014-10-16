from datastore import Track, Artist

class TrackParser():

    @staticmethod
    def parse(blob):
        result = []
        tracks = blob['recenttracks']['track']
        for track in tracks:
            try:
                artist = Artist(id=track['artist']['#text'])
                track = Track(listening_uts=int(track['date']['uts']),
                              artist=artist)
                result.append(track)
            except KeyError:
                print "Error in parsing track info: skipping"
        return result