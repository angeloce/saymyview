#coding:utf-8


class UrlHandlers(object):
    def __init__(self, handler_prefix="", patterns=None):
        self.handler_prefix = handler_prefix
        self.patterns = patterns

    def __iter__(self):
        handler_prefix = self.handler_prefix.strip()
        if handler_prefix and not handler_prefix.endswith('.'):
            handler_prefix += "."
        from tornado.util import import_object
        for pattern in self.patterns:
            if len(pattern) != 2:
                raise ValueError("Each url pattern must have two params")
            url_pattern = pattern[0]
            handler = pattern[1]
            if isinstance(handler, basestring):
                if handler_prefix and not handler.startswith(handler_prefix):
                    handler = handler_prefix + handler
                handler = import_object(handler)
            if isinstance(handler, self.__class__):
                for sub_url_pattern, sub_handler in handler:
                    yield url_pattern + sub_url_pattern, sub_handler
                continue
            yield url_pattern, handler


