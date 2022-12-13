# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup
from cloudmuiscSpider.items import CloudmuiscItem
from utils.tools import headers
from urllib.parse import urlencode, quote, unquote
import re
from utils.django_api import save_lyrics, get_one_song_without_lyrics


class LyricsSpider(scrapy.Spider):
    name = 'lyrics'
    allowed_domains = ['musicenc.com']
    base_url = 'https://www.musicenc.com/'

    def start_requests(self):
        songs = get_one_song_without_lyrics()
        for song in songs:
            target = self.base_url + '?search={}'
            name = song.song_title
            meta = {'id': song.song_id,
                    'artist': song.song_artist,
                    'name': name}
            yield scrapy.Request(url=target.format(quote(name)), callback=self.parse, headers=headers, meta=meta)
            song = get_one_song_without_lyrics()

    def parse(self, response):
        html = response.body
        meta = response.meta
        soup = BeautifulSoup(html, 'lxml')
        for i in soup.find_all('li'):
            try:
                artist = i.find('span').text
                name = i.find('a').text
            except:
                artist = ''
                name = '暂无'
            if meta.get('artist') in artist and (meta.get('name') in name or name in meta.get('name')):
                value = i.find('a').get('dates')
                target = 'https://www.musicenc.com/searchr/?token={}'
                return scrapy.Request(url=target.format(value), callback=self.parse_info, headers=headers, meta=meta)
        save_lyrics(meta.get('id'), '暂无歌词')

    def parse_info(self, response):
        html = response.body.decode()
        soup = BeautifulSoup(html, 'lxml')
        meta = response.meta
        contents = soup.find('div', class_='content').contents
        lyrics = ''
        for c in contents:
            if re.findall(r'\[\d+\:\d+\]', c.text):
                prefix = re.findall(r'\[\d+\:\d+\]', c.text)[0]
                lyrics += prefix + c.text.strip().replace(prefix, '') + '\n'
        print(lyrics)
        save_lyrics(meta.get('id'), lyrics)
