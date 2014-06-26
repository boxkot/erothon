# coding:utf-8

import sys

class redirect(object):
    def redirect(self, url):
        sys.stdout = sys.__stdout__
        print 'Location: %s\n' % url
