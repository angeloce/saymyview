#coding:utf-8

from painter.utils.db import Document
from painter.utils.date import now, strnow

class User(Document):
    _default_db = 'user'
    
    # fields: username, password, registered

    def create(self, username, password=''):
        return self.insert(username=username, registered=now())
