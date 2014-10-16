#!/usr/bin/env python

from sys import argv
from lastfm_stats import HttpClient, TrackParser, Datastore


api_key = '37ec4aba2276f65295c2401e38355447'

if __name__ == '__main__':
    username = argv[1]
    client = HttpClient()
    ds = Datastore('lastfm_stats.db')

    # Call 1: retrieve recently listened to data from API
    json_blob = client.get_track_history(username, api_key, 1)
    list_of_tracks = TrackParser.parse(json_blob)
    ds.save(list_of_tracks)

    # Identify oldest saved track

    # Call 2: retrieve historical listenings
    json_blob = client.get_track_history(username, api_key, 2)
    list_of_tracks = TrackParser.parse(json_blob)
    ds.save(list_of_tracks)

    # Store data to database

    # Aggregate data from database