#coding:utf-8

settings = None
if settings is None:
    from . import application
    settings = {}
    for k in dir(application):
        if k.isupper() and not k.startswith('__'):
            settings[k.lower()] = getattr(application, k)
