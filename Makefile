.PHONY: build run test clean help

# Docker image name
IMAGE_NAME := amdahl-analyzer

# Default Python interpreter
PYTHON := python3

help:
	@echo "Available targets:"
	@echo "  build      - Build Docker image"
	@echo "  run        - Run Docker container with default arguments"
	@echo "  test       - Run pytest tests locally"
	@echo "  clean      - Remove Docker images and output files"
	@echo "  install    - Install Python dependencies locally"
	@echo "  lint       - Run code linting checks"
	@echo "  help       - Show this help message"

build:
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME) .

run:
	@echo "Running Docker container..."
	docker run --rm $(IMAGE_NAME)

test:
	@echo "Running tests..."
	$(PYTHON) -m pytest tests/ -v

install:
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install -r requirements.txt

lint:
	@echo "Running lint checks..."
	$(PYTHON) -m flake8 *.py tests/*.py --max-line-length=100 --ignore=E203,W503 || true

clean:
	@echo "Cleaning up..."
	docker rmi $(IMAGE_NAME) 2>/dev/null || true
	rm -rf output/
	rm -rf __pycache__/
	rm -rf tests/__pycache__/
	rm -rf .pytest_cache/
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleanup complete."

