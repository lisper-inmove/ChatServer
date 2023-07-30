import websockets
import proto.api.api_common_pb2 as api_common_pb
from submodules.utils.protobuf_helper import ProtobufHelper
from submodules.utils.logger import Logger
from errors import PopupError
from errors import PopupSpecError
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
            request = api_common_pb.Request()
            request.ParseFromString(message_json)
            try:
                logger.info(f"收到信息: {request} {websocket}")
                if self.no_handler_message(websocket, request):
                    continue
                handler = self.handlers.get(request.action)(
                    request.action,
                    user=websocket.session.user,
                    websocket=websocket
                )
                if websocket.session.isAuthorized:
                    if request.action in [
                            api_common_pb.Action.STOP_GENERATE
                    ]:
                        await self.no_handler_message(websocket, request)
                    else:
                        await self.handle_message(handler, websocket, request)
                elif request.action in [
                        api_common_pb.Action.LOGIN,
                        api_common_pb.Action.SIGN_UP,
                        api_common_pb.Action.TOKEN_AUTHORIZE
                ]:
                    await self.handle_user_authorize(handler, websocket, request)
            except PopupError as err:
                logger.traceback(err, f"PopupError raised: {err}")
                replay = self.wrap_response(
                    request.action, errcode=api_common_pb.POPUP_ERROR, errmsg=str(err)
                ).SerializeToString()
                await websocket.send(replay)
            except PopupSpecError as err:
                logger.traceback(err, f"PopupSpecError raised: {err}")
                replay = self.wrap_response(
                    request.action, errcode=err.code, errmsg=err.msg
                ).SerializeToString()
                await websocket.send(replay)

    def no_handler_message(self, websocket, request):
        """某些不需要handler的操作"""
        if request.action == api_common_pb.Action.STOP_GENERATE:
            logger.info(f"Set generate stop: {websocket}")
            websocket.session.stop_generate = True
        else:
            return False
        return True

    async def handle_message(self, handler, websocket, request):
        async for response in handler(request.content):
            # 如果登陆或者注册失败了会直接抛出错误,所以如果代码执行到此处一定是成功的
            logger.info(f"回复消息: {handler} {response}")
            replay = self.wrap_response(response, handler.cpn).SerializeToString()
            await websocket.send(replay)

    async def handle_user_authorize(self, handler, websocket, request):
        async for response in handler(request.content):
            websocket.session.user = handler.user
            websocket.session.isAuthorized = True
            websocket.session.token = response.token
            logger.info(f"回复消息: {response}")
            replay = self.wrap_response(request.action, response).SerializeToString()
            await websocket.send(replay)
            await self.send_init_info(websocket)

    async def send_init_info(self, websocket):
        """当用户授权之后,给用户发一些必须要信息."""
        await self.__send_chitchat_list(websocket)

    async def __send_chitchat_list(self, websocket):
        from handlers.chitchat_handler import ChitchatHandler
        handler = ChitchatHandler(api_common_pb.Action.LIST_CHITCHAT)
        handler.user = websocket.session.user
        async for response in handler(None):
            reply = self.wrap_response(handler.cpn, response).SerializeToString()
            await websocket.send(reply)

    def wrap_response(self, action, response=None, errcode=None, errmsg=None):
        resp = api_common_pb.Response()
        resp.action = action
        if errcode is not None:
            resp.errcode = errcode
        if response is not None:
            resp.content = ProtobufHelper.to_json_v2(response)
        if errmsg is None:
            errmsg = "SUCCESS"
        resp.errmsg = errmsg
        return resp
