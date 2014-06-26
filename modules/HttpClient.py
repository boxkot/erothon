import urllib
import urllib2

class HttpClient(object):

    url      = ''
    sendData = {}

    def __init__(self):
        pass

    def setUrl(self, url):
        self.url = url
        return self

    def setData(self, data):
        for key, value in data.items():
            self.sendData[key] = value
        return self

    def getData(self):
        return self.sendData

    def resetData(self, data = {}):
        if len(data) == 0:
            self.sendData.clear()
        else:
            for key, value in data.items():
                if self.sendData.has_key(key):
                    del self.sendData[key]
                else:
                    raise sendDataKeyNouFound(str(key) + 'is not has key')
        return self

    def sendPost(self):
        req    = urllib2.Request(self.url)
        params = urllib.urlencode(self.getData())

        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        req.add_data(params)
        res = urllib2.urlopen(req)

        return res.read()

    def sendGet(self):
        params = urllib.urlencode(self.getData())
        res    = urllib2.urlopen(self.url + '?' + params)

        return res.read()
