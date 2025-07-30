.PHONY: install format lint typecheck help

help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies using uv"
	@echo "  format     - Format code using ruff"
	@echo "  lint       - Run linting using ruff"
	@echo "  typecheck  - Run type checking using ty"
	@echo "  help       - Show this help message"

install:
	uv sync

format:
	uv run ruff format .
	uv run ruff check --fix .

lint:
	uv run ruff check .

typecheck:
	uv run ty check
