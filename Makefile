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

run: $(VENV)/bin/activate
	$(PYTHON) manage.py runserver

docker-build:
	docker build -t django_app . -f Dockerfile

clean:
	rm -rf __pycache__
	rm -rf $(VENV)