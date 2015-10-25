from req import Service
import hashlib
from service.base import BaseService
import time

class RecordService(BaseService):
    def __init__(self, db, rs):
        self.db = db
        self.rs = rs
        RecordService.inst = self

    def get_record_list_by_id(self, data={}):
        print(data)
        res, rescnt = yield from self.db.execute("""
        SELECT p.price, p.name, records.*, s1.username as from_user, s2.username as to_user 
        FROM records, users as s1, users as s2, products as p
        WHERE (from_user_id=%s or to_user_id=%s)
        and s1.id=records.from_user_id
        and s2.id=records.to_user_id 
        and p.id=records.product_id
        order by id
        """, (str(data['id']), str(data['id']),))

        return (None, res)
