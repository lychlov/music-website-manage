from urllib.parse import quote

from django.shortcuts import render
from django.http import StreamingHttpResponse
from index.models import *


# 歌曲播放页面
def playView(request, song_id):
    # 热搜歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:4]
    # 歌曲信息
    song_info = Song.objects.get(song_id=int(song_id))
    # 播放列表
    play_list = request.session.get('play_list', [])
    song_exist = False
    if play_list:
        for i in play_list:
            if int(song_id) == i['song_id']:
                song_exist = True
    if song_exist == False:
        play_list.append(
            {'song_id': int(song_id), 'song_artist': song_info.song_artist, 'song_title': song_info.song_title})
    request.session['play_list'] = play_list
    # 歌词
    # if song_info.song_lyrics != '暂无歌词':
    #     f = open('/static/songLyric/' + song_info.song_lyrics, 'r', encoding='utf-8')
    #     song_lyrics = f.read()
    #     f.close()

    # 相关歌曲
    song_artist = Song.objects.values('song_artist').get(song_id=song_id)['song_artist']
    song_relevant = Dynamic.objects.select_related('song').filter(song__song_artist=song_artist).order_by(
        '-dynamic_plays').all()[:6]
    print(song_relevant)
    # 添加播放次数
    # 扩展功能：可使用session实现每天只添加一次播放次数
    dynamic_info = Dynamic.objects.filter(song_id=int(song_id)).first()
    # 判断歌曲动态信息是否存在，存在就在原来基础上加1
    if dynamic_info:
        dynamic_info.dynamic_plays += 1
        dynamic_info.save()
    # 动态信息不存在则创建新的动态信息
    else:
        dynamic_info = Dynamic(dynamic_plays=1, dynamic_search=0, dynamic_down=0, song_id=song_id)
        dynamic_info.save()
    response = render(request, 'play.html', locals())

    return response


# 歌曲下载
def downloadView(request, song_id):
    # 根据song_id查找歌曲信息
    song_info = Song.objects.get(song_id=int(song_id))
    print(song_id)
    # 添加下载次数
    dynamic_info = Dynamic.objects.filter(song=int(song_id)).first()
    # 判断歌曲动态信息是否存在，存在就在原来基础上加1
    if dynamic_info:
        dynamic_info.dynamic_down += 1
        dynamic_info.save()
    # 动态信息不存在则创建新的动态信息
    else:
        dynamic_info = Dynamic(dynamic_plays=0, dynamic_search=0, dynamic_down=1, song_id=song_id)
        dynamic_info.save()
    # 读取文件内容
    file = 'static/songFile/' + song_info.song_file_path

    def file_iterator(file, chunk_size=512):
        with open(file, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    # 将文件内容写入StreamingHttpResponse对象，并以字节流方式返回给用户，实现文件下载
    filename = song_info.song_title + '.mp3'
    print(filename)
    response = StreamingHttpResponse(file_iterator(file))
    response['Content-Type'] = 'application/octet-stream'
    # response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    response['Content-Disposition'] = 'attachment; {}'.format("filename*=utf-8''{}".format(quote(filename)))  # quote确保中文格式不乱码
    print(response['Content-Disposition'])
    return response
