#!/usr/bin/env python

from sys import argv
from lastfm_stats import HttpClient, TrackParser, Datastore


api_key = '37ec4aba2276f65295c2401e38355447'

if __name__ == '__main__':
    username = argv[1]
    client = HttpClient()
    parser = TrackParser()
    ds = Datastore('lastfm_stats.db')

    # Retrieve recently listened to data from API
    blob = client.get_track_history(username, api_key, 2)


    # Store data to database
    list_of_tracks = parser.parse(blob)
    ds.save(list_of_tracks)

    # Retrieve historical listenings

    # Store data to database

    # Aggregate data from database