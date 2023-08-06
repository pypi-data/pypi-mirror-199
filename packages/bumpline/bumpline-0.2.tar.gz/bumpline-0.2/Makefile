PYTHON = python3
TWINE  = $(PYTHON) -m twine
PYTEST = $(PYTHON) -m pytest
PIP    = $(PYTHON) -m pip

VENV   = $(CURDIR)/.venv
ACTIVATE = . $(VENV)/bin/activate

PYTEST_FLAGS = -v

COVERAGE_DIR = bumpline/

PYTHON_IMAGE   = python
PYTHON_VERSION = latest

build:
	$(PYTHON) -m build

check: | dist
	$(TWINE) check dist/*

publish: build
	$(TWINE) upload dist/*

dist:
	mkdir dist

clean: | dist
	rm -rf dist/*

install: $(VENV)

$(VENV): dev_requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && $(PIP) install -r dev_requirements.txt
	touch $(VENV)

test: | $(VENV)
	$(ACTIVATE) && $(PYTEST) $(PYTEST_FLAGS) $(PYTEST_FILES)

coverage: | $(VENV)
	$(ACTIVATE) && $(PYTEST) --cov=$(COVERAGE_DIR) tests/ 2> /dev/null
	if test -f .coverage; then rm .coverage; fi

clean_image:
	if test -n "$$(docker container ls -a -f name=test -q)"; then \
		docker-compose down; \
	fi
	if test -n "$$(docker image ls -f reference=bumpline-test -q)"; then \
		docker image rm bumpline-test; \
	fi

test_container: clean_image
	PYTHON_IMAGE=$(PYTHON_IMAGE); export PYTHON_IMAGE; \
	PYTHON_VERSION=$(PYTHON_VERSION); export PYTHON_VERSION; \
	if test -t 1; then \
		docker-compose up --exit-code-from test; \
	else \
		docker-compose -f no-tty.yml up --exit-code-from test; \
	fi
	docker-compose down

.PHONY: build check publish clean install test coverage
