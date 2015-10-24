from req import ApiRequestHandler
from req import Service
import tornado

class ApiInfoHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err, data = Service.Bank.get_bank_news()
        if err: self.render(500)
        else: self.render(200, data)

