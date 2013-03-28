#coding:utf-8


patterns = [
    (r'/', 'base.RequestHandler')

]



# add prefix and check ahead
def meet_convetion(patterns, handler_prefix=None):
    new_patterns = []
    from tornado.util import import_object
    for pattern in patterns:
        if len(pattern) < 2:
            raise ValueError("Each url pattern must have two params")
        handler = pattern[1]
        if isinstance(handler, basestring):
            if handler_prefix and not handler.startswith(handler_prefix):
                handler = handler_prefix + handler
            handler = import_object(handler)
            pattern = list(pattern)
            pattern[1] = handler
        new_patterns.append(pattern)
    return new_patterns

patterns = meet_convetion(patterns, "saymyview.web.handlers.")
