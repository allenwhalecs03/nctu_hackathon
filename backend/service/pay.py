from req import Service
from service.base import BaseService

class PayService(BaseService):
    def __init__(self, db, rs):
        self.db = db
        self.rs = rs
        PayService.inst = self
    
    def pay(self, data={}):
        args = ['qrcode', '']

