from req import Service
from service.base import BaseService

class StoreService(BaseService):
    def __init__(self, db, rs):
        self.db = db
        self.rs = rs
        StoreService.inst = self

    def get_store(self, data):
        args = ['id']
        err = self.check_required_args(args, data)
        if err: return (err, None)
        res, res_cnt = yield from self.db.execute('SELECT * FROM stores WHERE user_id = %s', (data['id'],))
        return (None, res)

    def add_store(self, data):
        args = ['id', 'name']
        err = self.check_required_args(args, data)
        if err: return (err, None)
        sql, param = self.gen_insert_sql('stores', {'user_id': data['id'], 'name': data['name']})
        res, res_cnt = yield from self.db.execute(sql, param)
        print(res)
        id = res[0]['id']
        return (None, id)
