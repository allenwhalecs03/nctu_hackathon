from req import WebRequestHandler
from req import Service
import tornado

class WebIndexHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render('index.html')

