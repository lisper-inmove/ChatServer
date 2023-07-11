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
        chitchat.type = chitchat_pb.Chitchat.Status.Value(request.type)
        return chitchat
