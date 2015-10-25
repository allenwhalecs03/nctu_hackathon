from tornado import websocket, web, ioloop
import json
import time
from req import ApiRequestHandler
from req import Service
import tornadoredis
import tornado


class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    @tornado.gen.coroutine
    def open(self):
        print('open')
        self.ars = tornadoredis.Client(selected_db = 2)
        self.ars.connect()
        yield tornado.gen.Task(self.ars.subscribe, 'pay_list')
        self.ars.listen(self.on_message)

    def on_message(self, msg):
        if msg.kind == 'message':
            print(type(msg.body), msg.body)
            self.write_message(str(msg.body))

    def on_close(self):
        pass

