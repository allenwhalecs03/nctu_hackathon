from req import WebRequestHandler
from req import Service
import tornado

class WebUserSignHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, action):
        print(action)
        if action == "signin":
            self.render('user/signin.html')

