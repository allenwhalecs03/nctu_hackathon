from req import ApiRequestHandler
from req import Service
import tornado

class ApiUserHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err, data = Service.User.get_user_info(self.token)
        print(data)
        if err: self.render(403, err)
        else: self.render(200, data)



