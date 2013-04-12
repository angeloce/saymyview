#coding:utf-8


import tornado
import tornado.autoreload
import tornado.ioloop
import tornado.web

from saymyview.web.conf import settings
from saymyview.web import urls
from saymyview.web.models.base import database

application = tornado.web.Application(urls.patterns, **settings)
application.database = database

if __name__ == "__main__":
    application.listen(8888)
    ioloop = tornado.ioloop.IOLoop.instance()

    tornado.autoreload.start(ioloop)
    ioloop.start()
