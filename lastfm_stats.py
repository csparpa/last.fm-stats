#!/usr/bin/env python

from sys import argv
from lastfm_stats import HttpClient, TrackParser, Datastore


api_key = '37ec4aba2276f65295c2401e38355447'

if __name__ == '__main__':
    username = argv[1]
    client = HttpClient()
    ds = Datastore(username+'.db')

    # Retrieve recently listened to data from API
    json_blob = client.get_track_history(username, api_key)
    list_of_tracks = TrackParser.parse(json_blob)
    ds.save(list_of_tracks)

    # Identify oldest saved track for user then retrieve historical listenings
    # This is done exactly 4 times
    for _ in range(4):
        uts = ds.oldest_listening_uts()
        json_blob = client.get_track_history(username, api_key, to=uts)
        list_of_tracks = TrackParser.parse(json_blob)
        ds.save(list_of_tracks)