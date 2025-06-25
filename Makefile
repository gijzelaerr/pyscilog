
all: test

# Check if poetry is installed, install if not
check-poetry:
	@which poetry > /dev/null || (echo "Poetry not found. Install with: curl -sSL https://install.python-poetry.org | python3 -" && exit 1)

# Install dependencies using poetry
install: check-poetry
	poetry install --with test,doc

# Install only main dependencies
install-main: check-poetry
	poetry install

# Install development dependencies
install-dev: check-poetry
	poetry install --with test,doc

setup: install

test: install
	poetry run pytest

clean:
	rm -rf build dist *.egg-info .eggs .venv/ __pycache__/ .pytest_cache/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

mypy: install
	poetry run mypy pyscilog test

pycodestyle: install
	poetry run pycodestyle pyscilog test

# Lint with both mypy and pycodestyle
lint: mypy pycodestyle

# Build distribution packages
build: install
	poetry build

# Publish to PyPI
publish: build
	poetry publish

# Publish to test PyPI
publish-test: build
	poetry publish --repository testpypi

# Development server/shell
shell: install
	poetry shell

# Run a command in the poetry environment
run: install
	poetry run

# Update dependencies
update: check-poetry
	poetry update

# Show dependency information
show: check-poetry
	poetry show

# Export requirements.txt (for compatibility)
export-requirements: install
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	poetry export -f requirements.txt --output requirements-dev.txt --with test,doc --without-hashes
