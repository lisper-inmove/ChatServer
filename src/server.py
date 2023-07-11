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
            setattr(websocket, "session", Session())
            await self.__handle_connection(websocket, path)
        except websockets.ConnectionClosed as ex:
            logger.error(f"Connection Closed: {ex}")

    async def __handle_connection(self, websocket, path):
        async for message_json in websocket:
            try:
                message = api_common_pb.Protocol()
                message.ParseFromString(message_json)
                logger.info(f"收到信息: {message} {websocket}")
                handler = self.handlers.get(message.action)(message.action)
                if message.action == BaseHandler.PING:
                    await self.handle_message(handler, websocket, message)
                else:
                    if websocket.session.isAuthorized:
                        await self.handle_message(handler, websocket, message)
                    elif message.action in [
                            BaseHandler.LOGIN,
                            BaseHandler.SIGN_UP
                    ]:
                        await self.handle_user_authorize(handler, websocket, message)
            except PopupError as err:
                logger.traceback(err, f"业务逻辑错误: {err}")
                response = self.generate_popup_error_response(str(err))
                # await websocket.send(ProtobufHelper.to_json_v2(response))
                await websocket.send(response.SerializeToString())

    async def handle_message(self, handler, websocket, message):
        async for response in handler(message.content):
            # 如果登陆或者注册失败了会直接抛出错误,所以如果代码执行到此处一定是成功的
            await websocket.send(self.wrap_protocol(response, handler.cpn).SerializeToString())

    async def handle_user_authorize(self, handler, websocket, message):
        async for response in handler(message.content):
            websocket.session.user = handler.user
            websocket.session.isAuthorized = True
            websocket.session.token = response.token
            logger.info(f"回复消息: {response}")
            print(self.wrap_protocol(response, handler.cpn).SerializeToString())
            await websocket.send(self.wrap_protocol(response, handler.cpn).SerializeToString())

    def wrap_protocol(self, response, action, errmsg=None):
        p = api_common_pb.Protocol()
        p.action = action
        p.content = ProtobufHelper.to_json_v2(response)
        if errmsg:
            p.errmsg = errmsg
        else:
            p.errmsg = "success"
        return p

    def generate_popup_error_response(self, error):
        response = api_common_pb.PopupErrorResponse()
        response.error = error
        return self.wrap_protocol(response, BaseHandler.POPUP_ERROR, error)
