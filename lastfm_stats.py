#!/usr/bin/env python

from lastfm_stats import UserStats
from sys import argv

username = argv[1]
api_key = '37ec4aba2276f65295c2401e38355447'

user_stats = UserStats(username, api_key)
user_stats.analyse()