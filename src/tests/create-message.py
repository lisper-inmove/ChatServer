import asyncio

import proto.api.api_chitchat_pb2 as api_chitchat_pb
import proto.api.api_common_pb2 as api_common_pb
from submodules.utils.protobuf_helper import ProtobufHelper

from token_authorize import send as token_authorize_send
from tester import main


async def send(client):
    _request = api_chitchat_pb.CreateMessageRequest()
    _request.role = "USER"
    _request.content = "Hello Can you create a hello world program using Rust"
    protocol = api_common_pb.Action()
    protocol.action = api_common_pb.Action.CREATE_MESSAGE
    protocol.content = ProtobufHelper.to_json_v2(_request)
    await client.send(protocol.SerializeToString())


if __name__ == '__main__':
    asyncio.run(main(sends=[token_authorize_send, send]))
