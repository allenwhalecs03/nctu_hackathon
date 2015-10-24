from req import ApiRequestHandler
from req import Service
import tornado

class LoginHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        args = ['username', 'password']
        meta = self.get_args(args)
        err, token = Service.Account.login(self, meta)
        if err: self.render(403, err)
        else: self.render(200, token)



