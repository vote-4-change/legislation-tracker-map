TOOL_ROOT=$(shell pwd)
VENV=$(TOOL_ROOT)/venv
PYTHON=$(VENV)/bin/python3
PIP=$(VENV)/bin/pip

define HELP
Makefile for the ingestor

Environment:
--------
VENV:      $(VENV)
PYTHON: $(PYTHON)
PIP:          $(PIP)

Targets:
--------
venv: create venv
setup: create a virtual environment and install dependencies
run: run the application
test: run the tests
clean: remove temporary files
endef

export HELP
help:
	@echo "$$HELP"

run: $(VENV)/bin/activate
	$(PYTHON) src/main.py

package: $(VENV)/bin/activate
	$(PYTHON) setup.py bdist_wheel

install: $(VENV)/bin/activate
	$(PIP) install dist/*.whl

$(VENV):
	python3 -m venv $(VENV)

venv: $(VENV)
	echo "Activate with: . ./venv/bin/activate"
setup: $(VENV)/bin/activate requirements.txt requirements_test.txt

$(VENV)/bin/activate: requirements.txt requirements_test.txt
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements_test.txt

test: $(VENV)/bin/activate
	pytest -m pytest tests --cov=ingestor --cov-report=xml --junitxml=report.xml



docker-build: package
	docker build -t ingestor . -f src/docker/Dockerfile

clean:
	rm -rf __pycache__
	rm -rf $(VENV)