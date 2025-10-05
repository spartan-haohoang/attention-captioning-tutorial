.PHONY: help install install-dev test lint format clean docker-build docker-run docker-stop setup pre-commit install-hooks

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation commands
install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt

install-uv: ## Install dependencies using uv (faster)
	uv pip install -r requirements.txt
	uv pip install -r requirements-dev.txt

# Development setup
setup: install-dev install-hooks ## Complete development setup
	@echo "Development environment setup complete!"

install-hooks: ## Install pre-commit hooks
	pre-commit install

# Testing
test: ## Run tests
	python -m pytest tests/ -v

test-cov: ## Run tests with coverage
	python -m pytest tests/ -v --cov=. --cov-report=html --cov-report=xml

test-fast: ## Run tests in parallel
	python -m pytest tests/ -v -n auto

# Code quality
lint: ## Run linting
	flake8 attention_networks/ tests/
	mypy attention_networks/

format: ## Format code
	black attention_networks/ tests/
	isort attention_networks/ tests/

format-check: ## Check code formatting
	black --check attention_networks/ tests/
	isort --check-only attention_networks/ tests/

# Docker commands
docker-build: ## Build Docker image
	docker build -t attention-networks .

docker-run: ## Run Jupyter server in Docker
	docker-compose up -d jupyter
	@echo "Jupyter server running at http://localhost:8888"

docker-stop: ## Stop Docker containers
	docker-compose down

docker-logs: ## Show Docker logs
	docker-compose logs -f jupyter

docker-shell: ## Open shell in Docker container
	docker-compose exec jupyter bash

# Data and model management
download-data: ## Download and extract dataset
	@echo "Downloading Flickr8K dataset..."
	cd datasets && unzip -o flickr8k.zip
	@echo "Dataset ready!"

clean-data: ## Clean downloaded data
	rm -rf flickr8k/
	rm -rf datasets/flickr8k/

# Cleanup
clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

clean-models: ## Clean trained models
	rm -rf models/*.pth
	rm -rf models/*.pt
	rm -rf models/*.pkl

# Jupyter notebook commands
notebook: ## Start Jupyter notebook server
	jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

lab: ## Start JupyterLab server
	jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root

convert-notebooks: ## Convert notebooks to Python scripts
	jupyter nbconvert --to script demo_*.ipynb

# Documentation
docs: ## Build documentation
	cd docs && make html

docs-serve: ## Serve documentation locally
	cd docs/_build/html && python -m http.server 8000

# Pre-commit
pre-commit: ## Run pre-commit on all files
	pre-commit run --all-files

# Environment
env: ## Create environment file from template
	cp env.example .env

# Git hooks
git-hooks: ## Install git hooks
	cp scripts/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

# Development workflow
dev: ## Start development environment
	@echo "Starting development environment..."
	@echo "1. Installing dependencies..."
	$(MAKE) install-dev
	@echo "2. Setting up pre-commit hooks..."
	$(MAKE) install-hooks
	@echo "3. Starting JupyterLab..."
	$(MAKE) lab

# CI/CD simulation
ci: ## Run CI pipeline locally
	@echo "Running CI pipeline..."
	$(MAKE) format-check
	$(MAKE) lint
	$(MAKE) test-cov
	@echo "CI pipeline completed successfully!"

# All-in-one commands
all: clean install-dev test-cov lint format ## Run all checks and tests
	@echo "All checks passed!"

fresh: clean install-dev ## Fresh start - clean and reinstall everything
	@echo "Fresh environment ready!"
