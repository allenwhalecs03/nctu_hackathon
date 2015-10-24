from req import WebRequestHandler
from req import Service
import tornado

class WebInfoHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        #err, data = Service.Bank.get_bank_news()
        #if err: self.write_error(500)
        self.render('bank/info.html', data=data)
