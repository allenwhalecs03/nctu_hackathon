from req import WebRequestHandler
from req import Service
import tornado

class WebPayHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, qrcode):
        self.render('pay/check.html', qrcode=qrcode)
    
    @tornado.gen.coroutine
    def post(self, qrcode):
        err, res = yield from Service.Pay.payqr({'token': self.token, 'id': self.id, 'token': self.token, 'qrcode': qrcode})

