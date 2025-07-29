.PHONY: install format typecheck help

help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies using uv"
	@echo "  format     - Format code using ruff"
	@echo "  typecheck  - Run type checking using ty"
	@echo "  help       - Show this help message"

install:
	uv sync

format:
	uv run ruff format .
	uv run ruff check --fix .

typecheck:
	uv run ty check
