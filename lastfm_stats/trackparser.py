from datastore import Track, Artist

class TrackParser():

    @staticmethod
    def parse(blob):
        result = []
        username = blob['recenttracks']['@attr']['user']
        tracks = blob['recenttracks']['track']
        for track in tracks:
            try:
                artist = Artist(id=track['artist']['#text'])
                track = Track(username=username,
                              listening_uts=track['date']['uts'],
                              artist=artist)
                result.append(track)
            except KeyError:
                print "Error in parsing track info: skipping"
        return result