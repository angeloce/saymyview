#coding:utf-8


from saymyview.web.handlers.base import RequestHandler
from saymyview.web.models import User


class IndexHandler(RequestHandler):

    def get(self):
        self.render('index.html')


class LoginHandler(RequestHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('u', '')
        password = self.get_argument('p', '')

        if username:
            user = User.query.filter_by(username=username).first()
            if user and user.is_same_password(password):
                self.set_current_user(user)
                return self.redirect('/')

        # login error
        self.render('login.html', error_message=u"用户名或密码错误", username=username, password=password)


class LogoutHandler(RequestHandler):

    def get(self):
        self.set_current_user(None)
        self.redirect('/')

    post = get



