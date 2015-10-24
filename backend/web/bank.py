from req import WebRequestHandler
from req import Service
import tornado

class WebInfoHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, page=None):
        if page is None:
            self.render('bank/info.html')
        elif page == 'news':
            err, data = Service.Bank.get_bank_news()
            if err: self.write_error(500)
            else: self.render('bank/news.html', data=data)
        elif page == 'events':
            err, data = Service.Bank.get_bank_events()
            if err: self.write_error(500)
            else: self.render('bank/events.html', data=data)

