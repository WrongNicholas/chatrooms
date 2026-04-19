from chatrooms.user import User

class Core:
    """ 
    Manages users grouped by room ID. 
    """
    def __init__(self) -> None:
        self.rooms: dict[str, set[User]] = {}
        self.admins: dict[str, User] = {}

    """
    Adds a user to a room.
    """
    def join(self, room_id: str, user: User):
        self.rooms.setdefault(room_id, set()).add(user)

        if room_id not in self.admins:
            self.admins[room_id] = user

        print(f"'{user.name}' has joined room '{room_id}'")

    """
    Removes a user from a room.
    """
    def leave(self, room_id: str, user: User):
        if room_id in self.rooms and user in self.rooms[room_id]:
            self.rooms[room_id].remove(user)
            print(f"'{user.name}' has left room '{room_id}'")

            if self.admins.get(room_id) == user:
                if self.rooms[room_id]:
                    self.admins[room_id] = next(iter(self.rooms[room_id]))
                else:
                    del self.admins[room_id]

            if not self.rooms[room_id]:
                del self.rooms[room_id]

    """
    Swaps users room.
    """
    def swap(self, old_room_id: str, user: User, new_room_id: str):
        self.leave(old_room_id, user)
        self.join(new_room_id, user)

    """
    Handles user kicked.
    """
    async def kick(self, room_id: str, user: User):
        # good enough probably
        self.leave(room_id, user)
        await user.websocket.close()
