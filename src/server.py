import websockets
import api.protocol_pb2 as protocol_pb
from submodules.utils.protobuf_helper import ProtobufHelper
from submodules.utils.logger import Logger
from client import Client
from errors import MyError

logger = Logger()


class Server:

    def __init__(self, handlers, host="0.0.0.0", port=8765):
        self.server = websockets.serve(self.handle_connection, host, port)
        self.handlers = handlers

    async def handle_message(self, client, action, request):
        result = action()(request)
        try:
            for response in result:
                response.sender = "server"
                response.action = request.action
                await client.send(ProtobufHelper.to_json_v2(response))
        except MyError as err:
            logger.info(f"业务逻辑错误发生: {err}")
            response = protocol_pb.Response()
            response.sender = "server"
            response.action = "error"
            response.content = str(err)
            await client.send(ProtobufHelper.to_json_v2(response))

    async def handle_connection(self, websocket, path):
        try:
            async for message_json in websocket:
                logger.info(f"收到信息: {message_json} {websocket}")
                request = ProtobufHelper.to_obj_v2(message_json, protocol_pb.Request)
                action = self.handlers.get(request.action)
                await self.handle_message(websocket, action, request)
        except websockets.ConnectionClosed as ex:
            logger.error(f"Websocket closed: {ex}")
