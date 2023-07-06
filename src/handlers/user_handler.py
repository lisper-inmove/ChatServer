import api.user_pb2 as api_user_pb
import proto.user_pb2 as user_pb

from handlers.base_handler import BaseHandler
from manager.user_manager import UserManager
from errors import PopupError
from submodules.utils.jwt_util import JWTUtil


class UserHandler(BaseHandler):

    LOGIN = 0x01
    SIGN_UP = 0x02
    PN = [LOGIN, SIGN_UP]

    async def __call__(self, request):
        if self.cpn == self.LOGIN:
            async for result in self.login(request):
                yield result
        elif self.cpn == self.SIGN_UP:
            async for result in self.sign_up(request):
                yield result

    async def login(self, request):
        manager = UserManager()
        user_request = self.PH.to_obj_v2(
            request, api_user_pb.UserLoginRequest
        )
        user = await manager.get_user_by_username_password(
            user_request.username,
            user_request.password
        )
        if not user:
            raise PopupError("用户不存在")
        yield self.generate_response(user)

    async def sign_up(self, request):
        manager = UserManager()
        user_request = self.PH.to_obj_v2(
            request, api_user_pb.UserSignUpRequest
        )
        user = manager.create_user(user_request)
        user.username = user_request.username
        user.password = user_request.password
        manager.add_user(user)
        yield self.generate_response(user)

    def generate_response(self, user):
        response = api_user_pb.UserCommonResponse()
        response.username = user.username
        response.token = JWTUtil().generate_token({"id": user.id})
        return response
