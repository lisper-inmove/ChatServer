import proto.entities.chitchat_pb2 as chitchat_pb
from manager.base_manager import BaseManager
from dao.chitchat_dao import ChitchatDA


class ChitchatManager(BaseManager):

    @property
    def dao(self):
        if self._dao is None:
            self._dao = ChitchatDA()
        return self._dao

    def create_chitchat(self, request, user):
        chitchat = self.create_obj(chitchat_pb.Chitchat)
        chitchat.userId = user.id
        chitchat.name = request.name
        chitchat.type = chitchat_pb.Chitchat.Type.Value(request.type)
        return chitchat

    async def list_chitchat(self, user):
        async for chitchat in self.dao.list_chitchat(user.id):
            yield chitchat

    async def get_chitchat_by_id(self, id):
        chitchat = await self.dao.get_chitchat_by_id(id)
        return self.PH.to_obj(chitchat, chitchat_pb.Chitchat)

    async def delete_chitchat(self, chitchat):
        return await self.dao.delete_chitchat(chitchat.id)

    async def add_or_update_chitchat(self, chitchat):
        super().update_obj(chitchat)
        await self.dao.add_or_update_chitchat(chitchat)
