import json

from chatrooms.protocol import (
    generate_message,
    serialize_message,
    parse_message,
)

from chatrooms.message import (
    ChatMessage,
    CommandMessage,
    JoinMessage,
    ErrorMessage,
)

def test_enerate_message_creates_chat_message():
    message = generate_message("hello world")

    assert isinstance(message, ChatMessage)
    assert message.type == "message"
    assert message.contents == "hello world"

def test_should_fail():
    assert False
