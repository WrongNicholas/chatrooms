PYTHON := python3
VENV := .venv
VPY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: install install-test test server client clean

$(VENV):
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip

install: $(VENV)
	$(PIP) install -e .

install-test: $(VENV)
	$(PIP) install -e ".[test]"

test: install-test
	$(VPY) -m pytest

server: install
	$(VPY) -m chatrooms.server

client: install
	$(VPY) -m chatrooms.client

gui: install
	$(VPY) -m chatrooms.gui

clean:
	rm -rf $(VENV)
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete

deep-clean:
	rm -rf .pytest_cache
