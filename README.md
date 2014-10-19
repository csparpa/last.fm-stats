last.fm-stats
=============

Exercise on Last.fm data aggregation

Works on
--------
Python 2.7

How to use it
-------------

1. Clone source code into a folder the Python interpreter can write into (eg. your
   home directory):
```bash
$ git clone git@github.com:csparpa/last.fm-stats.git
```

2. Install dependencies:
```bash
$ cd last.fm_stats
$ sudo pip install -r requirements.txt
```
(omit `sudo` if on Windows)

3. Launch the script replacing `<username>` with the username you want stats for:
```bash
$ python lastfm_stats.py <username>

You have listened to a total of 254 tracks. 
Your top 5 favorite artists: U2, Led Zeppelin, Rolling Stones, Bob Marley, Kasabian.
You listen to an average of 32 tracks a day.
Your most active day is Tuesday.
```

How to run the test suites
--------------------------
Make sure you are inside the git-cloned folder and execute:
```bash
$ python -m unittest discover
```

What you need to know
---------------------
* Only unit tests have been provided, using mocks where needed for the
  external components:
    - Last.fm web API
    - SQLite database
* Average tracks per day are rounded to the lowest integer value
