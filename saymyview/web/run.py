#coding:utf-8

try:
    import saymyview
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


import tornado.ioloop
import tornado.autoreload
from application import application

if __name__ == '__main__':
    application.listen(8888)
    ioloop = tornado.ioloop.IOLoop.instance()

    tornado.autoreload.start(ioloop)
    ioloop.start()
