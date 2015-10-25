from tornado import websocket, web, ioloop
import json
import time
from req import ApiRequestHandler
from req import Service
#Service.User.get_user_info(self.token)
c1 = []

def chk(ws):
    pass
class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print(Service.User.get_user_info(self.token))
        #if not check_client_exist(self):
        #    data = json.dumps(data)
        #    self.write_message(data)
        #    cl.append(client)

    def on_message(self, data):
        client.write_message("hello")

    def on_close(self):
        pass

    def send_device_list(self):
        pass
