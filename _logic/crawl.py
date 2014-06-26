#!/usr/bin/python
# coding:utf-8

import os

class crawl(object):
    def construct(self):
        pass

    def index(self):
        req    = self.helper.readHelper('request')
        result = ''

        if req.isPost():
            keyword = req.getParam('keyword', '')
            start   = req.getParam('start', 1)
            end     = req.getParam('end', 1)
            os.system('python ./_cli/main.py %s 0 0 分 20 0 %s %s' % (keyword, start, end))
            result = '実行が終了しましたが正常実行かわからなす'
        self.view.result = result

    def all_update(self):
        req    = self.helper.readHelper('request')
        db     = self.helper.readHelper('load').load('models_movie')
        result = ''
        if req.isPost():
            data = db.getSearch({'active' : 0})
            for row in data:
                url = row['link']
                os.system('python ./_cli/update.py %s %s' % (url, row['id']))
            result = 'とりあえず処理が終わった'

        self.view.result = result
