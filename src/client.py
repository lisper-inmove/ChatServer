import json
from manager.user_manager import UserManager
from submodules.utils.jwt_util import JWTUtil


class Client:

    def __init__(self):
        self.isAuthorized = False
