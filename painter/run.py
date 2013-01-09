#coding:utf-8

import os
import sys


import tornado.ioloop
import tornado.web
from settings import ApplicationSettings
import urls

sys.path.append('.')

def main():
    settings = dict([(k, v) for k, v in ApplicationSettings.__dict__.items() if not k.startswith('__')])
    application = tornado.web.Application(urls.patterns, **settings)
    
    application.listen(8888)
    ioloop = tornado.ioloop.IOLoop.instance()

    from tornado import autoreload
    autoreload.start(ioloop)

    ioloop.start()



if __name__ == "__main__":
    main()
