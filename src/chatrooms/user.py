from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class User:
    """ 
    Represents a connected user.
    """
    name: str
    websocket: Any
