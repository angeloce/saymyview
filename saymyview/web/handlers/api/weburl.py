#coding:utf-8

from saymyview.web.handlers.base import JsonRequestHandler
from saymyview.datamodel.weburl import WebUrl


class EnrollHandler(JsonRequestHandler):
    ST_URL_REQUIRED = ("-101", "url is required")
    ST_URL_INVALID = ("-102", "url is invalid")

    def post(self):
        url = self.get_argument("url")
        short_description = self.get_argument("short")

        if not url:
            return self.echoerror(self.ST_URL_REQUIRED)

        weburl = WebUrl(url=url, short_description=short_description).insert()

        return self.echodata(dict(weburl))


class UpdateHandler(JsonRequestHandler):
    ST_URL_REQUIRED = ("-101", "url is required")
    ST_URL_INVALID = ("-102", "url is invalid")

    def post(self):
        weburl_id = self.get_argument("id")
        name = self.get_argument("name", None)
        url = self.get_argument("url", None)
        short_description = self.get_argument("short", None)

        weburl = WebUrl.select().filter_by(id=weburl_id).first()

        if name is not None:
            weburl.name = name

        if url is not None:
            weburl.url = url

        if short_description is not None:
            weburl.short_description = short_description

        weburl.session.commit()

        return self.echodata(dict(weburl))