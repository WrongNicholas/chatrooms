# main.py
import asyncio
import websockets

async def sender(ws):
    while True:
        msg = await asyncio.to_thread(input, "> ")
        await ws.send(msg)

async def receiver(ws):
    async for msg in ws:
        print(msg)

async def client():
    server_id: str = input("Enter a server to join: ")
    username: str = input("Enter a username: ")

    async with websockets.connect("ws://localhost:8765") as ws:
        await ws.send(f"{server_id}:{username}")

        await asyncio.gather(
            sender(ws),
            receiver(ws),
        )


if __name__ == "__main__":
    asyncio.run(client())
