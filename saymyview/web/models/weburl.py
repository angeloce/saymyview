#coding:utf-8


from saymyview.datamodel.weburl import WebUrlModel


class WebUrl(object):

    @classmethod
    def add_url(cls, name, url, **kwargs):

        weburl = WebUrlModel()
        kwargs["name"] = name
        kwargs["url"] = url
        weburl.set_fields(**kwargs)
        return weburl.insert()

    def get_urls(self, start=None, end=None):
        if start is None and end is None:
            start, end = 0, 10
        elif start is not None and end is None:
            start, end = 0, start

        return WebUrlModel.select().all()[start:end]

