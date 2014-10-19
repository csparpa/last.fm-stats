from sqlalchemy import Column, ForeignKey, String, Integer, BigInteger, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()

class Artist(Base):
    """
    SQLALchemy entity class representing an Artist
    """
    __tablename__ = 'Artist'
    id = Column(String(56), primary_key=True)

class Track(Base):
    """
    SQLALchemy entity class representing a listened-to Track
    """
    __tablename__ = 'Track'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    listening_uts = Column(BigInteger, nullable=False)
    artist_id = Column(String, ForeignKey('Artist.id'), nullable=False)
    artist = relationship(Artist)

class Datastore():

    def __init__(self, engine):
        """
        A data-access provider allowing to manipulate an underlying SQLAlchemy
        mapped table set

        :param engine: a database manager object
        :type engine: sqlalchemy.engine.Engine
        """
        self.engine = engine
        self.session = sessionmaker(bind=self.engine)()
        Base.metadata.create_all(self.engine)

    def save_track_list(self, list_of_tracks):
        """
        Persists a list of Track objects on the underlying database.
        If the database schema does not exist yet, it is created according to
        the URI of the engine before saving objects to the corresponding tables.
        Persistence is done via merging: this means that if the list contains
        objects that already exist in the database, no insertion attempts will
        be made for them.

        :param list_of_tracks: a list of Tracks to be persisted
        :type list_of_tracks: list of lastfm_stats.datastore.Track instances
        """
        try:
            for track in list_of_tracks:
                self.session.merge(track)
        except:
            self.session.rollback()
            raise
        finally:
            self.session.commit()

    def oldest_listening_uts(self):
        """
        Retrieves the UTC Unix Timestamp corresponding to the oldest listened-to
        track in the database.

        :returns: an int  UTC Unix Timestamp
        """
        query = self.session.query(func.min(Track.listening_uts).label("min_uts"),)
        self.session.close()
        return query.one().min_uts

    def count_tracks(self):
        """
        Counts the number of listened-to tracks in the database (the tracks
        are not unique, eg: the same track could have been listened to multiple
        times).

        :returns: an int
        """
        query = self.session.query(Track.name)
        self.session.close()
        return query.count()

    def count_unique_tracks(self):
        """
        Counts the number of unique listened-to tracks in the database.

        :returns: an int
        """
        query = self.session.query(Track.name).distinct()
        self.session.close()
        return query.count()

    def get_all_listening_uts(self):
        """
        Retrieves all the UTC Unix Timestamps corresponding to track listens
        in the database.

        :returns: a list of tuples in the form: (timestamp, ) where 'timestamp'
            is an int
        """
        query = self.session.query(Track.listening_uts)
        self.session.close()
        return query.all()

    def ordered_artist_occurrences(self):
        """
        For all the artists in the database, retrieves the corresponding number
        of listened-to tracks, then orders the returned sequence in a decreasing
        frequency order (that is, starting from the most frequent artist up to
        the least)

        :returns: a list of tuples in the form: (artist_id, frequency) where
            'artist_id' is a str and 'frequency' is an int. The list is
            ordered by decreasing values of 'frequency'
        """
        query = self.session.query(Track.artist_id,
                    func.count(Track.artist_id).label("cnt")).\
                    group_by(Track.artist_id).\
                    order_by(desc("cnt")
                )
        self.session.close()
        return query.all()