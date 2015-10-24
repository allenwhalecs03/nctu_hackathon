from req import WebRequestHandler
from req import Service
import tornado

class Web404Handler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.write(404)

