#coding:utf-8

from tornado.web import RequestHandler as BaseRequestHandler
from jinja2 import FileSystemLoader, Environment

from saymyview.web.conf import convention
from saymyview.web.models.base import database
from saymyview.web.models.dbmodel import User

from saymyview.utils import date



class Session(object):

    def __init__(self, session_id, expires=None):
        self.session_id = session_id
        self.expires = expires
        self.content = {}

    def set(self, **kwargs):
        for k, v in kwargs.items():
            if v is None and k in self.content:
                del self.content[k]
                continue
            self.content[k] = v

    def get(self, key, default=None):
        return self.content.get(key, default)


class SessionManager(object):
    def __init__(self):
        self._d = {}

    def get(self, session_id):
        session = self._d.get(session_id)
        if session is None:
            return
        if session.expires:
            if session.expires > date.now():
                return session
            else:
                del self._d[session_id]

    def create_session(self, session_id, expires=None):
        self._d[session_id] = Session(session_id, expires)
        return self._d[session_id]

session_manager = SessionManager()


class RequestHandler(BaseRequestHandler):
    template_env = None

    def __init__(self, application, request, **kwargs):
        BaseRequestHandler.__init__(self, application, request, **kwargs)

        if not self.template_env:
            self.template_env = Environment(loader=FileSystemLoader(convention.template_path))

        session_id = self.get_cookie('session_id', None)
        self.session = None
        if session_id:
            self.session = session_manager.get(session_id)

        self.database = database

    def finish(self, chunk=None):
        if self.session and self.session.session_id != self.get_cookie('session_id'):
            self.set_cookie('session_id', self.session.session_id)
        return super(RequestHandler, self).finish(chunk)

    def create_session(self, htonl=None):
        session_id = self._create_session_id(htonl)
        session = session_manager.create_session(session_id)
        session.expires = date.now() + date.timedelta(7)
        self.session = session
        return session

    def _create_session_id(self, htonl=None):
        import hashlib
        sh1 = hashlib.sha1(self.request.remote_ip)
        sh1.update(date.strnow())
        if htonl:
            sh1.update(htonl)
        return sh1.hexdigest()

    def render_string(self, template_name, **kwargs):
        template = self.template_env.get_template(template_name)
        namespace = self.get_template_namespace()
        namespace.update(kwargs)
        return template.render(**namespace)

    def get_current_user(self):
        if self.session:
            user_name = self.session.get('u')
            if user_name:
                return User.query.filter_by(username=user_name).first()

    def set_current_user(self, user):
        if user:
            if not self.session:
                self.session = self.create_session(user.username)
                self.session.set(u=user.username)
        elif self.session:
            self.session.set(u=None)
        self._current_user = user
