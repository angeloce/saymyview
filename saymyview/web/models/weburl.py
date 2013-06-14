#coding:utf-8


from saymyview.datamodel.weburl import WebUrlModel

from _base import Model


class WebUrl(Model):

    def add_url(self, name, url, kwargs):
        weburl = WebUrlModel()
        kwargs["name"] = name
        kwargs["url"] = url
        weburl.set_fields(**kwargs)
        return weburl.insert()

    def get_by_id(self, url_id):
        return WebUrlModel.select().filter_by(id=url_id).one()

    def get_by_url(self, url):
        return WebUrlModel.select().filter_by(url=url).one()

    def get_urls(self, start=None, end=None):
        if start is None and end is None:
            start, end = 0, 10
        elif start is not None and end is None:
            start, end = 0, start

        return WebUrlModel.select().all()[start:end]

