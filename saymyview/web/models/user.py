#coding:utf-8


from saymyview.datamodel.user import UserModel


class User(object):

    @classmethod
    def create_user(cls, username, password):
        return UserModel(username=username, password=password).insert()

    @classmethod
    def get_user_by_name(cls, username):
        return UserModel.select().filter_by(username=username).one()

    @classmethod
    def login(cls, username, password):
        if username:
            user = cls.get_user_by_name(username)
            if user and user.check_password(password):
                return user

