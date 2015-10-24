from req import WebRequestHandler
from req import Service
import tornado

class WebProductHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, action=None, store_id=None):
        print(action)
        if action == 'get':
            err, data = yield from Service.Product.get_product({'store_id': store_id, 'id': self.id})
            if err:
                print(err)
                self.wrire_error(500)
            else: self.render('product/get_product.html', data=data)
        elif action == 'add':
            err, data = yield from Service.Product.get_product({'id': self.id})
            self.render('product/add_product.html')

