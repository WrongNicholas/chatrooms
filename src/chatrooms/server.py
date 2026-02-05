import websockets
from chatrooms.core import Core
from chatrooms.handler import UserHandler
import asyncio

core = Core()

async def handle_connection(websocket):
    """
    Handles a single incoming WebSocket connection.
    """
    handler = UserHandler(websocket, core)
    await handler.handle()

async def server():
    """
    Starts the WebSocket server and runs it indefinitely.
    """
    # TODO: switch to some "0.0.0.0" to enable port forwarding
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("Server listening on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(server())
