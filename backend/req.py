import json
import logging
import types
import datetime
import collections
import tornado.template
import tornado.gen
import tornado.web
import tornado.websocket
import datetime
import re


def md(s):
    if s is None: s = ''
    return markdown.markdown(s, extensions=['markdown.extensions.nl2br'])

class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

class Service:
    pass

class RequestHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        try:
            self.get_argument('json')
            self.res_json = True

        except tornado.web.HTTPError:
            self.res_json = False

    def log(self, msg):
        pass

    def get_args(self, name):
        meta = {}
        for n in name:
            try:
                if n[-2:] == "[]":
                    meta[n[:-2]] = self.get_arguments(n)
                elif n[-6:] == "[file]":
                    n = n[:-6]
                    meta[n] = self.request.files[n][0]
                else:
                    meta[n] = self.get_argument(n)
            except:
                meta[n] = None
        return meta

    @tornado.gen.coroutine
    def prepare(self):
        self.title = "Hackathon"
        super().prepare();
        try: 
            self.token = self.get_secure_cookie('token').decode()
            self.acct = Service.User.get_user_info(self.token)
        except: 
            self.token = None
            self.acct = {}




class ApiRequestHandler(RequestHandler):
    def render(self, code=200, msg=""):
        self.finish(json.dumps({'status': code,
                                'msg': msg}, cls=DatetimeEncoder))
        return
    @tornado.gen.coroutine
    def prepare(self):
        super().prepare()

class WebRequestHandler(RequestHandler):
    def set_secure_cookie(self, name, value, expires_days=30, version=None, **kwargs):
        kwargs['httponly'] = True
        super().set_secure_cookie(name, value, expires_days, version, **kwargs)

    def write_error(self, status_code, err=None, **kwargs):
        kwargs["err"] = err
        self.render('error/%s.html'%(status_code), **kwargs)

    def render(self, templ, **kwargs):
        kwargs['title'] = self.title
        kwargs['acct'] = self.acct
        super().render('./web/template/'+templ, **kwargs)
        pass

    @tornado.gen.coroutine
    def prepare(self):
        super().prepare()
        if self.token is None and self.request.uri != "/users/signin/":
            self.redirect("/users/signin/")
        

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

