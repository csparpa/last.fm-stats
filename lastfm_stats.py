#!/usr/bin/env python

"""
Lastfm_stats: aggregated Last.fm user statistics

Usage:
    python lastfm_stats.py <username>

Parameters:
    <username> = the Last.fm username you want stats for

Synopsis:
    the script will write on stdout:
        - The total number of tracks listened by <username>
        - The five top artists listened by <username>
        - The daily average number of tracks listened by <username>
        - The most active week day for <username>
"""

from lastfm_stats import UserStats
from sys import argv

username = argv[1]
api_key = '37ec4aba2276f65295c2401e38355447'

user_stats = UserStats(username, api_key)
user_stats.analyse()