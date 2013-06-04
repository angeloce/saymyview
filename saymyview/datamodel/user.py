#coding:utf-8

from sqlalchemy.orm import validates

from saymyview.datamodel.base import BaseModel
from saymyview.datamodel.tables import user_table


def _make_password(username, password):
    import hashlib
    sh1 = hashlib.sha1(password)
    sh1.update('saymyview')
    sh2 = hashlib.sha256(sh1.hexdigest())
    sh2.update(username)
    return sh2.hexdigest()


class UserModel(BaseModel):
    __table__ = user_table

    def check_password(self, raw_password):
        return _make_password(self.username, raw_password) == self.password

    def update_password(self, oldpwd, newpwd):
        if self.is_same_password(oldpwd):
            self.password = newpwd

    @validates("password")
    def validate_password(self, key, value):
        return _make_password(self.username, value)

    @validates("username")
    def validate_name(self, key, value):
        if len(value) < 3 or len(value) > 30:
            raise
        return value

    def __str__(self):
        return self.username or ""

