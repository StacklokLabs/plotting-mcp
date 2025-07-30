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

**Returns:** Base64 PNG image with data URL prefix

## LibreChat Integration

This MCP server is designed to work with LibreChat. The generated images are returned as base64 PNG data that LibreChat can display directly.

Supported image format: PNG

## ToolHive

ToolHive is a platform that simplifies the deployment and management of Model Context Protocol (MCP) servers by providing containerized, secure environments across UI, CLI, and Kubernetes modes. It offers streamlined deployment with comprehensive security controls and integration with popular development tools.

For more information, see the [ToolHive documentation](https://docs.stacklok.com/toolhive/). To get started with the CLI, check out the [ToolHive CLI Quickstart](https://docs.stacklok.com/toolhive/tutorials/quickstart-cli).

### Build the Docker image

```bash
docker build -t plotting-mcp .
```

### Run with ToolHive

#### Run locally

```bash
thv run --name plotting-mcp --transport streamable-http plotting-mcp:latest
```

#### Run with ToolHive in K8s with ToolHive operator

1. Create a PVC for the MCP server. This is needed since the plotting libraries Matplotlib and Cartopy require a writable filesystem to cache data:
```bash
kubectl apply -f toolhive-pvc.yaml
```

2. Deploy the MCP server in K8s
```bash
kubectl apply -f toolhive-deployment.yaml
```

3. Once the MCP server is deployed, do port-forwarding
```bash
kubectl port-forward svc/mcp-plotting-mcp-proxy 9090:9090
```

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
