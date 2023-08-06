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
	python -m black --check SpotifyPictureHelper setup.py
	python -m flake8 SpotifyPictureHelper setup.py --ignore=E501,E203

# Alias
lints: lint

format:  ## run autoformatting with black
	python -m black SpotifyPictureHelper/ setup.py

# alias
fix: format

#########
# TESTS #
#########
test: ## clean and run unit tests
	python -m pytest -v SpotifyPictureHelper/tests

coverage:  ## clean and run unit tests with coverage
	python3 -m pytest -v SpotifyPictureHelper/tests --cov=SpotifyPictureHelper --cov-branch --cov-fail-under=50 --cov-report term-missing

# Alias
tests: test

#########
# CLEAN #
#########
deep-clean: ## clean everything from the repository
	git clean -fdx

clean: ## clean the repository
	rm -rf .coverage coverage cover htmlcov logs build dist *.egg-info .pytest_cache .cache __pycache__