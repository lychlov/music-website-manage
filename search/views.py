from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from index.models import Song, Dynamic


def searchView(request, page):
    # 热搜歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:4]
    # 获取搜索内容，如果kword为空即查询全部歌曲
    kword = request.POST.get('kword', '')
    if kword:
        # Q是SQL语句里的or语法
        song_info = Song.objects.values('song_id', 'song_title', 'song_artist', 'song_album').filter(
            Q(song_title__icontains=kword) | Q(song_artist=kword)).all()
    else:
        song_info = Song.objects.values('song_id', 'song_title', 'song_artist', 'song_album').all()
    # 分页功能
    paginator = Paginator(song_info, 20)
    try:
        contacts = paginator.get_page(page)
        print(contacts)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    # 添加歌曲搜索次数
    song_exist = Song.objects.filter(song_title=kword)
    if song_exist:
        song_id = song_exist[0].song_id
        dynamic_info = Dynamic.objects.filter(song_id=int(song_id)).first()
        # 判断歌曲动态信息是否存在，存在就在原来基础上加1
        if dynamic_info:
            dynamic_info.dynamic_search += 1
            dynamic_info.save()
        # 动态信息不存在则创建新的动态信息
        else:
            dynamic = Dynamic(dynamic_plays=0, dynamic_search=1, dynamic_down=0, song_id=song_id)
            dynamic.save()
    return render(request, 'search.html', locals())
