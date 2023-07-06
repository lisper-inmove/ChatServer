import proto.user_pb2 as user_pb
from dao.mongodb import MongoDBHelper
from dao.base_dao import BaseDao


class UserDA(MongoDBHelper, BaseDao):

    coll = "___user_db___users___"

    def add_user(self, user):
        matcher = {
            'id': user.id
        }
        json_data = self.PH.to_dict(user)
        self.update_one(matcher, json_data, upsert=True)

    def get_user_by_id(self, id):
        matcher = {'id': id}
        user = self.find_one(matcher, user_pb.User)
        return user

    async def get_user_by_condition(self, **kargs):
        user = await self.__get_user_by_username_password(
            username=kargs.get("username"),
            password=kargs.get("password")
        )
        return self.PH.to_obj(user, user_pb.User)

    async def __get_user_by_username_password(self, username, password):
        if None in (username, password):
            return None
        matcher = {
            "username": username,
            "password": password
        }
        user = await self.find_one(matcher)
        return user
