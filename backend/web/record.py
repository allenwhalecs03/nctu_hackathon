from req import WebRequestHandler
from req import Service
import tornado

class WebRecordHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err, data = yield from Service.Record.get_record_list_by_id({"id": self.id})
        self.render('./record/record.html', data=data)
        
