#coding:utf-8


from saymyview.datamodel.user import UserModel

from _base import Model


class User(Model):

    def create_user(self, username, password):
        return UserModel(username=username, password=password).insert()

    def get_user_by_name(self, username):
        return UserModel.select().filter_by(username=username).one()

    def login(self, username, password):
        if username:
            user = self.get_user_by_name(username)
            if user and user.check_password(password):
                return user

