#coding:utf-8


import tornado
import tornado.autoreload
import tornado.ioloop
import tornado.web

from conf import settings
import urls


application = tornado.web.Application(urls.patterns, **settings)


if __name__ == "__main__":
    application.listen(8888)
    ioloop = tornado.ioloop.IOLoop.instance()

    tornado.autoreload.start(ioloop)
    ioloop.start()
