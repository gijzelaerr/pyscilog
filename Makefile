
all: test

venv/:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip wheel

venv/installed: venv/
	venv/bin/pip install -e ".[test]"
	touch venv/installed

setup: venv/installed

test: setup
	venv/bin/pytest

clean: venv/
	venv/bin/python3 setup.py clean
	rm -rf build dist *.egg-info .eggs venv/

venv/bin/mypy: venv/
	venv/bin/pip install mypy

venv/bin/pycodestyle: venv/
	venv/bin/pip install pycodestyle

mypy: venv/bin/mypy
	venv/bin/mypy pyscilog test

pycodestyle: venv/bin/pycodestyle
	venv/bin/pycodestyle pyscilog test

venv/bin/twine: venv/
	venv/bin/pip install twine

twine: venv/bin/twine
	venv/bin/twine upload dist/*

bdist_wheel: venv/
	venv/bin/python setup.py bdist_wheel

sdist: venv/
	venv/bin/python setup.py sdist
