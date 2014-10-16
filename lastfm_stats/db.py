from sqlalchemy import create_engine

def create_db(dbpath):
    engine = create_engine('sqlite:///lastfm_stats.db')