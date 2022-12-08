# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
import scrapy

from utils.django_api import save_song
from scrapy.pipelines.images import ImagesPipeline, FilesPipeline
from .settings import IMAGES_STORE as images_store
from utils.tools import headers


class MusicMongoPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient('localhost')
        self.db = self.client.get_database('163')
        self.collection = self.db.get_collection('music')
        self.collection_author = self.db.get_collection('song')

    def process_item(self, item, spider):
        result = self.collection_author.find_one_and_replace({"id": item['id']}, dict(item))
        if not result:
            insert_result = self.collection_author.insert_one(dict(item))
        return item


class MusicMysqlPipeline(object):
    def __init__(self):
        # connection database
        self.connect = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='music')  # 后面三个依次是数据库连接名、数据库密码、数据库名称
        # get cursor
        self.cursor = self.connect.cursor()
        print("连接数据库成功")

    def process_item(self, item, spider):
        # sql语句
        insert_sql = "insert into music.song (id, title, artist, artist_id, album, album_id, download_url) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (item['id'], item['title'], item['artist'], item['artist_id'],
                                         item['album'], item['album_id'], item['download_url']))
        # 提交，不进行提交无法保存到数据库
        self.connect.commit()
        return item

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.connect.close()


class MusicDjangoPipeline(object):
    def process_item(self, item, spider):
        # if save_song(item):
        #     return item
        save_song(item)
        return item


class MusicFilePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if None is item:
            return None
        image_url = item["song_download_url"]
        yield scrapy.Request(image_url, headers=headers, meta={'song_id': item['song_id'], 'song_title': item['song_title']})

    def file_path(self, request, response=None, info=None):
        filename = u'{}.mp3'.format(request.meta['song_id'])
        return filename


class MusicImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if None is item:
            return None
        image_url = item["song_img"]
        # 将图片地址提交下载器下载
        yield scrapy.Request(image_url, headers=headers, meta={'song_id': item['song_id'], 'song_title': item['song_title']})

    def file_path(self, request, response=None, info=None):
        # 图片文件名
        filename = u'{}.jpeg'.format(request.meta['song_id'])
        return filename
