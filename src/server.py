import websockets
import proto.api.api_common_pb2 as api_common_pb
from submodules.utils.protobuf_helper import ProtobufHelper
from submodules.utils.logger import Logger
from errors import PopupError
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
                if self.no_handler_message(websocket, message):
                    continue
                handler = self.handlers.get(message.action)(
                    message.action,
                    user=websocket.session.user
                )
                if websocket.session.isAuthorized:
                    if message.action in [
                            api_common_pb.ProtocolNumber.STOP_GENERATE
                    ]:
                        await self.no_handler_message(websocket, message)
                    else:
                        await self.handle_message(handler, websocket, message)
                elif message.action in [
                        api_common_pb.ProtocolNumber.LOGIN,
                        api_common_pb.ProtocolNumber.SIGN_UP,
                        api_common_pb.ProtocolNumber.TOKEN_AUTHORIZE
                ]:
                    await self.handle_user_authorize(handler, websocket, message)
            except PopupError as err:
                logger.traceback(err, f"业务逻辑错误: {err}")
                replay = self.wrap_protocol(None, handler.cpn).SerializeToString()
                await websocket.send(replay)

    def no_handler_message(self, websocket, message):
        """某些不需要handler的操作"""
        if message.action == api_common_pb.ProtocolNumber.STOP_GENERATE:
            logger.info(f"Set generate stop: {websocket}")
            websocket.session.stop_generate = True
        else:
            return False
        return True

    async def handle_message(self, handler, websocket, message):
        async for response in handler(message.content):
            # 如果登陆或者注册失败了会直接抛出错误,所以如果代码执行到此处一定是成功的
            logger.info(f"回复消息: {handler} {response}")
            replay = self.wrap_protocol(response, handler.cpn).SerializeToString()
            await websocket.send(replay)

    async def handle_user_authorize(self, handler, websocket, message):
        async for response in handler(message.content):
            websocket.session.user = handler.user
            websocket.session.isAuthorized = True
            websocket.session.token = response.token
            logger.info(f"回复消息: {response}")
            replay = self.wrap_protocol(response, handler.cpn).SerializeToString()
            await websocket.send(replay)
            await self.send_init_info(websocket)

    async def send_init_info(self, websocket):
        """当用户授权之后,给用户发一些必须要信息."""
        await self.__send_chitchat_list(websocket)

    async def __send_chitchat_list(self, websocket):
        from handlers.chitchat_handler import ChitchatHandler
        handler = ChitchatHandler(api_common_pb.ProtocolNumber.LIST_CHITCHAT)
        handler.user = websocket.session.user
        async for response in handler(None):
            reply = self.wrap_protocol(response, handler.cpn).SerializeToString()
            await websocket.send(reply)

    def wrap_protocol(self, response, action, errmsg=None):
        p = api_common_pb.Protocol()
        p.action = action
        if response is not None:
            p.content = ProtobufHelper.to_json_v2(response)
        if errmsg:
            p.errmsg = errmsg
        else:
            p.errmsg = "success"
        return p
