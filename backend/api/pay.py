from req import ApiRequestHandler
from req import Service
import tornado

class ApiPayHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self, qrcode):
        err, res = yield from Service.Pay.payqr({'token': self.token, 'id': self.id, 'token': self.token, 'qrcode': qrcode})
        print("api pay", res)
        self.render(200, res)
        

