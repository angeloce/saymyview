#coding:utf-8

import os
import sys

import tornado
import tornado.autoreload
import tornado.ioloop
import tornado.web

from painter.conf import settings
from painter import urls

class Application(object):

    def __init__(self):
        self.application = tornado.web.Application(urls.patterns, **settings)

    def run(self):
        self.application.listen(8888)
        ioloop = tornado.ioloop.IOLoop.instance()

        tornado.autoreload.start(ioloop)
        ioloop.start()



if __name__ == "__main__":
    main()
