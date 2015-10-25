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
from service.user import UserService
from service.bank import BankService
from service.product import ProductService
from service.pay import PayService

### api
from api.login import ApiLoginHandler
from api.bank import ApiInfoHandler
from api.logout import ApiLogoutHandler
from api.user import ApiUserHandler
from api.product import ApiProductHandler
from api.pay import ApiPayHandler
from api.ws import SocketHandler

### web
from web.index import WebIndexHandler
from web.user  import WebUserSignHandler
from web.error import Web404Handler
from web.bank import WebInfoHandler
from web.product import WebProductHandler
from web.pay import WebPayHandler
from web.ws import WebWSHandler
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
        ### web
        ('/', WebIndexHandler),
        ('/users/(sign.*)/', WebUserSignHandler),
        ('/banks/info/', WebInfoHandler),
        ('/banks/info/(.*)/', WebInfoHandler),
        ('/products/', WebProductHandler),
        ('/products/(\w+)/', WebProductHandler),
        ('/products/(\w+)/(\d+)/', WebProductHandler),
        ('/pay/(\w+)/', WebPayHandler),
        ('/ws/', WebWSHandler),
        #### api
        ('/api/banks/info/', ApiInfoHandler),
        ('/api/users/signin/', ApiLoginHandler),
        ('/api/users/signout/', ApiLogoutHandler),
        ('/api/users/', ApiUserHandler),
        ('/api/products/', ApiProductHandler),
        ('/api/pay/(\w+)/', ApiPayHandler),
        ('/api/ws/', SocketHandler),
        ### 404
        ('.*', Web404Handler),
        ],  cookie_secret = config.COOKIE_SECRET,
            compress_response = True,
            debug = config.DEBUG,
            autoescape =    'xhtml_escape',
            ui_modules =    ui_modules,
            xheaders=True,)
    global srv
    srv = tornado.httpserver.HTTPServer(app)
    Service.User = UserService(db, rs)
    Service.Bank = BankService(db, rs)
    Service.Product = ProductService(db, rs)
    Service.Pay = PayService(db, rs)
    srv.listen(config.PORT)
    print('Server Started')
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    tornado.ioloop.IOLoop().instance().start()
