#coding:utf-8


from saymyview.utils.url import UrlHandlers


patterns = UrlHandlers("saymyview.web.handlers.api",
    [
        (r"/url/add", "weburl.EnrollHandler"),
        (r"/url/update", "weburl.UpdateHandler"),
    ]

)
