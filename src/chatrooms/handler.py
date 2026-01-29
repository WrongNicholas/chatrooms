# handler.py
from chatrooms.core import Core
from chatrooms.message import ChatMessage, CommandMessage, ErrorMessage, JoinMessage
from chatrooms.protocol import parse_message, serialize_message
from chatrooms.user import User

class UserHandler:
    """
    Handles a single user's WebSocket connection.
    """
    def __init__(self, websocket, core: Core) -> None:
        self.websocket = websocket
        self.core = core
        self.user = None
        self.server_id = None
###PENIS

    async def handle(self):
        """
        Handles the connection lifecycle for the user.
        """
        try:
            async for raw in self.websocket:
                msg = parse_message(raw)
                if type(msg) == JoinMessage:
                    self.server_id = msg.server_id
                    self.user = User(msg.user_name, self.websocket)
                    self.core.join(self.server_id, self.user)
                elif type(msg) == ChatMessage:
                    await self.broadcast(raw)
                elif type(msg) == ErrorMessage:
                    print(f"ERROR: ErrorMessage: {msg.error}")
                elif type(msg) == CommandMessage:
                    await self.handle_command(msg)
        finally:
            if self.user and self.server_id:
                self.core.leave(self.server_id, self.user)


    async def broadcast(self, msg: str) -> None:
        """
        Broadcasts a message to all other users in the same server.
        """
        if self.server_id is not None:
            for user in self.core.dictionary[self.server_id]:
                if user != self.user:
                    print(f"Broadcasting ChatMessage to server: {self.server_id}: {msg}")
                    await user.websocket.send(msg)

    async def handle_command(self, msg: CommandMessage) -> None:
        """
        Handles CommandMessages sent to the server.
        """
        if msg.command == "leave":
            await self.user_leave()
        else:
            # TODO: probably fix whatever the hell this is
            await self.user.websocket.send(serialize_message(ChatMessage(
                type="message",
                contents="Command not found! Available commands:\n /leave"
            )))

    async def user_leave(self) -> None:
        """
        Handles this user leaving the server.
        """
        if self.user and self.server_id:
            self.core.leave(self.server_id, self.user)
            await self.websocket.close()
