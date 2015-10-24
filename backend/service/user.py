from service.base import BaseService
import requests
import json
import config

class UserService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        UserService.inst = self

    def login(self, req, data={}):
        '''
        username, password
        '''
        url = self.add_client_id(config.BASE_URL + '/login') 
        r = requests.post(url, data=json.dumps(data))
        try: res = json.loads(r.text)
        except: res = {'message': r.text}
        token = res.get('token')
        if token: req.set_secure_cookie('token', token)
        return (None if token else res['message'], token)

    def get_user_info(self, token):
        url = self.add_client_id(config.BASE_URL + '/accounts')
        r = requests.get(url, headers=self.headers(token))
        try: 
            return (None, json.loads(r.text))
        except:
            return (r.text, None)
