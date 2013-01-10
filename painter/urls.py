
from painter.base import RequestHandler

class IndexHandler(RequestHandler):
    def get(self):
        self.render('base.html')

patterns = [
    (r'/', IndexHandler)



]
