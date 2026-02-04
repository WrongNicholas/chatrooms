import asyncio
import websockets
from chatrooms.message import ChatMessage, JoinMessage, ErrorMessage
from chatrooms.protocol import generate_message, serialize_message, parse_message

async def sender(ws):
    """Handles sending messages to the server."""
    while True:
        try:
            contents = await asyncio.to_thread(input, "> ")
            msg = generate_message(contents)
            serialized_message = serialize_message(msg)
            await ws.send(serialized_message)
        except websockets.exceptions.ConnectionClosed:
            break;

async def receiver(ws):
    """Handles messages received from the server."""
    async for msg in ws:
        parsed_message = parse_message(msg)
        if type(parsed_message) == ChatMessage:
            print(parsed_message.contents)

async def client():
    """Connects to the server and runs the send/receive tasks."""
    server_id: str = input("Enter a server to join: ")
    async with websockets.connect("ws://localhost:8765") as ws:
    
        joined = False
        while not joined:
            user_name: str = input("Enter a username: ")
            join_message = JoinMessage(type="join", server_id=server_id, user_name=user_name)
            serialized_join_message = serialize_message(join_message)
            await ws.send(serialized_join_message)
            server_response = await ws.recv()
            parsed_message = parse_message(server_response)
            if type(parsed_message) == ErrorMessage:
                print(parsed_message.error)
            else:
                joined = True

        await asyncio.gather(
            sender(ws),
            receiver(ws),
        )
   

   



if __name__ == "__main__":
    asyncio.run(client())
