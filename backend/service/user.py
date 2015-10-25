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
            token = res['token']
            req.set_secure_cookie('token', token)
            _, res_cnt = yield from self.db.execute('SELECT * FROM users WHERE username = %s;', (data['username'],))
            if res_cnt == 0:
                insert_data = {'username': data['username'], 'account_id': ' '}
                sql, param = self.gen_insert_sql('users', insert_data)
                yield from self.db.execute(sql, param)
            res, res_cnt = yield from self.db.execute('SELECT id FROM users WHERE username=%s', (data['username'],))
            id = res[0]['id']
            req.set_secure_cookie('id', str(id))
            err, res = yield from self.get_user_info(token, id)
            sql, param = self.gen_update_sql('users', {'account_id': res['account_id']})
            yield from self.db.execute(sql+' WHERE id=%s', param+(str(id),))
            return (None, token)
        except Exception as e: 
            return (r.text, None)

    def get_user_info(self, token, id):
        url = self.add_client_id(config.BASE_URL + '/accounts')
        r = requests.get(url, headers=self.headers(token))
        try: 
            res, res_cnt = yield from self.db.execute('SELECT username FROM users WHERE id=%s;', (id,))
            res = res[0]
            res.update(json.loads(r.text)['accounts'][0])
            return (None, res)
        except:
            return (r.text, None)

    def get_user_id_by_account(self, account):
        res, rescnt = yield from self.db.execute("SELECT id FROM users WHERE account_id=%s", (account,))
        return (None, res[0]['id'])
