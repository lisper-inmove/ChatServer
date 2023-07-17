import asyncio
import hashlib

import proto.api.api_chitchat_pb2 as api_chitchat_pb
import proto.api.api_common_pb2 as api_common_pb
from submodules.utils.protobuf_helper import ProtobufHelper

from tester import main


async def send(client):
    _request = api_chitchat_pb.StopGenerateRequest()
    message = api_common_pb.Protocol()
    message.action = api_common_pb.ProtocolNumber.STOP_GENERATE
    message.content = ProtobufHelper.to_json_v2(_request)
    await client.send(message.SerializeToString())


# Run the main function
asyncio.run(main(send))
