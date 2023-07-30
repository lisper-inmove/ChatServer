import proto.api.api_user_pb2 as api_user_pb
import proto.entities.user_pb2 as user_pb
import proto.api.api_common_pb2 as api_common_pb

from handlers.base_handler import BaseHandler
from manager.user_manager import UserManager
from errors import PopupError
from errors import PopupSpecError
from submodules.utils.jwt_util import JWTUtil
from submodules.utils.jwt_util import TokenExpiredException


class UserHandler(BaseHandler):

    PN = [
        api_common_pb.Action.LOGIN,
        api_common_pb.Action.SIGN_UP,
        api_common_pb.Action.TOKEN_AUTHORIZE
    ]

    async def __call__(self, request):
        fmaps = {
            api_common_pb.Action.LOGIN: self.login,
            api_common_pb.Action.SIGN_UP: self.sign_up,
            api_common_pb.Action.TOKEN_AUTHORIZE: self.token_authorize,
        }
        f = fmaps.get(self.cpn)
        if not f:
            raise PopupError("Action not Exists")
        async for result in f(request):
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
            raise PopupSpecError(api_common_pb.TOKEN_AUTHORIZE_EXPIRED, "认证已过期,请重新登陆")

    def generate_response(self, user):
        response = api_user_pb.UserCommonResponse()
        response.username = user.username
        response.token = JWTUtil().generate_token({"id": user.id})
        return response
