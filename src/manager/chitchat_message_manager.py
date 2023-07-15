import proto.entities.chitchat_pb2 as chitchat_pb
from manager.base_manager import BaseManager
from dao.chitchat_message_dao import ChitchatMessageDA


class ChitchatMessageManager(BaseManager):

    @property
    def dao(self):
        if self._dao is None:
            self._dao = ChitchatMessageDA()
        return self._dao

    def create_chitchat_message(self, request):
        chitchat_message = self.create_obj(chitchat_pb.ChitchatMessage)
        chitchat_message.chitchatId = request.chitchatId
        chitchat_message.content = request.content
        return chitchat_message

    def create_chitchat_response_message(self, request):
        chitchat_message = self.create_obj(chitchat_pb.ChitchatMessage)
        chitchat_message.chitchatId = request.chitchatId
        chitchat_message.isResponse = True
        return chitchat_message

    async def get_chitchat_message_by_id(self, id):
        chitchat_message = await self.dao.get_chitchat_message_by_id(id)
        return chitchat_message

    async def list_chitchat_messages(self, chatId):
        async for chitchat_message in self.dao.list_chitchat_messages(chatId):
            yield chitchat_message

    async def add_or_update_chitchat_message(self, chitchatMessage):
        self.update_obj(chitchatMessage)
        await self.dao.add_or_update_chitchat_message(chitchatMessage)
