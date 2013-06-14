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
        weburl = WebUrl.add_url(name, url, arguments)

        return self.redirect('/url/%d' % weburl.id)

    def get(self):
        return self.render("weburl_enroll.html")



class DetailHandler(RequestHandler):

    def get(self, url_id):
        weburl = WebUrl.get_by_id(url_id)

        return self.render("weburl_detail.html", weburl=weburl)


class ScriptHandler(RequestHandler):

    def get(self, url_id):
        weburl = WebUrl.get_by_id(url_id)
        return self.render("weburl_script.html", weburl=weburl)

    def post(self, url_id):
        weburl = WebUrl.get_by_id(url_id)
        weburl_script = WebUrl.get_script(weburl.url)

        disable_script = self.get_argument("disable", "0")

        if disable_script != "0":
            script = self.get_argument("script", "")
            weburl_script.update(script=script)

        return self.render("weburl_script.html", weburl=weburl, weburl_script=weburl_script)