# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup
from cloudmuiscSpider.items import CloudmuiscItem
from utils.tools import headers


class CloudmusicSpider(scrapy.Spider):
    name = 'info'
    allowed_domains = ['163.com']
    base_url = 'https://music.163.com'
    download_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'

    def start_requests(self):
        target = 'http://music.163.com/song/media/outer/url?id=1859660047.mp3'
        yield scrapy.Request(url=target, callback=self.parse, headers=headers)

    def parse(self, response):
        html = response.body
        with open('p.mps','wb') as f:
            f.write(html)
            f.flush()
            f.close()

        soup = BeautifulSoup(html, 'lxml')
        play_lists = soup.find('ul', attrs={'id': 'm-pl-container'}).find_all('li')
        for p in play_lists:
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
        item['id'] = int(soup.find('a', attrs={'data-res-action': 'play'}).get('data-res-id'))
        item['title'] = soup.find('div', class_='tit').text.strip()
        item['artist'] = soup.find('p', class_='des').find('span').get('title')
        item['artist_id'] = int(''.join(filter(str.isdigit, soup.find('p', class_='des').find('a').get('href'))))
        item['album'] = soup.find('a', attrs={'href': re.compile(r'^/album')}).text.strip()
        item['album_id'] = int(''.join(filter(str.isdigit, soup.find('a', attrs={'href': re.compile(r'^/album')}).get('href'))))
        item['download_url'] = self.download_url.format(str(item['id']))
        yield item
