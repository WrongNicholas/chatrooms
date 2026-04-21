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
        self.user: User
        self.room_id = None


    async def handle(self):
        """
        Handles the connection lifecycle for the user.
        """
        try:
            async for raw in self.websocket:
                msg = parse_message(raw)
                if type(msg) == JoinMessage:
                    # Set up this handler
                    self.room_id = msg.room_id
                    self.user = User(msg.user_name, self.websocket)
                    self.core.join(self.room_id, self.user)

                    # Construct and broadcast chat message on join
                    join_broadcast = ChatMessage(type="message", sender="", contents=f"{msg.user_name} has joined the room.")
                    serialized_join_broadcast : str = serialize_message(join_broadcast)
                    await self.broadcast(serialized_join_broadcast)

                elif type(msg) == ChatMessage:
                    await self.broadcast(raw)
                elif type(msg) == ErrorMessage:
                    print(f"ERROR: ErrorMessage: {msg.error}")
                elif type(msg) == CommandMessage:
                    await self.handle_command(msg)
        finally:
            if self.user and self.room_id:
                self.core.leave(self.room_id, self.user)


    async def broadcast(self, msg: str) -> None:
        """
        Broadcasts a message to all other users in the same room.
        """
        if self.room_id is not None:
            for user in self.core.rooms[self.room_id]:
                if user != self.user:
                    print(f"Broadcasting ChatMessage to room: {self.room_id}: {msg}")
                    await user.websocket.send(msg)


    async def handle_command(self, msg: CommandMessage) -> None:
        """
        Handles CommandMessages sent to the server.
        """
        if msg.command == "leave":
            await self.user_leave()
        elif msg.command == "swap":
            await self.user_swap(msg.args)
        elif msg.command == "kick":
            await self.user_kick(msg.args)
        else:
            await self.user.websocket.send(serialize_message(ChatMessage(
                type="message",
                sender="SERVER",
                contents="Command not found! Available commands:\n /leave\n /swap <room_id>"
            )))


    async def user_leave(self) -> None:
        """
        Handles this user leaving the room.
        """
        if self.user and self.room_id:
            # Construct and broadcast chat message on leave
            leave_broadcast = ChatMessage(type="message", sender="", contents=f"{self.user.name} has left the room.")
            serialized_leave_broadcast : str = serialize_message(leave_broadcast)
            await self.broadcast(serialized_leave_broadcast)

            # Remove user from core dictionary
            self.core.leave(self.room_id, self.user)
            await self.websocket.close()

    async def user_swap(self, new_room_id: str) -> None:
        """
        Handles this user changing rooms.
        """
        if self.user and self.room_id:
            # Construct and broadcast chat message on leave
            leave_broadcast = ChatMessage(type="message", sender="", contents=f"{self.user.name} has left the room.")
            serialized_leave_broadcast : str = serialize_message(leave_broadcast)
            await self.broadcast(serialized_leave_broadcast)

            # Swap user in core dictionary, don't close websocket
            self.core.swap(self.room_id, self.user, new_room_id)
            # Swap handler room referenced
            self.room_id = new_room_id

    async def user_kick(self, user_to_kick: str) -> None:
        """
        Kicks user from this room.
        """
        if not (self.user and self.room_id):
            return

        if self.core.admins.get(self.room_id) != self.user:
            return

        # ignore how terrible this is, I refuse to refactor
        room_users = self.core.rooms.get(self.room_id, set())
        about_to_kick_rocks = next((u for u in room_users if u.name == user_to_kick), None)

        if not about_to_kick_rocks:
            return

        await self.core.kick(self.room_id, about_to_kick_rocks)

        kick_message = ChatMessage(type="message", sender="", contents=f"{self.user.name} has kicked {about_to_kick_rocks.name}")
        serialized_kick_message : str = serialize_message(kick_message)

        await self.broadcast(serialized_kick_message)
