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
        try: 
            res = json.loads(r.text)
            req.set_secure_cookie('token', res['token'])
            _, res_cnt = yield from self.db.execute('SELECT * FROM users WHERE username = %s;', (data['username'],))
            if res_cnt == 0:
                insert_data = {'username': data['username'], 'account_id': res['account_id']}
                sql, param = self.gen_insert_sql('users', insert_data)
                yield from self.db.execute(sql, param)
            return (None, token)
        except: 
            res = {'message': r.text}
            return (r.text, None)

    def get_user_info(self, token):
        url = self.add_client_id(config.BASE_URL + '/accounts')
        r = requests.get(url, headers=self.headers(token))
        try: 
            return (None, json.loads(r.text)['accounts'][0])
        except:
            return (r.text, None)
