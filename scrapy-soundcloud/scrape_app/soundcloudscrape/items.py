# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class SoundcloudArtistItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = Field()
    comments_count = Field()
    country_code = Field()
    created_at = Field()
    description = Field()
    followers_count = Field()
    followings_count = Field()
    first_name = Field()
    sc_id = Field()
    last_modified = Field()
    last_name = Field()
    likes_count = Field()
    permalink = Field()
    permalink_url = Field()
    track_count = Field()
    uri = Field()
    urn = Field()
    username = Field()


class SoundcloudWebProfileItem(Item):
    sc_id = Field()
    url = Field()
    network = Field()
    title = Field()
    username = Field()


class FacebookProfileItem(Item):
    fb_id = Field()
    sc_id = Field()
    genre = Field()
    record_label = Field()
    current_location = Field()


class SoundcloudTrackItem(Item):
    comment_count = Field()
    created_at = Field()
    description = Field()
    download_count = Field()
    duration = Field()
    genre = Field()
    tr_id = Field()
    label_name = Field()
    likes_count = Field()
    playback_count = Field()
    release_date = Field()
    repost_count = Field()
    tag_list = Field()
    title = Field()
    sc_id = Field()
    album_title = Field()
    contains_music = Field()
    upc_or_ean = Field()
    isrc = Field()
    explicit = Field()
    writer_composer = Field()
    c_line = Field()