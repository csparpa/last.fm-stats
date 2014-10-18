from sqlalchemy import Column, ForeignKey, String, Integer, BigInteger, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'Artist'
    id = Column(String(56), primary_key=True)

class Track(Base):
    __tablename__ = 'Track'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    listening_uts = Column(BigInteger, nullable=False)
    artist_id = Column(String, ForeignKey('Artist.id'), nullable=False)
    artist = relationship(Artist)

class Datastore():

    def __init__(self, engine):
        # Init ORM
        self.engine = engine
        self.session = sessionmaker(bind=self.engine)()
        Base.metadata.create_all(self.engine)

    def save_track_list(self, list_of_tracks):
        try:
            for track in list_of_tracks:
                self.session.merge(track)
        except:
            self.session.rollback()
            raise
        finally:
            self.session.commit()

    def oldest_listening_uts(self):
        query = self.session.query(func.min(Track.listening_uts).label("min_uts"),)
        self.session.close()
        return query.one().min_uts

    def count_tracks(self):
        query = self.session.query(Track.name)
        self.session.close()
        return query.count()

    def count_unique_tracks(self):
        query = self.session.query(Track.name).distinct()
        self.session.close()
        return query.count()

    def get_all_listening_uts(self):
        query = self.session.query(Track.listening_uts)
        self.session.close()
        return query.all()

    def artist_occurrences(self):
        query = self.session.query(Track.artist_id,
                    func.count(Track.artist_id).label("cnt")).\
                    group_by(Track.artist_id).\
                    order_by(desc("cnt")
                )
        self.session.close()
        return query.all()