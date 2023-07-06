import json
import websockets
import api.common_pb2 as common_pb
from submodules.utils.protobuf_helper import ProtobufHelper
from submodules.utils.logger import Logger
from client import Client
from errors import PopupError

logger = Logger()


class Server:

    def __init__(self, handlers, host="0.0.0.0", port=8765):
        self.server = websockets.serve(self.handle_connection, host, port)
        self.handlers = handlers

    async def handle_connection(self, websocket, path):
        try:
            await self.__handle_connection(websocket, path)
        except PopupError as err:
            logger.info(f"业务逻辑错误发生: {err}")
            response = self.generate_popup_error_response(str(err))
            await websocket.send(ProtobufHelper.to_json_v2(response))
        except websockets.ConnectionClosed as ex:
            logger.error(f"Connection Closed: {ex}")

    async def __handle_connection(self, websocket, path):
        async for message_json in websocket:
            handler, message_json = self.parse_request(message_json)
            logger.info(f"收到信息: {message_json} {websocket}")
            await self.handle_message(handler, websocket, message_json)

    async def handle_message(self, handler, client, params):
        try:
            async for response in handler(params):
                await client.send(handler.PN_to_str() + ProtobufHelper.to_json_v2(response))
        except PopupError as err:
            logger.info(f"业务逻辑错误发生: {err}")
            response = self.generate_popup_error_response(str(err))
            await client.send(ProtobufHelper.to_json_v2(response))

    def parse_request(self, content):
        """收到的字符串前两个字符表示请求的action"""
        action = int.from_bytes(content[0:2].encode())
        handler = self.handlers.get(action)
        if handler is None:
            raise PopupError(f"Action Not Supported: {action}")
        return handler(action), content[2:]

    def generate_popup_error_response(self, error):
        response = common_pb.PopupErrorResponse()
        response.error = error
        return response
