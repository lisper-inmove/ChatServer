import asyncio
import hashlib

import proto.api.api_user_pb2 as api_user_pb
import proto.api.api_common_pb2 as api_common_pb
from submodules.utils.protobuf_helper import ProtobufHelper
from tester import main


async def send(client):
    _request = api_user_pb.UserLoginRequest()
    _request.username = "inmove"
    _request.password = hashlib.md5("Allen123453#".encode()).hexdigest()
    message = api_common_pb.Protocol()
    message.action = api_common_pb.ProtocolNumber.LOGIN
    message.content = ProtobufHelper.to_json_v2(_request)
    await client.send(message.SerializeToString())


# Run the main function
asyncio.run(main(send))
