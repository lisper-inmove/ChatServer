import asyncio
import websockets


async def default_recv(client):
    await asyncio.sleep(5)
    while True:
        reply = await client.recv()
        if not reply:
            break
        print(f'server reply: {reply}')


async def main(sends, recv=None):
    # uri = "wss://ai.inmove.top/ChatServer"  # WebSocket 服务器的地址
    uri = "ws://127.0.0.1:8765"  # WebSocket 服务器的地址
    client = await websockets.connect(uri)
    if recv is None:
        recv = default_recv
    if not isinstance(sends, list):
        sends = [sends]
    sends.append(recv)
    print(sends)
    await asyncio.gather(*[s(client) for s in sends])
