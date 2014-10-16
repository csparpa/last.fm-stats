from datastore import Track, Artist

class TrackParser():

    @staticmethod
    def parse(blob):
        result = []
        tracks = blob['recenttracks']['track']
        for track in tracks:
            try:
                artist = Artist(mbid=track['artist']['mbid'],
                                name=track['artist']['#text'])
                track = Track(mbid=track['mbid'],
                              listening_uts=track['date']['uts'],
                              artist=artist)
                result.append(track)
            except KeyError:
                print "Error in parsing track info: skipping"
        return result