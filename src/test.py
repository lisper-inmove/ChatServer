import asyncio
import json
import websockets

from asyncio import Queue


messages = Queue()


async def send(client):
    # 发送消息
    while True:
        c = input("What's your message?: ")
        if c == 'q':
            break
        message = json.dumps({
            "messages": [{'role': 'user', "content": c}]
        })
        print(f"client send: {message}")
        await client.send(message)
        await asyncio.sleep(5)


async def recv(client):
    while True:
        while True:
            reply = await client.recv()
            if not reply:
                break
            print(f'server reply: {reply}')
        await asyncio.sleep(5)


async def main():
    # Schedule both the tasks to run
    uri = "wss://chat.inmove.top/ws"  # WebSocket 服务器的地址
    client = await websockets.connect(uri)
    await asyncio.gather(send(client), recv(client))


# Run the main function
asyncio.run(main())
