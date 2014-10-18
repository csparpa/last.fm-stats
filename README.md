last.fm-stats
=============

Exercise on Last.fm data aggregation

Works on
--------
Python 2.7

How to use it
-------------

1. Install dependencies:
```bash
$ pip install -r requirements.txt
```

2. Launch replacing `<username>` with the username you want stats for:
```bash
$ python lastfm_stats <username>

You have listened to a total of 254 tracks. 
Your top 5 favorite artists: U2, Led Zeppelin, Rolling Stones, Bob Marley, Kasabian.
You listen to an average of 32 tracks a day.
Your most active day is Tuesday.
```

How to run the test suites
--------------------------
```bash
$ python setup.py test
```
