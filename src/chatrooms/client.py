import asyncio
from typing import Callable, Any
import websockets
from chatrooms.message import ChatMessage, JoinMessage, Message
from chatrooms.protocol import generate_message, serialize_message, parse_message


class ChatClient:
    """
    A client class that handles the websocket connection,
    sending messages, and receiving messages.
    """
    def __init__(self, url: str = "ws://localhost:8765") -> None:
        self.url: str = url
        self.ws: Any = None
        self.room_id: str = ""
        self.user_name: str = ""

    async def connect(self, room_id: str, user_name: str) -> None:
        """Connects to the server and sends the initial join message."""
        if not room_id or not user_name:
            raise ValueError("Room ID and User Name cannot be empty.")
        
        self.room_id = room_id
        self.user_name = user_name
        
        self.ws = await websockets.connect(self.url)

        
        join_message = JoinMessage(type="join", room_id=room_id, user_name=user_name)
        await self.ws.send(serialize_message(join_message))

    async def send_message(self, content: str) -> None:
        """Sends a message to the server."""
        if self.ws:
            msg: Message = generate_message(content)
            serialized_message: str = serialize_message(msg)
            await self.ws.send(serialized_message)

    async def listen(self, message_callback: Callable) -> None:
        """ Listens for messages indefinitely."""
        try:
            async for msg in self.ws:
                parsed_message = parse_message(msg)

                if isinstance(parsed_message, ChatMessage):
                    message_callback(parsed_message.contents)

        except websockets.exceptions.ConnectionClosed:
            message_callback("System: Connection closed.")

    async def close(self) -> None:
        if self.ws:
            await self.ws.close()


#Existing CLI Implementation

async def cli_sender(client: ChatClient) -> None:
    """CLI-specific sender loop."""
    while True:
        try:
            contents: str = await asyncio.to_thread(input, "")
            await client.send_message(contents)
        except (KeyboardInterrupt):
            break


async def run_cli_client() -> None:
    """Main entry point for the Terminal Client."""
    room_id: str = input("Enter a room to join: ")
    user_name: str = input("Enter a username: ")
    client: ChatClient = ChatClient()
    
    try:
        await client.connect(room_id, user_name)
        
        await asyncio.gather(
            cli_sender(client),
            client.listen(print)
        )

    except Exception as e:
        print(f"Could not connect: {e}")
    finally:
        await client.close()


if __name__ == "__main__":
    try:
        asyncio.run(run_cli_client())
    except KeyboardInterrupt:
        print("\nExiting...")