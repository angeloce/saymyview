#coding:utf-8

try:
    import saymyview
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


import sys
import tornado.ioloop
import tornado.autoreload
from application import application

if __name__ == '__main__':
    try:
        port = int(sys.path[1])
    except:
        port = 8000
    
    application.listen(port)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()
