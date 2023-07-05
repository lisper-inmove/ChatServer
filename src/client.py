import json
from entities.user import UserDA
from submodules.utils.jwt_util import JWTUtil


class Client:

    def __init__(self, websocket):
        self.websocket = websocket

    async def identity(self):
        identity = await self.websocket.recv()
        identity = json.loads(identity)
        username = identity.get("username")
        password = identity.get("password")
        token = identity.get("token")
        if token is None:
            await self.__identity_by_username_and_password(username, password)
        else:
            await self.__identity_by_token(token)

    async def __identity_by_token(self, token):
        payload = JWTUtil().decode(token)
        user_id = payload.get("id")
        user_da = UserDA()

    async def __identity_by_username_and_password(self, username, password):
        pass
