#!/usr/bin/env python

from sys import argv
from lastfm_stats import HttpClient, TrackParser, Datastore, Aggregator
from sqlalchemy import create_engine

if __name__ == '__main__':

    api_key = '37ec4aba2276f65295c2401e38355447'
    username = argv[1]
    client = HttpClient(api_key)
    ds = Datastore(create_engine('sqlite:///%s.db' % (username,)))
    aggr = Aggregator(ds)

    def save_track_history_for(username, before=None):
        json_blob = client.get_recent_tracks_for(username, before)
        if json_blob is not None:
            ds.save(TrackParser.parse(json_blob))

    # Retrieve recently listened to data from API
    save_track_history_for(username)

    # Identify oldest saved track for user then retrieve historical listenings
    # This is done exactly 4 times
    for _ in range(4):
        uts = ds.oldest_listening_uts()
        save_track_history_for(username, uts)

    # Get stats
    print 'You have listened to a total of %d tracks.' % \
          (aggr.count_unique_tracks(),)

    print 'Your top 5 favorite artists: %s.' % \
          (", ".join(aggr.top_favorite_artists()),)

    avg = aggr.daily_average_tracks()
    if avg is not None:
        print 'You listen to an average of %d tracks a day.' % (avg,)
    else:
        print 'You never listened to any track.'

    print 'Your most active day is %s.' % (aggr.most_active_weekday(),)