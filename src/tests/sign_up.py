import asyncio
import json
import websockets
import hashlib

from asyncio import Queue

import api.user_pb2 as user_pb
from submodules.utils.protobuf_helper import ProtobufHelper


messages = Queue()


async def send(client):
    request = user_pb.UserSignUpRequest()
    request.username = "inmove"
    request.password = hashlib.md5("Allen123453#".encode()).hexdigest()
    message = ProtobufHelper.to_json_v2(request)
    protocol = 0x02.to_bytes(2)
    message = (protocol + message.encode()).decode()
    await client.send(message)


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
