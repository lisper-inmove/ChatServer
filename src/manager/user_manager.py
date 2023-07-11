import proto.entities.user_pb2 as user_pb
from manager.base_manager import BaseManager
from dao.user_dao import UserDA


class UserManager(BaseManager):

    @property
    def dao(self):
        if self._dao is None:
            self._dao = UserDA()
        return self._dao

    def create_user(self, request):
        user = self.create_obj(user_pb.User)
        user.username = request.username
        user.password = request.password
        return user

    async def add_user(self, user):
        if not user:
            return
        self.update_obj(user)
        await self.dao.add_user(user)

    async def get_user_by_username_password(self, username, password):
        user = await self.dao.get_user_by_condition(
            username=username,
            password=password
        )
        return user
