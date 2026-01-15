from dataclasses import dataclass

@dataclass(frozen=True)
class Message:
    """Base class for all protocol messages."""
    type: str

@dataclass(frozen=True)
class JoinMessage(Message):
    """Sent by a client to join a server."""
    server_id: str
    user_name: str

@dataclass(frozen=True)
class ChatMessage(Message):
    """Represents a chat message sent to/from server."""
    contents: str

@dataclass(frozen=True)
class CommandMessage(Message):
    """Represents a command message sent to server."""
    command: str

@dataclass(frozen=True)
class ErrorMessage(Message):
    """Represents some error as a Message."""
    error: str
