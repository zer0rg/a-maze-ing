# A-Maze-Ing Makefile
# Automates common development tasks

PYTHON = python3
PIP = pip
CONFIG = configs/20x20.txt

.PHONY: install run debug clean lint build

# Install project dependencies
install:
	$(PIP) install -e .
	$(PIP) install libs/mlx-2.2-py3-none-any.whl
	$(PIP) install flake8 mypy types-setuptools

# Run the main script
run:
	$(PYTHON) a_maze_ing.py $(CONFIG)

# Run in debug mode using pdb
debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

# Clean temporary files and caches
clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf custom_typing/__pycache__
	rm -rf .mypy_cache
	rm -rf build
	rm -rf a_maze_ing.egg-info
	rm -rf .pytest_cache

# Run linters (flake8 and mypy)
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Build distribution packages
build:
	$(PIP) install build
	$(PYTHON) -m build
