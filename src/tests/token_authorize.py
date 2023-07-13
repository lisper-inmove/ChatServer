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
    _request = api_user_pb.TokenAuthorizeRequest()
    _request.token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjA3NzUwNjU3LWE3NDUtNDQ4OS1iN2FhLThjY2I1NTVmNDk2ZSIsImNyZWF0ZV90aW1lIjoxNjg5MjE1MzQ3LCJleHBpcmVfYXQiOjE2ODk4MjAxNDcsIm5lZWRfbG9naW4iOmZhbHNlLCJyYW5kb21fdmFsdWUxIjo3OTkxMDYsInJhbmRvbV92YWx1ZTIiOjYzMDQ0Nn0.tV_6QQe4sVX89Up3bJ_YXH-muYMMgh9RKGeTpMXn8RI"
    message = api_common_pb.Protocol()
    message.action = api_common_pb.ProtocolNumber.TOKEN_AUTHORIZE
    message.content = ProtobufHelper.to_json_v2(_request)
    # await client.send(ProtobufHelper.to_json_v2(message))
    await client.send(message.SerializeToString())

async def recv(client):
    await asyncio.sleep(5)
    while True:
        reply = await client.recv()
        if not reply:
            break
        print(f'server reply: {reply}')


async def main():
    # uri = "wss://chat.inmove.top/ws"  # WebSocket 服务器的地址
    uri = "ws://127.0.0.1:8765"  # WebSocket 服务器的地址
    client = await websockets.connect(uri)
    await asyncio.gather(send(client), recv(client))


# Run the main function
asyncio.run(main())
