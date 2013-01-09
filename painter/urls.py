
from painter.base import RequestHandler

class IndexHandler(RequestHandler):
    def get(self):
        self.render('layout.html')

patterns = [
    (r'/', IndexHandler)



]
