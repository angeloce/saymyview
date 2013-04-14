#coding:utf-8


from convention import *
from local import *

settings = None
if settings is None:
    settings = {}
    for k, v in locals().items():
        if not k.startswith('__'):
            settings[k] = v
