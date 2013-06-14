#coding:utf-8


from saymyview.web.handlers.base import RequestHandler
from saymyview.web.models.user import User
from saymyview.web.models.weburl import WebUrl

class IndexHandler(RequestHandler):

    def get(self):
        weburls = WebUrl.get_urls(end=10)
        self.render('index.html', weburls=weburls)


class LoginHandler(RequestHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('u', None)
        password = self.get_argument('p', '')
        user = User.login(username, password)
        if user:
            session = self.create_user_session(user)
            session.set(user=username)
            return self.redirect('/')

        # login error
        self.render('login.html', error_message=u"用户名或密码错误", username=username, password=password)


class LogoutHandler(RequestHandler):

    def get(self):
        if self.session:
            self.session.delete()
        self.redirect('/')

    post = get



