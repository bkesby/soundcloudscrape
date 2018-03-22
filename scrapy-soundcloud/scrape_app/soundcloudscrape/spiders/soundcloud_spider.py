# -*- coding: utf-8 -*-
import csv
import facebook
import json
from scrapy import Spider, Request
from soundcloudscrape.items import SoundcloudArtistItem, SoundcloudWebProfileItem, SoundcloudTrackItem, FacebookProfileItem
from string import ascii_lowercase as alphabet


class SoundcloudSpider(Spider):
    name = 'soundcloudspider'

    # Request strings.
    allowed_domains = ['soundcloud.com']
    host = 'https://api-v2.soundcloud.com'
    sc_a_id = '&sc_a_id=92b125e2-ac6b-4d2f-b8a7-0e643f955e37'
    variant_ids = '&variant_ids='
    user_id = '&user_id=932640-392717-44388-893092'
    client_id = '&client_id=QoSeELR4smhYFoJcsrWJ9N6wgQmoo1Yk'
    linked = '&linked_partitioning=1'
    app_version = '&app_version=1521644633'
    app_locale = '&app_locale=en'

    # Graph API initialising.
    token = 'EAAEeg8KsqegBANZCAoVql0BvIPFf1Smd7Vr0TscfC8iOWT4bCI6ZCwQYGpiQgZCZA4XrYnGEf09McyxF5emqyKIWvox5DKVy' \
            'fdSZBdtyZCzKN733W9FF4Si9cpxPoyahQzmisahYvL292YZCEbOJZBTiquHbHkQv1gPMqtZAEknyAVQZDZD'
    graph = facebook.GraphAPI(access_token=token)


    def __init__(self, type='', query='', time='', location='', limit='200', offset='0', *args, **kwargs):
        super(SoundcloudSpider, self).__init__(*args, **kwargs)
        self.search_url = []
        if type == 'full-search':
            with open('towns.csv') as csvfile:
                file = csv.reader(csvfile)
                towns = [row[1].lower() for row in file]
            print "-" * 15 + "Creating starting URLS" + "-" * 15
            for town in towns:
                for letter in alphabet:
                    # Construct url for each search and append to search_url list.
                    q = '/search/users?q={!s}'.format(letter)
                    if len(time) == 0:
                        filter_time = ''
                    else:
                        filter_time = '&filter.created_at={!s}'.format(time)
                    filter_loc = '&filter.place={!s}&facet=place'.format(town)
                    lim = '&limit={!s}&offset={!s}'.format(limit, offset)
                    url = self.host + q + self.sc_a_id + self.variant_ids + filter_time + filter_loc + self.user_id + \
                              self.client_id + lim + self.linked + self.app_version + self.app_locale
                    self.search_url.append(url)
        else:
            q = '/search/users?q={!s}'.format(query)
            if len(time) == 0:
                filter_time = ''
            else:
                filter_time = '&filter.created_at={!s}'.format(time)
            if len(location) == 0:
                filter_loc = '&facet=place'
            else:
                filter_loc = '&filter.place={!s}&facet=place'.format(location)
            lim = '&limit={!s}&offset={!s}'.format(limit, offset)
            url = self.host + q + self.sc_a_id + self.variant_ids + filter_time + filter_loc + self.user_id + \
                              self.client_id + lim + self.linked + self.app_version + self.app_locale
            self.search_url.append(url)

    def start_requests(self):
        for url in self.search_url:
            yield Request(url, callback=self.search_parse)


    def search_parse(self, response):
        data = json.loads(response.body_as_unicode())
        next_href = data.get('next_href')
        for item in data.get('collection', []):
            if item.get('track_count') != 0:
                artist = SoundcloudArtistItem()
                artist['city'] = item.get('city')
                artist['comments_count'] = item.get('comments_count')
                artist['country_code'] = item.get('country_code')
                artist['created_at'] = item.get('created_at')
                artist['description'] = item.get('description')
                artist['followers_count'] = item.get('followers_count')
                artist['followings_count'] = item.get('followings_count')
                artist['first_name'] = item.get('first_name')
                artist['sc_id'] = item.get('id')
                artist['last_modified'] = item.get('last_modified')
                artist['last_name'] = item.get('last_name')
                artist['likes_count'] = item.get('likes_count')
                artist['permalink'] = item.get('permalink')
                artist['permalink_url'] = item.get('permalink_url')
                artist['track_count'] = item.get('track_count')
                artist['uri'] = item.get('uri')
                artist['urn'] = item.get('urn')
                artist['username'] = item.get('username')
                yield artist

                # Web-profiles request from urn + /web-profiles.
                web_profile_url = self.host + '/users/' + item.get('urn') + '/web-profiles?' +self.client_id + \
                                  self.app_version + self.app_locale
                web_request = Request(web_profile_url, callback=self.web_profile_parse)
                web_request.meta['sc_id'] = item.get('id')
                yield web_request

                # Tracks request from id + /tracks.
                tracks_url = self.host + '/users/' + str(item.get('id')) + '/tracks?representation=' + self.client_id + \
                             '&limit=20&offset=0' + self.linked + self.app_version + self.app_locale
                tracks_request = Request(tracks_url, callback=self.tracks_parse)
                tracks_request.meta['sc_id'] = item.get('id')
                yield tracks_request

        if next_href:
            next_request = next_href + self.next_tail
            yield Request(next_request, self.search_parse)


    def web_profile_parse(self, response):
        sc_id = response.meta['sc_id']
        data = json.loads(response.body_as_unicode())
        for item in data:
            wprofile = SoundcloudWebProfileItem()
            wprofile['sc_id'] = sc_id
            wprofile['url'] = item.get('url')
            wprofile['network'] = item.get('network')
            wprofile['title'] = item.get('title')
            wprofile['username'] = item.get('username')
            yield wprofile

            if item['network'] == 'facebook':
                fields = ['genre', 'record_label', 'current_location']
                page = self.graph.request(item.get('username'))
                page_id = page['id']
                profile = self.graph.get_object(id=page_id, fields='genre, record_label, current_location')
                facebook = FacebookProfileItem()
                facebook['fb_id'] = str(profile['id'])
                facebook['sc_id'] = sc_id
                for field in fields:
                    try:
                        if profile[field]:
                            facebook[field] = profile[field]
                    except KeyError:
                        facebook[field] = None
                yield facebook



    def tracks_parse(self, response):
        # Limited to last 20 tracks
        sc_id = response.meta['sc_id']
        data = json.loads(response.body_as_unicode())
        for item in data.get('collection', []):
            if item.get('kind') == 'track':
                # Track details
                track = SoundcloudTrackItem()
                track['comment_count'] = item.get('comment_count')
                track['created_at'] = item.get('created_at')
                track['description'] = item.get('description')
                track['download_count'] = item.get('download_count')
                track['duration'] = item.get('duration')
                track['genre'] = item.get('genre')
                track['tr_id'] = item.get('id')
                track['label_name'] = item.get('label_name')
                track['likes_count'] = item.get('likes_count')
                track['playback_count'] = item.get('playback_count')
                track['release_date'] = item.get('release_date')
                track['repost_count'] = item.get('repost_count')
                track['tag_list'] = item.get('tag_list')
                track['title'] = item.get('title')
                track['sc_id'] = sc_id

                # Tracks publisher meta details
                meta = item.get('publisher_metadata')
                track['album_title'] = meta.get('album_title')
                track['contains_music'] = meta.get('contains_music')
                track['upc_or_ean'] = meta.get('upc_or_ean')
                track['isrc'] = meta.get('isrc')
                track['explicit'] = meta.get('explicit')
                track['writer_composer'] = meta.get('writer_composer', '')
                track['c_line'] = meta.get('c_line')
                yield track