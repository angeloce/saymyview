#coding:utf-8

from painter.utils.webutil import RequestHandler

class IndexHandler(RequestHandler):

    def get(self):
        self.render('base.html')
