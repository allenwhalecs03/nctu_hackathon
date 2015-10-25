from req import WebRequestHandler
from req import Service
import tornado

class WebWSHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render('ws/test.html')

