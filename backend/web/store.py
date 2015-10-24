from req import WebRequestHandler
from req import Service
import tornado

class WebStoreHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, action=None):
        if action == None:
            err, data = yield from Service.Store.get_store({'id': self.id})
            self.render('store/get_store.html', data=data)
        if action == 'add':
            self.render('store/add_store.html')

