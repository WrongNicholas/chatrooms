import json
from typing import Any
from chatrooms.message import Message, JoinMessage, ChatMessage, CommandMessage, ErrorMessage
from dataclasses import asdict

"""
Message protocol utilities.
"""

def generate_message(contents: str) -> Message:
    """
    Creates Messages from raw input. Commands are inferred from leading '/'.
    """
    if contents.startswith("/"):
        return CommandMessage(
            type="command",
            command=contents[1:]
        )
    else:
        return ChatMessage(
            type="message",
            contents=contents
        )

def serialize_message(message: Message) -> str:
    """
    Serializes a Message into a JSON string.
    """
    return json.dumps(asdict(message))

def parse_message(raw_message: str) -> Message:
    """
    Parses a JSON string into a Message.

    Returns an ErrorMessage if some failure.
    """
    try:
        data: dict[str, Any] = json.loads(raw_message)
    except:
        return generate_error_message("JSON loads error!")
    message_type = data.get("type")
    if not message_type:
        return generate_error_message("Missing message type!")

    if message_type == "join":
        return JoinMessage(
            type="join", 
            server_id=data["server_id"], 
            user_name=data["user_name"]
        )
    elif message_type == "message":
        return ChatMessage(
            type="message",
            contents=data["contents"]
        )
    elif message_type == "command":
        return CommandMessage(
            type="command",
            command=data["command"]
        )
    elif message_type == "error":
        return ErrorMessage(
            type="error",
            error=data["error"]
        )
    return generate_error_message("Some error in generating a message type!")

def generate_error_message(error: str) -> ErrorMessage:
    """
    Creates an ErrorMessage with given error text.
    """
    return ErrorMessage(
        type="error",
        error=error
    )
