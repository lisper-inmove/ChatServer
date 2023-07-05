from .mongodb import MongoDBHelper
from pymongo.errors import DuplicateKeyError
from submodules.utils.logger import Logger
from errors import PopupError

logger = Logger()


class User:

    id: str
    username: str
    password: str
    create_time: int
    update_time: int

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "create_time": self.create_time,
            "update_time": self.update_time
        }


class UserDA(MongoDBHelper):

    coll = "___user_db___users___"

    def sign_up(self, user: User):
        matcher = {
            "id": user.id
        }
        json_data = {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "create_time": user.create_time,
            "update_time": user.update_time
        }
        try:
            self.update_one(matcher, json_data, upsert=True)
        except DuplicateKeyError as err:
            logger.error(str(err))
            if "".join(err.details.get("keyValue").keys()) == 'username':
                raise PopupError("用户名已存在")
        return user

    def login(self, user: User):
        matcher = {
            "username": user.username,
            "password": user.password
        }
        result = self.find_one(matcher)
        user = User()
        if not result:
            raise PopupError("用户名或密码错误")
        user.id = result.get("id")
        user.username = result.get("username")
        user.password = result.get("password")
        user.create_time = result.get("create_time")
        user.update_time = result.get("update_time")
        return user

    def get_user_by_id(self, id: str):
        matcher = {"id": id}
        result = self.find_one(matcher)
        use = User()
        if not result:
            raise PopupError("用户不存在")
