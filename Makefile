PYTHON := python3
VENV := .venv
VPY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.venv:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip

install: .venv
	$(PIP) install -e .

server: .venv
	$(VPY) -m chatrooms.server

client: .venv
	$(VPY) -m chatrooms.client

clean:
	rm -rf $(VENV)

.PHONY: install server client clean
