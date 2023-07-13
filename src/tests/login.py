import asyncio
import json
import websockets
import hashlib

from asyncio import Queue

import proto.api.api_user_pb2 as api_user_pb
import proto.api.api_common_pb2 as api_common_pb
from submodules.utils.protobuf_helper import ProtobufHelper


messages = Queue()


async def send(client):
    _request = api_user_pb.UserLoginRequest()
    _request.username = "inmove"
    _request.password = hashlib.md5("Allen123453#".encode()).hexdigest()
    message = api_common_pb.Protocol()
    message.action = 0x01
    message.content = ProtobufHelper.to_json_v2(_request)
    await client.send(message.SerializeToString())

async def recv(client):
    await asyncio.sleep(5)
    while True:
        reply = await client.recv()
        if not reply:
            break
        print(f'server reply: {reply}')


async def main():
    # uri = "wss://ai.inmove.top/ChatServer"  # WebSocket 服务器的地址
    uri = "ws://127.0.0.1:8765"  # WebSocket 服务器的地址
    client = await websockets.connect(uri)
    await asyncio.gather(send(client), recv(client))


# Run the main function
asyncio.run(main())
