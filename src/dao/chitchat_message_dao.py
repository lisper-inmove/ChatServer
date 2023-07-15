import proto.entities.chitchat_pb2 as chitchat_pb
from dao.mongodb import MongoDBHelper
from dao.base_dao import BaseDao


class ChitchatMessageDA(MongoDBHelper, BaseDao):

    coll = "___chitchat_db___chitchat_messages___"

    async def add_or_update_chitchat_message(self, chitchatMessage):
        matcher = {"id": chitchatMessage.id}
        json_data = self.PH.to_dict(chitchatMessage)
        await self.update_one(matcher, json_data, upsert=True)

    async def get_chitchat_message_by_id(self, id):
        matcher = {"id": id}
        chitchatMessage = await self.find_one(matcher)
        return self.PH.to_obj(chitchatMessage, chitchat_pb.ChitchatMessage)

    async def list_chitchat_messages(self, chatId):
        matcher = {"chatId": chatId}
        async for message in self.find_many(matcher):
            yield self.PH.to_obj(message, chitchat_pb.ChitchatMessage)
