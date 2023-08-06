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
# RUN #
#########

run:
	python3 pynixconfig/linuxconfig.py

#########
# LINTS #
#########
lint:  ## run static analysis with flake8
	python -m black -t py38 --check pynixconfig setup.py
	python -m flake8 pynixconfig setup.py

# Alias
lints: lint

format:  ## run autoformatting with black
	python -m black pynixconfig/ setup.py

#########
# TESTS #
#########

test:
	python -m pytest -v pynixconfig/tests

coverage:  ## clean and run unit tests with coverage
	python -m pytest -v pynixconfig/tests --cov=pynixconfig --cov-branch --cov-fail-under=50 --cov-report term-missing