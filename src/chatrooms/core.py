from chatrooms.user import User

class Core:
    """ 
    Manages users grouped by server ID. 
    """
    def __init__(self) -> None:
        self.dictionary: dict[str, set[User]] = {}

    def join(self, server_id: str, user: User):
        self.dictionary.setdefault(server_id, set()).add(user)
        print(f"'{user.name}' has joined server '{server_id}'")

    def leave(self, server_id: str, user: User):
        if server_id in self.dictionary and user in self.dictionary[server_id]:
            self.dictionary[server_id].remove(user)
            print(f"'{user.name}' has left server '{server_id}'")
    def username_taken(self, server_id: str, username: str):
        if server_id not in self.dictionary:
            return False
        for user in self.dictionary[server_id]:
            if user.name == username:
                return True
        return False