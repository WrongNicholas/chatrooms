## Software Engineering EECE 3093C Project

A chat app.

## Windows

After cloning:
```sh
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
```

# Run the server
```sh
python src/server.py
```

# Run the client
```sh
python src/client.py
```

## Setup UNIX

After cloning:

```sh
make .venv
make install
```

# Run the server
```sh
make server
```

# Run the client
```sh
make client
```

# Note
The server runs on:
```sh
ws://localhost:8675
```
