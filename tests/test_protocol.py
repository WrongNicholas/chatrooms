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

def test_parse_message_properly_parses_chat_message():
    raw_message = '{"type": "message", "contents": "hello world"}'
    parsed_message = parse_message(raw_message)    

    assert isinstance(parsed_message, ChatMessage)
    assert parsed_message.type == "message"
    assert parsed_message.contents == "hello world"

def test_parse_message_properly_parses_command_message():
    raw_message = '{"type": "command", "command": "leave"}'
    parsed_message = parse_message(raw_message)    

    assert isinstance(parsed_message, CommandMessage)
    assert parsed_message.type == "command"
    assert parsed_message.command == "leave"

def test_parse_message_properly_parses_join_message():
    raw_message = '{"type": "join", "server_id": "my_server_id", "user_name": "my_user_name"}'
    parsed_message = parse_message(raw_message)    

    assert isinstance(parsed_message, JoinMessage)
    assert parsed_message.type == "join"
    assert parsed_message.server_id == "my_server_id"
    assert parsed_message.user_name == "my_user_name"

def test_parse_message_properly_parses_error_message():
    raw_message = '{"type": "error", "error": "this is an error message"}'
    parsed_message = parse_message(raw_message)    

    assert isinstance(parsed_message, ErrorMessage)
    assert parsed_message.type == "error"
    assert parsed_message.error == "this is an error message"

def test_parse_message_returns_error_message_on_invalid_json():
    raw_message = 'this is not valid json'
    parsed_message = parse_message(raw_message)

    assert isinstance(parsed_message, ErrorMessage)
    assert parsed_message.type == "error"
    assert parsed_message.error == "JSON loads error!"

def test_parse_message_returns_error_message_on_invalid_message_type():
    raw_message = '{"type": "invalid", "contents": "something"}'
    parsed_message = parse_message(raw_message)

    assert isinstance(parsed_message, ErrorMessage)
    assert parsed_message.type == "error"
    assert parsed_message.error == "Some error in generating a message type!"

def test_parse_message_returns_error_on_no_type():
    raw_message = '{"contents":"some contents"}'
    parsed_message = parse_message(raw_message)

    assert isinstance(parsed_message, ErrorMessage)
    assert parsed_message.type == "error"
    assert parsed_message.error == "Missing message type!"
