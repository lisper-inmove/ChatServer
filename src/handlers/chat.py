import api.chitchat_pb2 as api_chitchat_pb
import time
import random
import json
from handlers.base_handler import BaseHandler


class ChatHandler(BaseHandler):

    # 创建消息,发聊天内容
    CREATE_MESSAGE = 0x13
    UPDATE_MESSAGE = 0x14
    # 创建聊天
    CREATE_CHAT = 0x10
    UPDATE_CHAT = 0x11
    DELETE_CHAT = 0x12
    PN = [
        CREATE_CHAT,
        UPDATE_CHAT,
        DELETE_CHAT,
        CREATE_MESSAGE
    ]

    async def __call__(self, request):
        f = open("test")
        response = json.load(f)
        for chunk in response:
            # TODO: 为了模拟从第三方请求
            time.sleep(random.randint(10, 30) / 200)
            yield self.generate_response(chunk)

    def generate_response(self, chunk):
        choice = chunk.get('choices')[0]
        response = api_chitchat_pb.CreateMessageResponse()
        response.role = choice.get('delta').get('role', '')
        response.content = choice.get('delta', {}).get('content', '')
        return response
