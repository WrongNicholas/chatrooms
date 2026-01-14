from user import User

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
        if server_id in self.dictionary:
            self.dictionary[server_id].remove(user)
            print(f"'{user.name}' has left server '{server_id}'")
