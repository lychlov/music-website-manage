import django
import sys

import os

# sys.path.insert(0, 'D:/PycharmProjects/crawler_admin_site/')
os.environ["DJANGO_SETTINGS_MODULE"] = "music.settings"
django.setup()

from index import models


def save_song(item):
    try:
        song_info = models.Song(song_id=item['song_id'],
                                song_title=item['song_title'],
                                song_artist=item['song_artist'],
                                song_artist_id=item['song_artist_id'],
                                song_album=item['song_album'],
                                song_album_id=item['song_album_id'],
                                song_img=item['song_img'],
                                song_img_file_path=item['song_img_file_path'],
                                song_download_url=item['song_download_url'],
                                song_file_path=item['song_file_path']
                                )
    except Exception as e:
        print(e)
        return False
    try:
        if models.Song.objects.get(song_id=item['song_id']):
            return False
    except:
        pass
    song_info.save()
    print("成功爬取歌曲：%s" % song_info.song_id)
    return True


def get_one_song_without_lyrics():
    try:
        result = models.Song.objects.filter(song_lyrics='')
        return result
    except:
        return None


def save_lyrics(song_id, lyrics):
    song = models.Song.objects.get(song_id=song_id)
    song.song_lyrics = lyrics
    song.save()
    pass
