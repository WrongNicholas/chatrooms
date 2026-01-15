## Software Engineering EECE 3093C Project

A chat app.

## Setup

Clone the repository:
```sh
git clone https://github.com/WrongNicholas/chatrooms.git
cd chatrooms
```

Create the Python virtual environment:
```sh
make .venv
```

Activate the virtual environment:
```sh
source .venv/bin/activate
```

Install dependencies:
```sh
make install
```

# Running the Application
Running the server:
```sh
make server
```

Running the client:
```sh
make client
```

# Notes
- All Makefile commands explicitly use the virtual environment's `python` and `pip`.
- You do not need to have the virtual environment active to run `make` commands.
