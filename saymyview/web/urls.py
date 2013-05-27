#coding:utf-8

from saymyview.utils.url import UrlHandlers

import api_urls


patterns = UrlHandlers("saymyview.web.handlers",
    [
        (r'/', 'index.IndexHandler'),
        (r'/login', 'index.LoginHandler'),
        (r'/logout', 'index.LogoutHandler'),
        (r'/api', api_urls.patterns),
    ]
)
