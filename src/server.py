import websockets
from core import Core
from handler import Handler
import asyncio

core = Core()

async def server_entry(websocket):
    handler = Handler(websocket, core)
    await handler.handle()

async def main():
    async with websockets.serve(server_entry, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
