# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup
from cloudmuiscSpider.items import CloudmuiscItem
from utils.tools import headers
from utils.tools import headers


class CloudmusicSpider(scrapy.Spider):
    name = 'cloudmusic'
    allowed_domains = ['163.com']
    base_url = 'https://music.163.com'
    download_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'

    def start_requests(self):
        yield scrapy.Request(url='https://music.163.com/discover/playlist/', callback=self.parse, headers=headers)

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        play_lists = soup.find('ul', attrs={'id': 'm-pl-container'}).find_all('li')
        for p in play_lists[:10]:
            target_url = p.find('a', class_='msk').get('href')
            yield scrapy.Request(url=self.base_url + target_url, callback=self.parse_playlist, headers=headers)
            # break
        next_button = soup.find('a', class_='znxt')
        if 'js-disabled' not in next_button.get('class'):
            yield scrapy.Request(url=self.base_url + next_button.get('href'), callback=self.parse, headers=headers)

    def parse_playlist(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        songs = soup.find('ul', class_='f-hide').find_all('a')
        for s in songs:
            yield scrapy.Request(url=self.base_url + s.get('href'), callback=self.parse_song, headers=headers)
            # break

    def parse_song(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        item = CloudmuiscItem()
        item['song_id'] = int(soup.find('a', attrs={'data-res-action': 'play'}).get('data-res-id'))
        item['song_title'] = soup.find('div', class_='tit').text.strip()
        item['song_artist'] = soup.find('p', class_='des').find('span').get('title')
        item['song_artist_id'] = int(''.join(filter(str.isdigit, soup.find('p', class_='des').find('a').get('href'))))
        item['song_img'] = soup.find('img', class_='j-img').get('data-src')
        item['song_album'] = soup.find('a', attrs={'href': re.compile(r'^/album')}).text.strip()
        item['song_album_id'] = int(''.join(filter(str.isdigit, soup.find('a', attrs={'href': re.compile(r'^/album')}).get('href'))))
        item['song_file_path'] = '{}.mp3'.format(item['song_id'])
        item['song_img_file_path'] = '{}.jpeg'.format(item['song_id'])

        item['song_download_url'] = self.download_url.format(str(item['song_id']))
        yield item

        # yield scrapy.Request(url=item['song_download_url'], callback=self.parse_download, headers=headers, meta={'item': item})

    # def parse_download(self, response):
    #     item = response.meta['item']
    #     item['song_download_url'] = response.url
