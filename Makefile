SHELL := /bin/bash

.PHONY: help install lint test build run clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dependencies
	pip install -r bot/requirements.txt

lint: ## Lint with ruff
	ruff check bot/ tests/

test: ## Run tests
	python -m pytest tests/ -v

build: ## Build Docker image
	docker build -t ghcr.io/pkalab/incident-bot:latest -f bot/Dockerfile bot/

run: ## Run bot locally
	@cd bot && python app.py

clean: ## Clean Python cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
