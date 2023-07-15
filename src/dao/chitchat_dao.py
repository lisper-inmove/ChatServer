import proto.entities.chitchat_pb2 as chitchat_pb
from dao.mongodb import MongoDBHelper
from dao.base_dao import BaseDao


class ChitchatDA(MongoDBHelper, BaseDao):

    coll = "___chitchat_db___chitchats___"

    async def add_or_update_chitchat(self, chitchat):
        matcher = {
            "id": chitchat.id
        }
        json_obj = self.PH.to_dict(chitchat)
        await self.update_one(matcher, json_obj, upsert=True)

    async def get_chitchat_by_id(self, id):
        return await self.find_one({"id": id})

    async def delete_chitchat(self, id):
        return await self.delete_one({"id": id})

    async def list_chitchat(self, userId):
        async for chitchat in self.find_many(matcher={"userId": userId}):
            yield self.PH.to_obj(chitchat, chitchat_pb.Chitchat)
