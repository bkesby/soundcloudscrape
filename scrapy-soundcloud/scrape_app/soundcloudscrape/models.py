from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

Base = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_table(engine):
    Base.metadata.create_all(engine)


class Artists(Base):
    ''' SqlAlchemy artists model '''
    __tablename__ = 'artists'

    sc_id = Column('sc_id', Integer, primary_key=True)
    username = Column('username', String, nullable=True)
    city = Column('city', String, nullable=True)
    country_code = Column('country_code', String, nullable=True)
    track_count = Column('track_count', Integer)
    followers_count = Column('followers_count', Integer)
    followings_count = Column('followings_count', Integer)
    comments_count = Column('comments_count', Integer)
    likes_count = Column('likes_count', Integer)
    description = Column('description', String, nullable=True)
    first_name = Column('first_name', String, nullable=True)
    last_name = Column('last_name', String, nullable=True)
    created_at = Column('created_at', DateTime)
    last_modified = Column('last_modified', DateTime)
    permalink = Column('permalink', String, nullable=True)
    permalink_url = Column('permalink_url', String, nullable=True)
    uri = Column('uri', String, nullable=True)
    urn = Column('urn', String, nullable=True)

class WebProfiles(Base):
    ''' SqlAlchemy web profiles model '''
    __tablename__ = 'web_profiles'

    network = Column('network', String, nullable=True)
    url = Column('url', String,  primary_key=True)
    title = Column('title', String, nullable=True)
    username = Column('username', String, nullable=True)
    sc_id = Column('sc_id', Integer, ForeignKey('artists.sc_id'))


class FacebookProfiles(Base):
    ''' SqlAlchemy facebook model'''
    __tablename__ = 'facebook_profiles'

    fb_id = Column('fb_id', String, primary_key=True)
    sc_id = Column('sc_id', Integer, ForeignKey('artists.sc_id'))
    genre = Column('genre', String, nullable=True)
    record_label = Column('record_label', String, nullable=True)
    current_location = Column('current_location', String, nullable=True)

class Tracks(Base):
    ''' SqlAlchemy tracks model '''
    __tablename__ = 'tracks'

    tr_id = Column('tr_id', Integer, primary_key=True)
    sc_id = Column('sc_id', Integer, ForeignKey('artists.sc_id'))
    title = Column('title', String, nullable=True)
    genre = Column('genre', String, nullable=True)
    playback_count = Column('playback_count', Integer)
    likes_count = Column('likes_count', Integer)
    comment_count = Column('comment_count', Integer)
    repost_count = Column('repost_count', Integer)
    download_count = Column('download_count', Integer)
    duration = Column('duration', Integer)
    label_name = Column('label_name', String, nullable=True)
    c_line = Column('c_line', String, nullable=True)
    tag_list = Column('tag_list', String, nullable=True)
    album_title = Column('album_title', String, nullable=True)
    created_at = Column('created_at', DateTime)
    release_date = Column('release_date', DateTime)
    description = Column('description', String, nullable=True)
    contains_music = Column('contains_music', Boolean, nullable=True)
    upc_or_ean = Column('upc_or_ean', String, nullable=True)
    isrc = Column('isrc', String, nullable=True)
    explicit = Column('explicit', Boolean, nullable=True)
    writer_composer = Column('writer_composer', String, nullable=True)