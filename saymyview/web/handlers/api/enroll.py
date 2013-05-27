#coding:utf-8

from saymyview.web.handlers.base import JsonRequestHandler
from saymyview.datamodel.weblink import WebLink

class EnrollWebLink(JsonRequestHandler):
    ST_URL_REQUIRED = ("-101", "url is required")
    ST_URL_INVALID = ("-102", "url is invalid")

    def post(self):
        url = self.get_argument("url")
        short_description = self.get_argument("short")

        if not url:
            return self.echoerror(self.ST_URL_REQUIRED)

        link = WebLink(url=url, short_description=short_description).insert()

        return self.echodata({"id": link.id, "url": link.url})

