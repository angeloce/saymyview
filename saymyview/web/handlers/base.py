#coding:utf-8

from tornado.web import RequestHandler as BaseRequestHandler
from jinja2 import FileSystemLoader, Environment

from saymyview.web.conf import convention
from saymyview.web.models import User, Session

from saymyview.utils import date


class RequestHandler(BaseRequestHandler):
    template_env = None

    def __init__(self, application, request, **kwargs):
        BaseRequestHandler.__init__(self, application, request, **kwargs)
        self.db = application.database

        if not self.template_env:
            self.template_env = Environment(loader=FileSystemLoader(convention.template_path))

        session_id = self.get_cookie('session_id', None)
        self.session = None
        if session_id:
            self.session = Session.get_session(session_id)

    def finish(self, chunk=None):
        if self.session and self.session.session_id != self.get_cookie('SESSIONID'):
            self.set_cookie('SESSIONID', self.session.session_id)
        return super(RequestHandler, self).finish(chunk)

    def create_user_session(self, user):
        session_id = self._create_session_id(user.username+':'+user.password)
        session = Session(session_id=session_id, expires=date.now() + date.timedelta(7)).insert()
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
            user_name = self.session.get('user')
            if user_name:
                user = User.select().filter_by(username=user_name).first()
                if not user:
                    self.session.set(user=None)
