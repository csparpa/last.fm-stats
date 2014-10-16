from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'Artist'
    mbid = Column(String(36), primary_key=True)
    name = Column(String(50), nullable=False)

class Track(Base):
    __tablename__ = 'Track'
    mbid = Column(String(36), primary_key=True)
    uts = Column(String(20), nullable=False)
    artist_mbid = Column(String, ForeignKey('Artist.mbid'), nullable=False)
    artist = relationship(Artist)



class Datastore():

    def __init__(self, db_name):
        # Init ORM
        self.engine = create_engine('sqlite:///'+db_name)
        Base.metadata.create_all(self.engine)