from req import ApiRequestHandler
from req import Service
import tornado

class ApiPayHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self, qrcode):
        args = ['longitude', 'latitude']
        meta = self.get_args(args)
        meta['token'] = self.token
        meta['id'] = self.id
        meta['qrcode'] = qrcode
        err, res = yield from Service.Pay.payqr(meta)
        self.render(200, res)
        

