#coding:utf-8

from functools import wraps


def require_login(redirect='/'):
    def wrapper_method(self, *args, **kwargs):
        if self.current_user is None:
            return self.redirect()

    return wrapper_method


