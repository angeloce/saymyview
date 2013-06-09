#coding:utf-8

from types import UnboundMethodType



class Meta(type):
    def __new__(cls, name, bases, attrs):
        print cls, name, bases, attrs
        for key, attr in attrs.items():
            print attr
            if key.startswith("_") or isinstance(attr, UnboundMethodType):
                pass


class Model(object):
    __metaclass__ = Meta
    # def __new__(cls, name, bases, attrs):
    #     print cls, name, bases, attrs
    #     for key, attr in attrs.items():
    #         print attr
    #         if key.startswith("_") or isinstance(attr, UnboundMethodType):
    #             pass









class C(Model):
    def asd(self):
        pass
