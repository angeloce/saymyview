#coding:utf-8


from base import BaseModel
from tables import *


def _make_password(username, password):
    import hashlib
    sh1 = hashlib.sha1(password)
    sh1.update('saymyview')
    sh2 = hashlib.sha256(sh1.hexdigest())
    sh2.update(username)
    return sh2.hexdigest()


class User(BaseModel):
    def check_password(self, username, user_password, check_password):

        result = self.execute(self.select(UserTable).where(UserTable.c.username == username))

        if result:
            pass

