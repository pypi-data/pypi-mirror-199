# Example taken from https://github.com/ColumbiaOSS/example-project-python/blob/main/Makefile

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
	python -m black --check src tests setup.py
	python -m flake8 --per-file-ignores="__init__.py:F401" --max-line-length 120 src tests setup.py

# Alias
lints: lint

format:  ## run autoformatting with black
	python -m black src tests setup.py

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
	python -m pytest -v tests/

coverage:  ## clean and run unit tests with coverage
	python -m pytest -v tests/ --cov=src --cov-branch --cov-fail-under=50 --cov-report=term-missing

# Alias
tests: test

###########
# VERSION #
###########
show-version:
	bump2version --dry-run --allow-dirty setup.py --list | grep current | awk -F= '{print $2}'

patch:
	bump2version patch

minor:
	bump2version minor

major:
	bump2version major

########
# DIST #
########
dist-build:  # Build python dist
	python setup.py sdist bdist_wheel

dist-check:
	python -m twine check dist/*

dist: clean build dist-build dist-check  ## Build dists

publish:  # Upload python assets
	echo "would usually run python -m twine upload dist/* --skip-existing"
