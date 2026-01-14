from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class User:
    name: str
    websocket: Any
