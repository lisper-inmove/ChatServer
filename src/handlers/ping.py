from handlers.base_handler import BaseHandler
import api.protocol_pb2 as protocol_pb


class PingHandler(BaseHandler):

    def __call__(self, request):
        yield self.generate_response()

    def generate_response(self):
        response = protocol_pb.Response()
        return response
