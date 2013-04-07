#coding:utf-8

from tornado.web import RequestHandler as BaseRequestHandler
from jinja2 import FileSystemLoader, Environment

from saymyview.web.conf import convention
from saymyview.web.models.dbmodel import User


class RequestHandler(BaseRequestHandler):
    template_env = None

    def __init__(self, *args, **kwargs):
        BaseRequestHandler.__init__(self, *args, **kwargs)
        if not self.template_env:
            self.template_env = Environment(loader=FileSystemLoader(convention.template_path))

    def prepare(self):
        pass

    def render_string(self, template_name, **kwargs):
        template = self.template_env.get_template(template_name)
        namespace = self.get_template_namespace()
        namespace.update(kwargs)
        return template.render(**namespace)


class SessionSimpleMemory(object):
    def __init__(self):
        self._d = {}

        pass


class SessionManager(object):
    session_store = []

def auth_user(handler):
    handler.request.get_cookie('222')
    pass