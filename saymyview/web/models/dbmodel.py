#coding:utf-8

from base import database
from sqlalchemy import Column, Integer, String, DateTime, Text



def _make_password(username, password):
    import hashlib
    sh1 = hashlib.sha1(password)
    sh1.update('saymyview')
    sh2 = hashlib.sha256(sh1.hexdigest())
    sh2.update(username)
    return sh2.hexdigest()


class User(database.Model):
    __tablename__ = 'user'

    username = Column(String(20))
    nickname = Column(String(20))
    password = Column(String(128))
    wherefrom = Column(Integer)

    def __init__(self, account, password):
        self.username = account
        self.nickname = account
        self.set_password(password)

    def is_same_password(self, raw_password):
        return _make_password(self.username, raw_password) == self.password

    def set_password(self, raw_password):
        self.password = _make_password(self.username, raw_password)

    def update_password(self, oldpwd, newpwd):
        if self.is_same_password(oldpwd):
            self.set_password(newpwd)

    def __str__(self):
        return self.username or ""


class WebPage(database.Model):
    __tablename__ = "web_page"

    url = Column(String(255))
    update_date = Column(DateTime)
    create_date = Column(DateTime)


class WebPageScript(database.Model):
    __tablename__ = "web_page_script"

    url = Column(String(255))
    script = Column(Text)
    update_date = Column(DateTime)
