#!/usr/bin/python
# coding:utf-8

import os
import math

class index(object):
    def construct(self):
        self.db = self.helper.readHelper('load').load('models_movie')

    def index(self):
        load = self.helper.readHelper('load')
        db   = load.load('models_movie')

    def list(self):
        data      = {'page' : 1, 'active' : 0}
        reqUri    = '?'
        req       = self.helper.readHelper('request')
        if req.isPost():
            temp = req.getPost()
        elif req.isGet():
            temp = req.getGet()

        for key, value in temp.items():
            data[key] = value

        if req.isRequest():
            for key, value in data.items():
                if key == 'page':
                    continue
                reqUri += '%s=%s&' % (key, value)

        result  = self.db.getSearch(data, {'id' : 'ASC'})
        pageNum = float(self.db.getCount(data))
        pageNum = int(math.ceil((pageNum / 20))) + 1

        self.view.data    = result
        self.view.reqUri  = reqUri
        self.view.pageNum = pageNum

    def movie_update(self):
        self.viewRender = False
        req             = self.helper.readHelper('request')
        redirect        = self.helper.readHelper('redirect')
        if not req.isPost():
            redirect.redirect('./../list/')

        favorite = req.getParam('favorite[]', [])
        update   = req.getParam('update[]', [])
        dust     = req.getParam('dust[]', [])

        for value in favorite:
            if self.db.getRow(int(value))['favorite'] == 0:
                self.db.updateById({'favorite' : 1}, int(value))
            else:
                self.db.updateById({'favorite' : 0}, int(value))

        for value in dust:
            self.db.updateById({'active' : 1}, int(value))

        for value in update:
            url = self.db.getRow((int(value)))['link']
            os.system('python ./_cli/update.py %s %s' % (url, value))

        redirect.redirect('./')
