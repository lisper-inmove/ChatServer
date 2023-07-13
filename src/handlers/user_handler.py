import proto.api.api_user_pb2 as api_user_pb
import proto.entities.user_pb2 as user_pb
import proto.api.api_common_pb2 as api_common_pb

from handlers.base_handler import BaseHandler
from manager.user_manager import UserManager
from errors import PopupError
from submodules.utils.jwt_util import JWTUtil
from submodules.utils.jwt_util import TokenExpiredException


class UserHandler(BaseHandler):

    PN = [
        api_common_pb.ProtocolNumber.LOGIN,
        api_common_pb.ProtocolNumber.SIGN_UP,
        api_common_pb.ProtocolNumber.TOKEN_AUTHORIZE
    ]

    async def __call__(self, request):
        if self.cpn == api_common_pb.ProtocolNumber.LOGIN:
            async for result in self.login(request):
                yield result
        elif self.cpn == api_common_pb.ProtocolNumber.SIGN_UP:
            async for result in self.sign_up(request):
                yield result
        elif self.cpn == api_common_pb.ProtocolNumber.TOKEN_AUTHORIZE:
            async for result in self.token_authorize(request):
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
        self.user = user
        yield self.generate_response(user)

    async def sign_up(self, request):
        manager = UserManager()
        user_request = self.PH.to_obj_v2(
            request, api_user_pb.UserSignUpRequest
        )
        user = manager.create_user(user_request)
        user.username = user_request.username
        user.password = user_request.password
        await manager.add_user(user)
        self.user = user
        yield self.generate_response(user)

    async def token_authorize(self, request):
        user_request = self.PH.to_obj_v2(request, api_user_pb.TokenAuthorizeRequest)
        try:
            manager = UserManager()
            payload = JWTUtil().decode(user_request.token)
            id = payload.get("id")
            user = await manager.get_user_by_id(id)
            self.user = user
            yield self.generate_response(user)
        except TokenExpiredException as ex:
            raise PopupError("认证已过期,请重新登陆")

    def generate_response(self, user):
        response = api_user_pb.UserCommonResponse()
        response.username = user.username
        response.token = JWTUtil().generate_token({"id": user.id})
        return response
