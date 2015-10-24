from req import WebRequestHandler
from req import Service
import tornado

class WebProductHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, action=None, product_id=None):
        print(action)
        if action == None:
            err, data = yield from Service.Product.get_product({'id': self.id})
            if err:
                self.wrire_error(500)
            else: self.render('product/get_product.html', data=data)
        elif action == 'add':
            err, data = yield from Service.Product.get_product({'id': self.id})
            self.render('product/add_product.html')
        elif action == 'show':
            err, data = yield from Service.Product.get_product_by_id({'id': product_id})
            if err: self.write_error(500, err)
            else: self.render('product/show_product.html', data=data)
        elif action == 'fast':
            self.render('product/fast_product.html')

