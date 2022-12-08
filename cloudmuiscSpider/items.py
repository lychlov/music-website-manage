# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CloudmuiscItem(scrapy.Item):
    # define the fields for your item here like:
    song_id = scrapy.Field()
    song_title = scrapy.Field()
    song_artist = scrapy.Field()
    song_artist_id = scrapy.Field()
    song_album = scrapy.Field()
    song_album_id = scrapy.Field()
    song_img = scrapy.Field()
    song_img_file_path = scrapy.Field()
    song_download_url = scrapy.Field()
    song_file_path = scrapy.Field()
    pass
