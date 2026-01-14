# handler.py
from core import Core
from user import User

class Handler:
    def __init__(self, websocket, core: Core) -> None:
        self.websocket = websocket
        self.core = core
        self.user = None
        self.server_id = None


    async def handle(self):
        try:
            join_message = await self.websocket.recv()
            self.server_id, username = parse_join(join_message)

            self.user = User(username, self.websocket)
            self.core.join(self.server_id, self.user)

            async for msg in self.websocket:
                await self.broadcast(msg)
        finally:
            if self.user and self.server_id:
                self.core.leave(self.server_id, self.user)


    async def broadcast(self, msg: str):
        if self.server_id is not None:
            for user in self.core.dictionary[self.server_id]:
                if user != self.user:
                    print(f"Broadcasting to server: {self.server_id}: {msg}")
                    await user.websocket.send(msg)


def parse_join(msg: str) -> tuple[str, str]:
    first, second = msg.split(':', 1)
    return (first, second)
