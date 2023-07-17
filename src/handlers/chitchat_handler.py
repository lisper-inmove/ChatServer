import time
import random
import json

import proto.api.api_chitchat_pb2 as api_chitchat_pb
import proto.api.api_common_pb2 as api_common_pb
import proto.entities.chitchat_pb2 as chitchat_pb
from handlers.base_handler import BaseHandler
from manager.chitchat_manager import ChitchatManager
from manager.chitchat_message_manager import ChitchatMessageManager
from errors import PopupError

import grpc
import proto.grpc_api.grpc_chatgpt_pb2 as grpc_chatgpt_pb
import proto.grpc_api.grpc_chatgpt_pb2_grpc as grpc_chatgpt_pb_grpc


class ChitchatHandler(BaseHandler):

    CHATGPT_CLIENT_HOST = "chat.inmove.top:8443"

    PN = [
        api_common_pb.ProtocolNumber.CREATE_CHITCHAT,
        api_common_pb.ProtocolNumber.UPDATE_CHITCHAT,
        api_common_pb.ProtocolNumber.DELETE_CHITCHAT,
        api_common_pb.ProtocolNumber.LIST_CHITCHAT,
        api_common_pb.ProtocolNumber.CREATE_MESSAGE,
        api_common_pb.ProtocolNumber.UPDATE_MESSAGE,
        api_common_pb.ProtocolNumber.REGENERATE,
    ]

    async def __call__(self, request):
        fmaps = {
            api_common_pb.ProtocolNumber.CREATE_CHITCHAT: self.create_chitchat,
            api_common_pb.ProtocolNumber.UPDATE_CHITCHAT: self.update_chitchat,
            api_common_pb.ProtocolNumber.DELETE_CHITCHAT: self.delete_chitchat,
            api_common_pb.ProtocolNumber.LIST_CHITCHAT: self.list_chitchat,
            api_common_pb.ProtocolNumber.CREATE_MESSAGE: self.create_message,
            api_common_pb.ProtocolNumber.UPDATE_MESSAGE: self.update_message,
            api_common_pb.ProtocolNumber.REGENERATE: self.regenerate,
        }
        f = fmaps.get(self.cpn)
        if not f:
            raise PopupError("Action Not Exists")
        async for result in f(request):
            yield result

    async def delete_chitchat(self, request):
        manager = ChitchatManager()
        request = self.PH.to_obj_v2(request, api_chitchat_pb.DeleteChitchatRequest)
        chitchat = await manager.get_chitchat_by_id(request.id)
        if not chitchat:
            raise PopupError("Chitchat not Exists")
        if chitchat.userId != self.user.id:
            raise PopupError("Can not delete other's Chitchat")
        await manager.delete_chitchat(chitchat)
        yield chitchat

    async def create_chitchat(self, request):
        manager = ChitchatManager()
        request = self.PH.to_obj_v2(request, api_chitchat_pb.CreateChitchatRequest)
        chitchat = manager.create_chitchat(request, self.user)
        await manager.add_or_update_chitchat(chitchat)
        yield chitchat

    async def list_chitchat(self, request):
        manager = ChitchatManager()
        async for chitchat in manager.list_chitchat(self. user):
            yield chitchat

    async def create_message(self, request):
        manager = ChitchatMessageManager()
        request = self.PH.to_obj_v2(request, api_chitchat_pb.CreateMessageRequest)
        message = manager.create_chitchat_message(request)
        responseMessage = manager.create_chitchat_response_message(message)
        async for response in self.__call_chat_completion_request(message, responseMessage):
            yield response
        await manager.add_or_update_chitchat_message(message)
        await manager.add_or_update_chitchat_message(responseMessage)

    async def regenerate(self, request):
        request = self.PH.to_obj_v2(request, api_chitchat_pb.Regeneraterequest)
        manager = ChitchatMessageManager()
        message = manager.get_chitchat_message_by_id(request.messageId)
        responseMessage = manager.create_chitchat_response_message(message)
        async for response in self.__call_chat_completion_request(message, responseMessage):
            yield response
        await manager.add_or_update_chitchat_message(message)
        await manager.add_or_update_chitchat_message(responseMessage)

    async def __call_chat_completion_request(self, message, responseMessage):
        with grpc.secure_channel(self.CHATGPT_CLIENT_HOST, grpc.ssl_channel_credentials()) as channel:
            stub = grpc_chatgpt_pb_grpc.ChatGPTStub(channel)
            for response in stub.ChatCompletion(grpc_chatgpt_pb.ChatCompletionRequest(
                messages=[
                    grpc_chatgpt_pb.ChatCompletionRequest.ChatCompletionMessage(
                        role=chitchat_pb.ChitchatMessage.Role.Name(message.role).lower(),
                        content=message.content
                    )
                ]
            )):
                response = self.generate_response(response)
                responseMessage.content += response.content
                yield response
                if self.websocket.session.stop_generate:
                    self.websocket.session.stop_generate = False
                    break

    def generate_response(self, chunk):
        choice = chunk.choices[0]
        response = api_chitchat_pb.CreateMessageResponse()
        response.role = choice.delta.role
        response.content = choice.delta.content
        response.isStart = choice.delta.role == 'assistant'
        response.isFinished = choice.finish_reason == 'stop'
        response.isContinue = not (response.isStart or response.isFinished)
        return response

    async def create_message_test(self, request):
        f = open("test")
        response = json.load(f)
        for chunk in response:
            # TODO: 为了模拟从第三方请求
            time.sleep(random.randint(10, 30) / 200)
            yield self.generate_response_test(chunk)

    def generate_response_test(self, chunk):
        choice = chunk.get('choices')[0]
        response = api_chitchat_pb.CreateMessageResponse()
        response.role = choice.get('delta').get('role', '')
        response.content = choice.get('delta', {}).get('content', '')
        response.isStart = choice.get('delta', {}).get('role') == 'assistant'
        response.isFinished = choice.get('finish_reason') == 'stop'
        response.isContinue = not (response.isStart or response.isFinished)
        return response
