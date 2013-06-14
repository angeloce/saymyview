#coding:utf-8

from saymyview.utils.url import UrlHandlers

import api_urls



patterns = UrlHandlers("saymyview.web.handlers",
    [
        (r'/', 'index.IndexHandler'),
        (r'/login', 'index.LoginHandler'),
        (r'/logout', 'index.LogoutHandler'),
        (r'/url/add', 'weburl.EnrollHandler'),

        (r'/url/(\d+)', 'weburl.DetailHandler'),
        (r'/url/(\d+)/script', 'weburl.ScriptHandler'),
        (r'/api', api_urls.patterns),
    ]
)