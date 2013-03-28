#coding:utf-8

import os

app_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
static_path = os.path.join(app_path, 'static')
template_path = os.path.join(app_path, 'templates')

