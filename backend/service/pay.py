from req import Service
from service.base import BaseService
import requests
import json
import config
import datetime

class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

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
        err, resid = yield from self.pay({'product_id': product_info['id'], 'payee_account_id': product_info['account_id'], 'transaction_amount': product_info['price'], 'account_id': user_info['account_id'], 'token': data['token'], 'id_number': user_info['id_number']})
        return (None, resid)
    
    def pay(self, data={}):
        print('pay')
        args = ['payee_account_id', 'transaction_amount', 'account_id', 'id_number']
        err = self.check_required_args(args, data)
        if err: return (err, None)
        token = data.pop('token')
        url = self.add_client_id(config.BASE_URL + '/accounts/%s/in_house_transfer'%data.pop('account_id'))
        r = requests.post(url, data=json.dumps(data), headers=self.headers(token))
        meta = json.loads(r.text)
        meta['product_id'] = data['product_id']
        err, id = yield from self.update_db(meta)
        err, product = yield from Service.Product.get_product_by_id({'id': data['product_id']})
        self.rs.publish('pay_list', json.dumps(product, cls=DatetimeEncoder))
        return (None, id)

    def update_db(self, data={}):
        err, _from = yield from Service.User.get_user_id_by_account(data['account_id'])
        err, _to = yield from Service.User.get_user_id_by_account(data['payee_account_id'])
        meta = {
                "from_user_id": _from,
                "to_user_id": _to,
                "product_id": data['product_id']
                }
        return (None, 123)
