from datastore import Track, Artist


def build_track_from(track_dict):
    """
    Given a dict structured according the Last.fm API JSON representation for a
    Track, tries to parse a new Track object out of it. In case of
    non-conformities, returns None.

    :param track_dict: the dict containing Track data to be parsed
    :type track_dict: dict
    :returns: a lastfm_stats.datastore.Track instance or None in case of parse
        errors
    """
    try:
        artist = Artist(id=track_dict['artist']['#text'])
        track = Track(name=track_dict['name'],
                      listening_uts=int(track_dict['date']['uts']),
                      artist_id=artist.id,
                      artist=artist)
        return track
    except KeyError:
        print "Warning: impossible to parse data for this track, skipping"
        return None


def parse(track_collection_dict):
    """
    Given a dict structured according the Last.fm API JSON representation for
    recently listened-to tracks collection, tries to parse a list of Track
    objects out of it. In case of non-conformities, returns an empty list.

    :param track_collection_dict: the dict containing the Tracks collection
        data to be parsed
    :type track_collection_dict: dict
    :returns: a list of lastfm_stats.datastore.Track instances, empty in case
        of parse errors
    """
    result = []
    try:
        recent_tracks_blob = track_collection_dict['recenttracks']['track']
        for track_blob in recent_tracks_blob:
            track = build_track_from(track_blob)
            if track is not None:
                result.append(track)
    except KeyError:
        print "Warning: impossible to parse user track data, skipping data batch"
    finally:
        return result
