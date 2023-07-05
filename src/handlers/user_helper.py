import json
import api.protocol_pb2 as protocol_pb
from submodules.utils.jwt_util import JWTUtil


class UserHelper:

    def generate_response(self, user):
        response = protocol_pb.Response()
        response.is_complete = True
        response.content = json.dumps({
            "username": user.username,
            "token": JWTUtil().generate_token({
                "id": user.id
            }).decode()
        })
        return response
