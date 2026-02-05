from chatrooms.user import User

class Core:
    """ 
    Manages users grouped by room ID. 
    """
    def __init__(self) -> None:
        self.rooms: dict[str, set[User]] = {}

    """
    Adds a user to a room.
    """
    def join(self, room_id: str, user: User):
        self.rooms.setdefault(room_id, set()).add(user)
        print(f"'{user.name}' has joined room '{room_id}'")

    """
    Removes a user from a room.
    """
    def leave(self, room_id: str, user: User):
        if room_id in self.rooms and user in self.rooms[room_id]:
            self.rooms[room_id].remove(user)
            print(f"'{user.name}' has left room '{room_id}'")
