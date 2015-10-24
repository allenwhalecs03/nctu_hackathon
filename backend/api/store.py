from req import ApiRequestHandler
from req import Service
import tornado

class ApiStoreHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        args = ['name']
        meta = self.get_args(args)
        meta['id'] = self.id
        err, res = yield from Service.Store.add_store(meta)
        if err: self.render(500, err)
        else: self.render(200, res)

