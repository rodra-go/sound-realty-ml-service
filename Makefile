.PHONY: all test lint format run help install train docker-build docker-push hit-api

TAG ?= latest

all: help

help:
	@echo "Available commands:"
	@echo "  install        - Install project dependencies using pip."
	@echo "  test           - Run the test suite."
	@echo "  lint           - Lint the code with flake8, black, and isort."
	@echo "  format         - Format the code with black and isort."
	@echo "  run            - Run the FastAPI application."
	@echo "  train          - Trains a new version of the model."
	@echo "  docker-build   - Builds a docker image."
	@echo "  docker-push    - Pushes the image to docker repository."
	@echo "  hit-api        - Hits the API."
	@echo "  help           - Display this help."

install:
	@echo "Installing dependencies from pyproject.toml..."
	@pip install --no-cache-dir .'[dev]'

test:
	@echo "Running tests..."
	@pytest


lint:
	@echo "Linting code..."
	@echo "Running flake8..."
	@flake8 .
	@echo "Running black..."
	@black --check .
	@echo "Running isort..."
	@isort --check-only .

# Format code with black and isort
format:
	@echo "Formatting code..."
	@black .
	@isort .

# Run the FastAPI app
run:
	@echo "Running application..."
	@uvicorn main:app --reload

# Train a new model version
train:
	@echo "Training a new model version..."
	@python training/create_model.py

# Builds a new image
docker-build:
	@echo "Building new image..."
	@docker build -t sound_realty_ml_service:$(TAG) -f api.Dockerfile .

# Pushes image to image repo
docker-push:
	@echo "Pushing new image..."
	@sleep 5

# Hits API
hit-api:
	@echo "Hitting the API..."
	@python hit_api.py
