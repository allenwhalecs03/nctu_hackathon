from service.base import BaseService
import requests
import config

class AccountService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        AccountService.inst = self

    def get_token(self, data={}):
        '''
        username, password
        '''
        url = self.add_client_id(config.BASE_URL + '/login') 


