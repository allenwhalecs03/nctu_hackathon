from req import WebRequestHandler
from req import Service
import tornado

class WebPayHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, qrcode):
        err, data = yield from Service.Product.get_product_by_qr({'qrcode': qrcode})
        self.render('pay/check.html', qrcode=qrcode, data=data)
    
