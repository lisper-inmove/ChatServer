import time
import random
import json
from handlers.base_handler import BaseHandler
import api.protocol_pb2 as protocol_pb


class ChatHandler(BaseHandler):

    def __call__(self, request):
        f = open("test")
        response = json.load(f)
        for chunk in response:
            # TODO: 为了模拟从第三方请求
            time.sleep(random.randint(10, 30) / 200)
            yield self.generate_response(chunk)

    def generate_response(self, chunk):
        choice = chunk.get('choices')[0]
        response = protocol_pb.Response()
        response.is_start = choice.get('delta').get('role') == 'assistant'
        response.content = choice.get('delta', {}).get('content', '')
        response.is_finished = choice.get('finish_reason') == 'stop'
        response.is_continue = not (response.is_start or response.is_finished)
        return response
