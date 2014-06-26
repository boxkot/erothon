#!/usr/bin/python
# coding:utf-8

from modules.ORM import ORM

class movie(object):
    def __init__(self):
        self.db = ORM('./sqlite/movie.db')

    def getAll(self):
        self.db.select().table('movie')
        return self.db.fetchAll()

    def getRow(self, movie_id):
        self.db.select().table('movie').where({'id = ' : movie_id})
        return self.db.fetchAll()[0]

    def getSearch(self, data, order = {}):
        self.db.select().table('movie')

        if data.has_key('keyword'):
            self.db.where({'keyword = ' : data['keyword']})
        if data.has_key('title'):
            self.db.where({'title like ' : '%' + data['title'] + '%'})
        if data.has_key('status'):
            self.db.where({'status = ' : data['status']})
        if data.has_key('view_num'):
            self.db.where({'view_num > ' : int(data['view_num'])})
        if data.has_key('album_num'):
            self.db.where({'album_num > ' : int(data['album_num'])})
        if data.has_key('comment_num'):
            self.db.where({'comment_num > ' : int(data['comment_num'])})
        if data.has_key('comment'):
            self.db.where({'commetn like ' : data['comment']})
        if data.has_key('favorite'):
            self.db.where({'favorite = ' : int(data['favorite'])})
        if data.has_key('active'):
            self.db.where({'active = ' : int(data['active'])})


        if len(order) > 0:
            self.db.order(order)
        if data.has_key('page'):
            limit = (20, (int(data['page']) - 1) * 20)
            self.db.limit(limit)

        return self.db.fetchAll()

    def getCount(self, data):
        self.db.select([{'count(*)' : 'num'}]).table('movie')

        if data.has_key('keyword'):
            self.db.where({'keyword = ' : data['keyword']})
        if data.has_key('title'):
            self.db.where({'title like ' : '%' + data['title'] + '%'})
        if data.has_key('comment'):
            self.db.where({'commetn like ' : data['comment']})
        if data.has_key('view_num'):
            self.db.where({'view_num > ' : data['view_num']})
        if data.has_key('album_num'):
            self.db.where({'album_num > ' : data['album_num']})
        if data.has_key('comment_num'):
            self.db.where({'comment_num > ' : data['comment_num']})
        if data.has_key('favorite'):
            self.db.where({'favorite = ' : data['favorite']})
        if data.has_key('active'):
            self.db.where({'active = ' : data['active']})

        return self.db.fetchOne()[0]

    def updateById(self, data, movie_id):
        self.db.update('movie', data)       \
               .where({'id = ' : movie_id}) \

        return self.db.updateExe()
