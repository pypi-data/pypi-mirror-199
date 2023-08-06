PYTHON = python3
TWINE  = $(PYTHON) -m twine
PYTEST = $(PYTHON) -m pytest
PIP    = $(PYTHON) -m pip

VENV   = $(CURDIR)/.venv
ACTIVATE = . $(VENV)/bin/activate

PYTEST_FLAGS = -v

COVERAGE_DIR = bumpline/

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
	if test ! -d $(VENV); then \
		$(PYTHON) -m venv $(VENV); \
	fi
	$(ACTIVATE) && $(PIP) install -r dev_requirements.txt
	touch $(VENV)

test: $(VENV)
	$(ACTIVATE) && $(PYTEST) $(PYTEST_FLAGS) $(PYTEST_FILES)

coverage: $(VENV)
	$(ACTIVATE) && $(PYTEST) --cov=$(COVERAGE_DIR) tests/ 2> /dev/null
	if test -f .coverage; then rm .coverage; fi

.PHONY: build check publish clean install test coverage
