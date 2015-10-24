### tornado 
import tornado.ioloop
import tornado.httpserver
import tornado.web
### self define from req import RequestHandler
from req import Service 
### my app
import config
import pg
import mysql
import myredis

### service 
from service.account import AccountService

### api
from api.login import LoginHandler


### web
from web.index import WebIndexHandler

### built-in module
import time
import signal
import logging


def sig_handler(sig, frame):
    print('Catch Stop Signal')
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)

def shutdown():
    print('Server Stopping')
    srv.stop()
    io_loop = tornado.ioloop.IOLoop.instance()
    deadline = time.time() + config.MAX_WAIT_SECOND_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            print('Server Stopped')
    stop_loop()


if __name__ == '__main__':
    print('Server Starting')
    db = pg.AsyncPG(config.DBNAME, config.DBUSER, config.DBPASSWORD, host=config.DBHOST, dbtz='+8')
    rs = myredis.MyRedis(db=2)
    rs.flushdb()
    ui_modules = {
            }
    app = tornado.web.Application([
        ('/asset/(.*)', tornado.web.StaticFileHandler, {'path': '../http'}),
        ('/', WebIndexHandler),
        ('/login/', LoginHandler),
        ],  cookie_secret = config.COOKIE_SECRET, 
            compress_response = True,
            debug = config.DEBUG,
            autoescape =    'xhtml_escape', 
            ui_modules =    ui_modules,
            xheaders=True,)
    global srv
    srv = tornado.httpserver.HTTPServer(app)
    Service.Account = AccountService(db, rs)
    srv.listen(config.PORT)
    print('Server Started')
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    tornado.ioloop.IOLoop().instance().start()
