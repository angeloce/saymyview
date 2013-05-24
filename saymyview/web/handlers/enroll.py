#coding:utf-8


from saymyview.web.handlers.base import RequestHandler
from saymyview.datamodel.user import User



class EnrollHandler(RequestHandler):

    def post(self):

        if not self.current_user:
            return

        self.get_argument('link', '')
