#!/usr/bin/python
# coding:utf-8

import os
import os.path
import sys
import StringIO
import ConfigParser
import tenjin
from tenjin.helpers import *
from tenjin.html import *
from modules.View import View
from modules.Helper import Helper

#出力バッファを監視
output     = StringIO.StringIO()
sys.stdout = output

print 'Content-Type: text/html\n\n'

#config
conf = ConfigParser.SafeConfigParser()
conf.read('config.ini')
toBasePath   = conf.get('root', 'base')
toView       = conf.get('root', 'views')
toViewPath   = toBasePath + toView
toController = conf.get('root', 'controllers')


#基底パスに辿り着くまでのREQUEST URIの長さを計算
toBasePath = toBasePath.split('/')
if toBasePath[-1] == '':
    toBasePath = toBasePath[:-1]
toBaseLength = len(toBasePath)

#rooting
path = os.environ['REQUEST_URI'].split('/')
if path[-1] == '':
    path = path[:-1]

#Controller名をセット
if len(path) > toBaseLength:
    controller = path[toBaseLength]
else:
    controller = 'index'

#Action名をセット
if len(path) > toBaseLength + 1:
    action = path[toBaseLength + 1]
else:
    action = 'index'

engin     = tenjin.Engine()
viewPath  = './%s/%s/%s.html' % (toView, controller, action)
logicPath = '%s.%s' % (toController, controller)
#Not Found用HTMLを読み込み,処理終了
if not os.path.isfile('%s/%s.py' % (toController, controller)):
    body = engin.render('./%s/__error.html' % toView)
    print (body)
    exit()

#logicクラスの読み込み,オブジェクト生成
module        = __import__(logicPath)
module        = getattr(module, controller)
controllerObj = getattr(module, controller)()
#Not Found用HTMLを読み込み,処理終了
if not hasattr(controllerObj, action):
    body = engin.render('./%s/__error.html' % toView)
    print (body)
    exit()

#基本データをセット
controllerObj.view       = View()
controllerObj.viewRender = True
controllerObj.helper     = Helper()
controllerObj.config     = conf

#コンストラクタ実行
if hasattr(controllerObj, 'construct'):
    controllerObj.__getattribute__('construct')()

#Action実行
controllerObj.__getattribute__(action)()

#viewデータの抜き出し、htmlへデータを受け渡すための整形を行う
context = {'viewpath' : toViewPath}
for name in dir(controllerObj.view):
    if name[0] == '_':
        continue
    context[name] = getattr(controllerObj.view, name)

#バッファを吐き出して解放
sys.stdout = sys.__stdout__
print output.getvalue()
output.close()

#HTMLを描画
if controllerObj.viewRender:
    header = engin.render('./%s/__header.html' % toView, context)
    footer = engin.render('./%s/__footer.html' % toView, context)
    body   = engin.render(viewPath, context)
    print (header)
    print (body)
    print (footer)

