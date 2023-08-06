# Thanks to Tim Paine for the example Makefile from https://github.com/ColumbiaOSS/example-project-python/blob/main/Makefile

#########
# BUILD #
#########
develop:  ## install dependencies and build library
	python -m pip install -e .[develop]

build:  ## build the python library
	python setup.py build build_ext --inplace

install:  ## install library
	python -m pip install .

#########
# LINTS #
#########
lint:  ## run static analysis with flake8
	python -m black --check src setup.py
	python -m flake8 src setup.py

# Alias
lints: lint

format:  ## run autoformatting with black
	python -m black src/ setup.py

# alias
# alias
fix: format

check:  ## check assets for packaging
	check-manifest -v

# Alias
checks: check


#########
# TESTS #
#########
test: ## clean and run unit tests
	python -m pytest -v src/test.py

coverage:  ## clean and run unit tests with coverage
	python -m pytest -v src/test.py --cov=src/fin_libs --cov-branch --cov-fail-under=75 --cov-report term-missing

# Alias
tests: test