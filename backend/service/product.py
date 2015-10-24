from req import Service
from service.base import BaseService

class ProductService(BaseService):
    def __init__(self, db, rs):
        self.db = db
        self.rs = rs
        ProductService.inst = self

    def get_product(self, data):
        args = ['store_id', 'id']
        err = self.check_required_args(args, data)
        if err: return (err, None)
        res, res_cnt = yield from self.db.execute('SELECT * FROM products WHERE store_id = %s;', (data['store_id'],))
        print("PRO", res)
        return (None, res)

    def add_product(self, data):
        args = ['id', 'name', 'store_id']
        err = self.check_required_args(args, data)
        if err: return (err, None)
        sql, param = self.gen_insert_sql('products', {'user_id': data['id'], 'name': data['name'], 'store_id': data['store_id']})
        res, res_cnt = yield from self.db.execute(sql, param)
        print(res)
        id = res[0]['id']
        return (None, id)
