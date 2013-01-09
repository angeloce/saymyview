#coding:utf-8


import os
from jinja2 import FileSystemLoader



class ApplicationSettings(object):

    app_path = os.path.join(os.path.dirname(__file__), 'painter')
    debug = True
    static_path = os.path.join(app_path, "static")
    template_path = [os.path.join(app_path, 'templates')]
