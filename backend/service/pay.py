from req import Service
from service.base import BaseService
import requests
import json
import config

class PayService(BaseService):
    def __init__(self, db, rs):
        self.db = db
        self.rs = rs
        PayService.inst = self
    
    def payqr(self, data={}):
        args = ['qrcode', 'id', 'token']
        err = self.check_required_args(args, data)
        if err: return (err, None)
        err, user_info = yield from Service.User.get_user_info(data['token'], data['id'])
        if err: return (err, None)
        err, product_info = yield from Service.Product.get_product_by_qr(data)
        if err: return (err, None)
        self.pay({'payee_account_id': product_info['account_id'], 'transaction_amount': product_info['price'], 'account_id': user_info['account_id'], 'token': data['token'], 'id_number': user_info['id_number']})
        return (None, product_info)
    
    def pay(self, data={}):
        args = ['payee_account_id', 'transaction_amount', 'account_id', 'id_number']
        err = self.check_required_args(args, data)
        if err: return (err, None)
        token = data.pop('token')
        url = self.add_client_id(config.BASE_URL + '/accounts/%s/in_house_transfer'%data.pop('account_id'))
        r = requests.post(url, data=json.dumps(data), headers=self.headers(token))
        print(r.text)

