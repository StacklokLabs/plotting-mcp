.PHONY: install format lint typecheck test help

help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies using uv"
	@echo "  format     - Format code using ruff"
	@echo "  lint       - Run linting using ruff"
	@echo "  typecheck  - Run type checking using ty"
	@echo "  test       - Run tests using pytest"
	@echo "  help       - Show this help message"

install:
	uv sync

format:
	uv run ruff format .

lint:
	uv run ruff check .

typecheck:
	uv run ty check

test:
	uv run pytest
