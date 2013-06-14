#coding:utf-8

from types import FunctionType


class Meta(type):
    def __new__(cls, name, bases, attrs):
        for key, attr in attrs.items():
            if key.startswith("_") or isinstance(attr, FunctionType):
                attrs[key] = classmethod(attr)
        return type.__new__(cls, name, bases, attrs)


class Model(object):
    __metaclass__ = Meta

