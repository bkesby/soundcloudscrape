# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from models import Artists, WebProfiles, FacebookProfiles, Tracks, db_connect, create_table
from items import SoundcloudArtistItem, SoundcloudWebProfileItem, SoundcloudTrackItem, FacebookProfileItem


class SoundcloudPipeline(object):
    ''' Soundcloud pipeline for storing scraped items in the database'''
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates artists table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def insert_item(self, item):
        session = self.Session()
        try:
            session.add(item)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def process_item(self, item, spider):
        """
        Save items in the database.
        """
        # Handle soundcloud artist item.
        if isinstance(item, SoundcloudArtistItem):
            artist = Artists(**item)
            self.insert_item(artist)
            return item

        # Handle soundcloud web profile item.
        if isinstance(item, SoundcloudWebProfileItem):
            wprofile = WebProfiles(**item)
            self.insert_item(wprofile)
            return item

        # Handle facebook profile item.
        if isinstance(item, FacebookProfileItem):
            facebook = FacebookProfiles(**item)
            self.insert_item(facebook)
            return item

        # handle soundcloud track item.
        if isinstance(item, SoundcloudTrackItem):
            track = Tracks(**item)
            self.insert_item(track)
            return item