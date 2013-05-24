#coding:utf-8


from saymyview.web.models.base import BaseModel
from saymyview.web.models.tables import user_table


def _make_password(username, password):
    import hashlib
    sh1 = hashlib.sha1(password)
    sh1.update('saymyview')
    sh2 = hashlib.sha256(sh1.hexdigest())
    sh2.update(username)
    return sh2.hexdigest()



class User(BaseModel):
    __table__ = user_table

    def check_password(self, raw_password):
        return _make_password(self.username, raw_password) == self.password

    def set_password(self, raw_password):
        self.password = _make_password(self.username, raw_password)

    def update_password(self, oldpwd, newpwd):
        if self.is_same_password(oldpwd):
            self.set_password(newpwd)

    def __str__(self):
        return self.username or ""

