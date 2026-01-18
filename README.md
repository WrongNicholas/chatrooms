## Software Engineering EECE 3093C Project

A WebSocket-based chat application.

---

## Setup

Clone the repository:
```sh
git clone https://github.com/WrongNicholas/chatrooms.git
cd chatrooms
```

No additional setup required. The Makefile manages the virtual environment and dependencies automatically.

## Running the Application
Run the server:
```sh
make server
```

Run the client:
```sh
make client
```

## Running Tests
```sh
make test
```

This installs test dependencies and runs the full test sweet.

## Cleaning the Environment
```sh
make clean
```
This removes the virtual environment (`.venv`) and generated Python artifacts.

## Requirements
- Python 3.10+
- `make`
