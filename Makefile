PYTHON := python3
VENV := .venv
VPY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.venv:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip

install: .venv
	$(PIP) install -r requirements.txt

server: .venv
	$(VPY) src/server.py

client: .venv
	$(VPY) src/client.py

clean:
	rm -rf $(VENV)

.PHONY: install server client clean
