from tornado.web import RequestHandler as BaseRequestHandler
from jinja2 import FileSystemLoader, Enviroment

class RequestHandler(BaseRequestHandler):

    def render_string(self, template_name, **kwargs):
        loader = FileSystemLoader('templates')
        loader

