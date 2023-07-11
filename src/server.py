import struct

import websockets
import proto.api.api_common_pb2 as api_common_pb
from submodules.utils.protobuf_helper import ProtobufHelper
from submodules.utils.logger import Logger
from errors import PopupError
from handlers.base_handler import BaseHandler
from session import Session

logger = Logger()


class Server:

    def __init__(self, handlers, host="0.0.0.0", port=8765):
        self.server = websockets.serve(self.handle_connection, host, port)
        self.handlers = handlers

    async def handle_connection(self, websocket, path):
        try:
            print(f"!!!!!!!!!!!!!!!!!!!: {websocket}")
            setattr(websocket, "session", Session())
            await self.__handle_connection(websocket, path)
        except websockets.ConnectionClosed as ex:
            logger.error(f"Connection Closed: {ex}")

    async def __handle_connection(self, websocket, path):
        async for message_json in websocket:
            try:
                logger.info(f"收到信息: {message_json} {websocket}")
                logger.info(f"收到信息: {message_json.encode()} {websocket}")
                handler, message_json = self.parse_request(message_json)
                if handler.cpn == BaseHandler.PING:
                    await self.handle_message(handler, websocket, message_json)
                else:
                    if websocket.session.isAuthorized:
                        await self.handle_message(handler, websocket, message_json)
                    elif handler.cpn in [
                            BaseHandler.LOGIN,
                            BaseHandler.SIGN_UP
                    ]:
                        await self.handle_message(handler, websocket, message_json)
                        websocket.session.isAuthorized = True
            except PopupError as err:
                logger.traceback(err, f"业务逻辑错误: {err}")
                response = self.generate_popup_error_response(str(err))
                await websocket.send(ProtobufHelper.to_json_v2(response))

    async def handle_message(self, handler, websocket, params):
        async for response in handler(params):
            # 如果登陆或者注册失败了会直接抛出错误,所以如果代码执行到此处一定是成功的
            # await websocket.send(self.PN_to_bytes(handler.cpn) + response.SerializeToString())
            await websocket.send(ProtobufHelper.to_json_v2(self.wrap_protocol(response, handler.cpn)))

    def wrap_protocol(self, response, action, errmsg=None):
        p = api_common_pb.Protocol()
        p.action = action
        p.content = ProtobufHelper.to_json_v2(response)
        if errmsg:
            p.errmsg = errmsg
        else:
            p.errmsg = "success"
        return p

    def parse_request(self, content):
        """收到的字符串前两个字节表示请求的action"""
        action = int.from_bytes(content[0:2].encode())
        handler = self.handlers.get(action)
        if handler is None:
            raise PopupError(f"Action Not Supported: {action}")
        return handler(action), content[2:]

    def generate_popup_error_response(self, error):
        response = api_common_pb.PopupErrorResponse()
        response.error = error
        return self.wrap_protocol(response, BaseHandler.POPUP_ERROR, error)

    def PN_to_bytes(self, pn):
        return struct.pack('H', pn)
