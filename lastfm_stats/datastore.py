from sqlalchemy import Column, ForeignKey, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'Artist'
    mbid = Column(String(36), primary_key=True)
    name = Column(String(50), nullable=False)

class Track(Base):
    __tablename__ = 'Track'
    mbid = Column(String(36), primary_key=True)
    listening_uts = Column(String(20), nullable=False, primary_key=True)
    artist_mbid = Column(String, ForeignKey('Artist.mbid'), nullable=False)
    artist = relationship(Artist)



class Datastore():

    def __init__(self, db_name):
        # Init ORM
        self.engine = create_engine('sqlite:///'+db_name)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def save(self, list_of_tracks):
        session = self.Session()
        for track in list_of_tracks:
            session.merge(track)
        session.commit()
