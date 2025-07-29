# Plotting MCP Server

An MCP (Model Context Protocol) server that generates plots from CSV data, optimized for LibreChat integration.

## Features

- Generate plots from CSV data strings
- Support for multiple plot types: line, bar, pie
- Returns base64-encoded PNG images compatible with LibreChat

## Installation

### Using Makefile

```bash
make install
```

### Using uv

```bash
uv sync
```

## Usage

### Running the Server

```bash
uv run plotting-mcp
```

The server runs on port 9090 by default.

### Tools

#### `generate_plot`
Generate a plot from CSV data.

**Parameters:**
- `csv_data` (str): CSV data as a string
- `plot_type` (str): Type of plot (line, bar, pie)
- `**kwargs`: Additional plotting parameters.

**Returns:** Base64-encoded PNG image with data URL prefix

## LibreChat Integration

This MCP server is designed to work with LibreChat. The generated images are returned as base64-encoded PNG data URLs that LibreChat can display directly.

Supported image format: PNG

## Development

### Code Formatting

```bash
make format
# or
uv run ruff format .
uv run ruff check --fix .
```

### Typechecking

```bash
make typecheck
# or
uv run ty check
```
