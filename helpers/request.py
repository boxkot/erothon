# coding:utf-8

import os
import cgi

class request(object):
    def __init__(self):
        self.data = cgi.FieldStorage()

    def isGet(self):
        return os.environ['REQUEST_METHOD'] == 'GET'

    def isPost(self):
        return os.environ['REQUEST_METHOD'] == 'POST'

    def isRequest(self):
        return self.isGet() or self.isPost()

    def getPost(self):
        data = {}
        for key in self.data:
            temp = self.data[key]
            if isinstance(temp, list):
                temp = temp[0]
            data[key] = temp.value
        return data

    def getGet(self):
        data = {}
        for key in self.data:
            temp = self.data[key]
            if isinstance(temp, list):
                temp = temp[-1]
            data[key] = temp.value
        return data

    def getParam(self, name, default = None):
        data   = None
        toList = False
        if not default == None:
            data = default

        if self.data.has_key(name):
            if name[-2:] == '[]':
                data = self._toList(self.data[name])
            else:
                data = self.data[name].value
        return data

    def _toList(self, data):
        result = []
        if isinstance(data, list):
            for value in data:
                result.append(value.value)
        else:
            result.append(data.value)
        return result
