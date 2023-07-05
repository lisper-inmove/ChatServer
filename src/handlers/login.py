import api.user_pb2 as user_pb

from handlers.base_handler import BaseHandler
from entities.user import User, UserDA
from handlers.user_helper import UserHelper
from submodules.utils.protobuf_helper import ProtobufHelper


class LoginHandler(BaseHandler):

    def __call__(self, request):
        user_request = ProtobufHelper.to_obj_v2(request.content, user_pb.UserLoginRequest)
        user = User()
        user.username = user_request.username
        user.password = user_request.password
        user = UserDA().login(user)
        yield UserHelper().generate_response(user)
