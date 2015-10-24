from req import ApiRequestHandler
from req import Service
import tornado

class ApiProductHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        args = ['name', 'price']
        meta = self.get_args(args)
        meta['id'] = self.id
        err, res = yield from Service.Product.add_product(meta)
        if err: self.render(500, err)
        else: self.render(200, res)

