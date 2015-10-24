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
        elif page == 'finance_news':
            err, data = Service.Bank.get_bank_finance_news()
            if err: self.write_error(500)
            else: self.render('bank/finance_news.html', data=data)
        elif page == 'foreign_market':
            err, data = Service.Bank.get_bank_foreign_market()
            if err: self.write_error(500)
            else: self.render('bank/foreign_market.html', data=data)
        elif page == 'rate_spot_exchange':
            err, data = Service.Bank.get_bank_rate_spot_exchange()
            if err: self.write_error(500)
            else: self.render('bank/rate_spot_exchange.html', data=data)
        elif page == 'rate_deposit_loan':
            err, data = Service.Bank.get_bank_rate_deposit_loan()
            if err: self.write_error(500)
            else: self.render('bank/rate_deposit_loan.html', data=data)




