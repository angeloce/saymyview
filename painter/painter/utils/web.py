#coding:utf-8

import os
import sys

from tornado.web import RequestHandler as BaseRequestHandler
from jinja2 import FileSystemLoader, Environment

class RequestHandler(BaseRequestHandler):
    template_env = None
    def __init__(self, *args, **kwargs):
        BaseRequestHandler.__init__(self, *args, **kwargs)
        if not self.template_env:
            self.template_env = Environment(loader = FileSystemLoader(self.application.settings['template_path']))
    
    def render_string(self, template_name, **kwargs):
        template = self.template_env.get_template(template_name)
        namespace = self.get_template_namespace()
        namespace.update(kwargs)
        return template.render(**namespace)


def H(handler_name):
    rl = handler_name.rsplit('.', 1)
    module_name = 'painter.handlers' + '.'+rl[0] if rl[0] else ''
    module = __import__(module_name, fromlist=['...'])
    handler = getattr(module, rl[1])
    return handler

