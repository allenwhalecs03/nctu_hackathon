from service.base import BaseService 
import config
import requests
import json

class BankService(BaseService):
    def __init__(self, db, rs):
        self.db = db
        self.rs = rs
        BankService.inst = self

    def get_bank_news(self):
        url = self.add_client_id(config.BASE_URL + '/news')
        r = requests.get(url)
        try: return (None, json.loads(r.text))
        except: return (r.text, None)

    def get_bank_events(self):
        url = self.add_client_id(config.BASE_URL + '/events')
        r = requests.get(url)
        try: return (None, json.loads(r.text))
        except: return (r.text, None)



