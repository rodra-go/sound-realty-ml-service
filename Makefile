.PHONY: all test lint format run help install

# Define commands for easy modification
PYTHON = python
PIP = pip
PYTEST = pytest
BLACK = black
ISORT = isort
FLAKE8 = flake8
UVICORN = uvicorn
APP = main:app

# Default command when you run 'make'
all: help

# Help command to list available commands
help:
	@echo "Available commands:"
	@echo "  install - Install project dependencies using pip."
	@echo "  test    - Run the test suite."
	@echo "  lint    - Lint the code with flake8, black, and isort."
	@echo "  format  - Format the code with black and isort."
	@echo "  run     - Run the FastAPI application."
	@echo "  help    - Display this help."

# Install project dependencies using pip
install:
	@echo "Installing dependencies from pyproject.toml..."
	@$(PIP) install --no-cache-dir .'[dev]'

# Run tests
test:
	@echo "Running tests..."
	@$(PYTEST)

# Lint with flake8, black, and isort
lint:
	@echo "Linting code..."
	@echo "Running flake8..."
	@$(FLAKE8) .
	@echo "Running black..."
	@$(BLACK) --check .
	@echo "Running isort..."
	@$(ISORT) --check-only .

# Format code with black and isort
format:
	@echo "Formatting code..."
	@$(BLACK) .
	@$(ISORT) .

# Run the FastAPI app
run:
	@echo "Running application..."
	@$(UVICORN) $(APP) --reload
