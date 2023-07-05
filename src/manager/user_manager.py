import proto.user_pb2 as user_pb
from manager.base_manager import BaseManager
from dao.user_dao import UserDA


class UserManager(BaseManager):

    @property
    def da(self):
        if self._da is None:
            self._da = UserDA()
        return self._da

    def create_user(self, request):
        user = self.create_obj(user_pb.User)

    def sign_up(self, request):
        pass
