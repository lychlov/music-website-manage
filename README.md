## 基于Django的简易音乐管理网站


### 运行环境
- Python3(3.7)
- Mysql8.0

```
在确保计算机环境已经安装好环境后执行：
    pip3 install -r requirements.txt
```

### 配置数据库
- 在 music/setting.py 中配置数据库连接参数
```
DATABASES = {...}
```
- 在MySQL数据库中创建 music_manage 库
```
create database music charset=utf8mb4;
```

### Django项目初始化
- 创建超级管理员账户， 此账户用于admin管理系统的使用
    ```
    python manage.py createsuperuser
    ```
- 数据迁移
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

### Scrapy数据抓取
使用Scrapy爬取网易云音乐网站歌曲信息，获取歌曲名称、歌手、专辑等信息，下载封面图片和音乐源文件到本地磁盘。
爬虫直接使用Django ORM模块入库，爬取信息直接写入MySQL数据库。
爬虫直接下载歌曲封面图片、音乐mp3文件存入Django项目static目录，可被网站直接使用。

- 运行爬虫
    ```
    python runner_one.py
    ```

### 启动网站
- 运行Django项目
    ```
    python manage.py runserver
    ```



