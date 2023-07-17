import asyncio
import hashlib

import proto.api.api_user_pb2 as api_user_pb
import proto.api.api_common_pb2 as api_common_pb
from submodules.utils.protobuf_helper import ProtobufHelper
from tester import main


async def send(client):
    _request = api_user_pb.UserSignUpRequest()
    _request.username = "inmove"
    _request.password = hashlib.md5("Allen123453#".encode()).hexdigest()
    protocol = api_common_pb.Protocol()
    protocol.action = api_common_pb.ProtocolNumber.SIGN_UP
    protocol.content = ProtobufHelper.to_json_v2(_request)
    await client.send(protocol.SerializeToString())


# Run the main function
asyncio.run(main(send))
