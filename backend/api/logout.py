from req import ApiRequestHandler
from req import Service
import tornado

class ApiLogoutHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        try:
            self.clear_cookie("token")
            self.clear_cookie("id")
            self.render(200)
        except:
            self.render(500)
