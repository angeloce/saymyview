#coding:utf-8


from saymyview.web.handlers.base import RequestHandler


class IndexHandler(RequestHandler):

    def get(self):
        x = 2

        self.render('index.html', x=2)
