#coding:utf-8


from saymyview.utils.url import UrlHandlers


patterns = UrlHandlers("saymyview.web.handlers.api",
    [
        (r"/123", "enroll.EnrollWebLink"),
    ]
)
