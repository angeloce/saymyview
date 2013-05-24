#coding:utf-8


import tornado
import tornado.web

from saymyview.datamodel.base import DataBase

from saymyview.web.conf import settings
from saymyview.web import urls


application = tornado.web.Application(urls.patterns, **settings)
application.database = DataBase(settings)


