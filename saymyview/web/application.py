#coding:utf-8


import tornado
import tornado.web

from saymyview.web.conf import settings
from saymyview.web import urls
from saymyview.web.models.base import DataBase


application = tornado.web.Application(urls.patterns, **settings)
application.database = DataBase(settings)


