#coding:utf-8

import json
from base import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Text


def _make_password(username, password):
    import hashlib
    sh1 = hashlib.sha1(password)
    sh1.update('saymyview')
    sh2 = hashlib.sha256(sh1.hexdigest())
    sh2.update(username)
    return sh2.hexdigest()


class User(BaseModel):
    __tablename__ = 'user'

    username = Column(String(20))
    nickname = Column(String(20))
    password = Column(String(128))
    wherefrom = Column(Integer)

    def is_same_password(self, raw_password):
        return _make_password(self.username, raw_password) == self.password

    def set_password(self, raw_password):
        self.password = _make_password(self.username, raw_password)

    def update_password(self, oldpwd, newpwd):
        if self.is_same_password(oldpwd):
            self.set_password(newpwd)

    def __str__(self):
        return self.username or ""


class WebPage(BaseModel):
    __tablename__ = "web_page"

    url = Column(String(255))
    update_date = Column(DateTime)
    create_date = Column(DateTime)


class WebPageScript(BaseModel):
    __tablename__ = "web_page_script"

    url = Column(String(255))
    script = Column(Text)
    update_date = Column(DateTime)


class RequestSession(BaseModel):
    __tablename__ = "request_session"

    session_id = Column(String(32))
    session_data = Column(Text)
    expires = Column(DateTime)

    @property
    def session_obj(self):
        if hasattr(self, '_session_obj'):
            try:
                self._session_obj = json.loads(self.session_data)
            except Exception, e:
                self._session_obj = {}
        return self._session_obj

    def get(self, name, default=None):
        return self.session_obj.get(name, default)

    def set(self, name, value):
        if value is None:
            del self.session_obj[name]
        else:
            self.session_obj[name] = value

    def save(self):
        self.session_data = json.dumps(self.session_obj)
        self.save()

