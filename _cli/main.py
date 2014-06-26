#!/usr/bin/env python
# coding:utf-8

import re
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) )

from modules.HttpClient import HttpClient
from modules.ORM import ORM

http      = HttpClient()
db        = ORM('./sqlite/movie.db')
failCount = 0

url    = 'http://video.fc2.com/ja/a/movie_search.php'

params = {'keyword'   : sys.argv[1],
          'timestart' : int(sys.argv[2]),
          'timeend'   : int(sys.argv[3]),
          'test'      : '',
          'timemin'   : sys.argv[4],
          'perpage'   : int(sys.argv[5]),
          'usertime'  : int(sys.argv[6])}

for i in xrange(int(sys.argv[7]), int(sys.argv[8]) + 1):
    params['page'] = i
    body           = http.setData(params).setUrl(url).sendGet()
    body           = re.findall('<div class=\"video_list_renew clearfix\">([\s\S]+?)<\!--/video_list', body)

    #失敗多かったらぶれーく
    if failCount == 10:
        break

    for text in body:
        try:
            statusText = re.search('<ul class=\"video_info_upper_renew clearfix\">([\s\S]+?)</ul>', text).group(1)
            status     = re.search('<li class=\"member_icon.*?>(.*?)</li>', statusText).group(1)
            viewNum    = re.search('再生数[\s\S]*?>(.+?)</li>', statusText).group(1)
            albumNum   = re.search('アルバム追加数[\s\S]*?>(.+?)</li>', statusText).group(1)
            commentNum = re.search('コメント数[\s\S]*?>.*>(.+?)</a>', statusText).group(1)

            img        = re.search('<div class=\"video_thumb_small[\s\S]*?<img src=\"(.+?)\"', text).group(1)
            title      = re.search('<h3>[\s\S]*?title=\"(.*?)\"', text).group(1)
            link       = re.search('<h3>[\s\S]*?<a href=\"(.*?)\"', text).group(1)
            userName   = re.search('<p class=\"user_name\">([\s\S]*?)</p>', text).group(1)
        except:
            failCount += 1
            continue

        try:
            comment    = re.search('<p class=\"comments\">([\s\S]*?)</p>', text).group(1)
        except:
            comment = ''

        data = {'keyword'     : params['keyword'],
                'title'       : title,
                'status'      : status,
                'view_num'    : viewNum,
                'album_num'   : albumNum,
                'comment_num' : commentNum,
                'comment'     : comment,
                'user_name'   : userName,
                'link'        : link,
                'image_link'  : img}

        db.select().table('movie').where({'title =' : data['title']})
        num = db.fetchOne()
        if num is None:
            db.insert('movie', data)
