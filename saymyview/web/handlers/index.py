#coding:utf-8


from saymyview.web.handlers.base import RequestHandler
from saymyview.datamodel.user import User
from saymyview.datamodel.weburl import WebUrl

class IndexHandler(RequestHandler):

    def get(self):

        weburls = WebUrl.select().all()[:10]

        self.render('index.html', weburls=weburls)


class LoginHandler(RequestHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('u', '')
        password = self.get_argument('p', '')
        if username:
            user = User.select().filter_by(username=username).first()
            if user and user.check_password(password):
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



