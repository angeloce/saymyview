#coding:utf-8


from saymyview.web.handlers.base import RequestHandler
from saymyview.web.models.weburl import WebUrl


class EnrollHandler(RequestHandler):

    def prepare(self):
        if not self.current_user:
            self.redirect('/login')

    def post(self):
        name = self.get_argument("name")
        url = self.get_argument("url")

        arguments = self.get_query_arguments()
        weburl = WebUrl.add_url(name, url, **arguments)

        return self.redirect('/url/%d' % weburl.id)

    def get(self):
        return self.render("weburl_enroll.html")



class DetailHandler(RequestHandler):

    def get(self, **kwargs):
        if kwargs["id"]:
            weburl = WebUrl.select().filter_by(id=kwargs["id"]).first()
        else:
            weburl = WebUrl.select().filter_by(url=kwargs["id"]).first()

        return self.render("weburl_detail.html", weburl=weburl)

