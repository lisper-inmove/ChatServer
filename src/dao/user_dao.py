from pymongo.errors import DuplicateKeyError

import proto.entities.user_pb2 as user_pb
from dao.mongodb import MongoDBHelper
from dao.base_dao import BaseDao
from errors import PopupError
from submodules.utils.logger import Logger

logger = Logger()


class UserDA(MongoDBHelper, BaseDao):

    coll = "___user_db___users___"

    async def add_user(self, user):
        matcher = {
            'id': user.id
        }
        json_data = self.PH.to_dict(user)
        try:
            await self.update_one(matcher, json_data, upsert=True)
        except DuplicateKeyError as err:
            logger.error(str(err))
            if "".join(err.details.get("keyValue").keys()) == 'username':
                raise PopupError("用户名已存在")

    async def get_user_by_id(self, id):
        matcher = {'id': id}
        user = await self.find_one(matcher)
        return self.PH.to_obj(user, user_pb.User)

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
