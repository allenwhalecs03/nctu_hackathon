from req import Service
import hashlib
from service.base import BaseService
import time

class ProductService(BaseService):
    def __init__(self, db, rs):
        self.db = db
        self.rs = rs
        ProductService.inst = self

    def get_product(self, data):
        args = ['id']
        err = self.check_required_args(args, data)
        if err: return (err, None)
        res, res_cnt = yield from self.db.execute('SELECT * FROM products WHERE user_id = %s;', (data['id'],))
        return (None, res)

    def get_product_by_id(self, data):
        args = ['id']
        err = self.check_required_args(args, data)
        if err: return (err, None)
        res, res_cnt = yield from self.db.execute('SELECT p.*, u.* FROM products as p, users as u WHERE p.id = %s AND p.user_id = u.id;', (data['id'],))
        if res_cnt == 0:
            return ('Product Not Found', None)
        res = res[0]
        return (None, res)

    def get_product_by_qr(self, data):
        args = ['qrcode']
        err = self.check_required_args(args, data)
        if err: return (err, None)
        res, res_cnt = yield from self.db.execute('SELECT u.*, p.* FROM products as p, users as u WHERE p.qrcode = %s AND p.user_id = u.id;', (data['qrcode'],))
        if res_cnt == 0:
            return ('Product Not Found', None)
        res = res[0]
        return (None, res)

    def add_product(self, data):
        args = ['id', 'price']
        err = self.check_required_args(args, data)
        if err: return (err, None)
        id = data.pop('id')
        data['user_id'] = id
        sql, param = self.gen_insert_sql('products', data)
        res, res_cnt = yield from self.db.execute(sql, param)
        yield from self.gen_product_qr(res[0])
        id = res[0]['id']
        return (None, id)

    def gen_product_qr(self, data={}):
        args = ['id']
        err = self.check_required_args(args, data)
        if err: return (err, None)
        err, res = yield from self.get_product_by_id(data)
        if err: return (err, None)
        raw = ((''.join(str(res[x]) for x in res)) + str(time.time())).encode()
        hash_1 = hashlib.md5(raw).hexdigest()
        hash_2 = hashlib.sha512(raw).hexdigest()
        hashed = hash_1[len(hash_1)//3:] + hash_2[:len(hash_2)//3] 
        yield from self.db.execute('UPDATE products SET qrcode = %s WHERE id = %s;', (hashed,data['id'],))
        return hashed

