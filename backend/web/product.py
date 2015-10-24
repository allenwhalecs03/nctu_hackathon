from req import WebRequestHandler
from req import Service
import tornado

class WebProductHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, action=None):
        if action == None:
            data = None
            self.render('product/get_product.html', data=data)
        elif action == 'add':
            err, data = yield from Service.Store.get_store({'id': self.id})
            self.render('product/add_product.html')

