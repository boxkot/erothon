#!/usr/bin/env python
# coding:utf-8

import re
import os
import sys
import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) )

from modules.HttpClient import HttpClient
from modules.ORM import ORM


http     = HttpClient()
db       = ORM('./sqlite/movie.db')
body     = http.setUrl(sys.argv[1]).sendGet()
movie_id = sys.argv[2]
now      = datetime.datetime.today()
now      = now.strftime("%Y-%m-%d %H:%M:%S")

try:
    re.search('id=\"pagetitle\"', body).group(1)
except:
    try:
        title = re.search('id=\"video_title\">(.+?)</h2>', body).group(1)
        data  = db.select().table('movie').where({'id = ' : movie_id}).fetchAll()
        #まともな抜き出しからわからぬ
        for value in data:
            old_title = value['title']
        if title == old_title:
            raise error('error')
    except:
        exit()


db.delete('movie')             \
  .where({'id = ' : movie_id}) \
  .deleteExe()
