.PHONY: all install-dev test docs clean-pyc

all: test

pack:
	python setup.py check && python setup.py sdist

test-upload:
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload:
	python -m twine upload dist/*

install-dev:
	pip install -q -e .[dev]

test: clean-pyc install-dev
	pytest

docs: clean-pyc install-dev
	$(MAKE) -C docs html

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-cache:
	find . -name '__pycache__' -exec rm -rf {} +