from dao.mongodb import MongoDBHelper
from dao.base_dao import BaseDao


class ChitchatDA(MongoDBHelper, BaseDao):

    coll = "___chitchat_db___chitchats___"

    async def create_chitchat(self, chitchat):
        matcher = {
            "id": chitchat.id
        }
        json_obj = self.PH.to_dict(chitchat)
        self.update_one(matcher, {"$set": json_obj}, upsert=True)

    async def get_chitchat_by_id(self, id):
        return await self.find_one({"id": id})

    async def list_chitchat(self, user_id):
        return await self.find_many(matcher={"user_id": user_id})
