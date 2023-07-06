import api.common_pb2 as api_common_pb
from handlers.base_handler import BaseHandler


class PingHandler(BaseHandler):

    PING = 0x00
    PN = [PING]

    async def __call__(self, request):
        response = api_common_pb.PingResponse()
        yield response
