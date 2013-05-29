#coding:utf-8

import json

from tornado.web import RequestHandler as BaseRequestHandler
from jinja2 import FileSystemLoader, Environment

from saymyview.web.conf import convention
from saymyview.datamodel.user import User
from saymyview.datamodel.session import Session

from saymyview.utils import date


class RequestHandler(BaseRequestHandler):
    template_env = None
    SESSIONID = "SESSIONID"

    def __init__(self, application, request, **kwargs):
        BaseRequestHandler.__init__(self, application, request, **kwargs)
        self.db = application.database

        if not self.template_env:
            self.template_env = Environment(loader=FileSystemLoader(convention.template_path))

        self.session = None
        session_id = self.get_cookie(self.SESSIONID)
        if session_id:
            self.session = Session.get_session(session_id)

    def finish(self, chunk=None):
        session_id = self.get_cookie(self.SESSIONID)
        if self.session and self.session.session_id != session_id:
            self.set_cookie(self.SESSIONID, self.session.session_id)
        elif session_id and self.session is None:
            self.clear_cookie(self.SESSIONID)
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
                return user


class JsonRequestHandler(RequestHandler):
    def _echo_and_end(self, data):
        self.set_header("Content-Type", "Application/json")
        self.finish(json.dumps(data))

    def echoerror(self, error):
        if not isinstance(error, (tuple, list)) or len(error) != 2:
            raise ValueError
        self._echo_and_end({"result": error[0], "msg": error[1]})

    def echodata(self, data):
        self._echo_and_end({"result": 0, "data": data})

