import api.user_pb2 as user_pb

from handlers.base_handler import BaseHandler
from handlers.user_helper import UserHelper
from entities.user import User, UserDA
from submodules.utils.misc import Misc
from submodules.utils.idate import IDate
from submodules.utils.protobuf_helper import ProtobufHelper


class SignUpHandler(BaseHandler):

    def __call__(self, request):
        user_request = ProtobufHelper.to_obj_v2(request.content, user_pb.UserSignUpRequest)
        user = User()
        user.id = Misc.uuid()
        user.username = user_request.username
        user.password = user_request.password
        user.create_time = IDate.now_timestamp()
        user.update_time = IDate.now_timestamp()
        UserDA().sign_up(user)
        yield UserHelper().generate_response(user)
