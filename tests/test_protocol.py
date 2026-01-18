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

def test_generate_message_creates_chat_message():
    message = generate_message("hello world")

    assert isinstance(message, ChatMessage)
    assert message.type == "message"
    assert message.contents == "hello world"

def test_generate_message_creates_command_message():
    message = generate_message("/help")

    assert isinstance(message, CommandMessage)
    assert message.type == "command"
    assert message.command == "help"

def test_serialize_message_properly_serializes_chat_message():
    message = ChatMessage(type="message", contents="hello world")

    expected = '{"type": "message", "contents": "hello world"}'
    actual = serialize_message(message)

    assert expected == actual

def test_serialize_message_properly_serializes_command_message():
    message = CommandMessage(type="command", command="help")

    expected = '{"type": "command", "command": "help"}'
    actual = serialize_message(message)

    assert expected == actual

def test_serialize_message_properly_serializes_join_message():
    message = JoinMessage(type="join", server_id="my_server_id", user_name="my_user_name")

    expected = '{"type": "join", "server_id": "my_server_id", "user_name": "my_user_name"}'
    actual = serialize_message(message)

    assert expected == actual

def test_serialize_message_properly_serializes_error_message():
    message = ErrorMessage(type="error", error="this is an error")

    expected = '{"type": "error", "error": "this is an error"}'
    actual = serialize_message(message)

    assert expected == actual


