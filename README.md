# 📊 Plotting MCP Server

A MCP (Model Context Protocol) server that transforms CSV data into beautiful visualizations. Built with Python and optimized for seamless integration with AI assistants and chat applications.

## ✨ Features

- **📈 Multiple Plot Types**: Create line charts, bar graphs, pie charts, and world maps
- **🌍 Geographic Visualization**: Built-in support for plotting coordinate data on world maps using Cartopy
- **🔧 Flexible Parameters**: Fine-tune your plots with JSON-based configuration options
- **📱 Chat-Ready Output**: Returns base64-encoded PNG images perfect for AI chat interfaces
- **⚡ Fast Processing**: Efficient CSV parsing and plot generation with pandas and matplotlib

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
Transform your CSV data into stunning visualizations.

**Parameters:**
- `csv_data` (str): CSV data as a string
- `plot_type` (str): Plot type - `line`, `bar`, `pie`, or `worldmap`
- `json_kwargs` (str): JSON string with plotting parameters for customization

**Plotting Options:**
- **Line/Bar Charts**: Use Seaborn parameters (`x`, `y`, `hue` for data mapping)
- **World Maps**: Automatic coordinate detection (`lat`/`latitude`/`y` and `lon`/`longitude`/`x`)
  - Customize with `s` (size), `c` (color), `alpha` (transparency), `marker` (style)
- **Pie Charts**: Supports single column (value counts) or two columns (labels + values)

**Returns:** Base64-encoded PNG image ready for display

## 🤖 AI Assistant Integration

Perfect for enhancing AI conversations with data visualization capabilities. The server returns plots as base64-encoded PNG images that display seamlessly in:

- **LibreChat**: Direct integration for chat-based data analysis
- **Claude Desktop**: Through `mcp-remote` command to transform from HTTP transport to stdio
```json
{
  "mcpServers": {
    "plotting": {
      "command": "uvx",
      "args": [
        "--from", "/path/to/plotting-mcp",
        "plotting-mcp", "--transport=stdio"
      ]
    }
  }
}
```
- **Custom AI Applications**: Easy integration via MCP protocol
- **Development Tools**: Compatible with any MCP-enabled environment

**Image Format**: High-quality PNG with configurable DPI and sizing

## 🚀 ToolHive Deployment

Deploy and manage your plotting server effortlessly with ToolHive - a platform that provides containerized, secure environments for MCP servers across UI, CLI, and Kubernetes modes.

**Benefits:**
- 🔒 **Secure Containerization**: Isolated environments with comprehensive security controls
- ⚙️ **Multiple Deployment Options**: UI, CLI, and Kubernetes support
- 🔧 **Developer-Friendly**: Seamless integration with popular development tools

📚 **Resources:**
- [ToolHive Documentation](https://docs.stacklok.com/toolhive/)
- [CLI Quickstart Guide](https://docs.stacklok.com/toolhive/tutorials/quickstart-cli)

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

2. Deploy the MCP server in K8s. In the `toolhive-deployment.yaml`, you can customize the `image` field to point to your image registry.
```bash
kubectl apply -f toolhive-deployment.yaml
```

3. Once the MCP server is deployed, do port-forwarding
```bash
kubectl port-forward svc/mcp-plotting-mcp-proxy 9090:9090
```

## 🛠️ Development

Built with modern Python tooling for a great developer experience.

**Tech Stack:**
- 🐍 **Python 3.13+**: Latest Python features
- 📊 **Seaborn & Matplotlib**: Professional-grade plotting
- 🌍 **Cartopy**: Advanced geospatial visualization
- ⚡ **FastMCP**: High-performance MCP server framework
- 🔧 **UV**: Fast Python package management

### Code Quality

```bash
# Format code and fix linting issues
make format

# Type checking
make typecheck

# Or use uv directly
uv run ruff format .
uv run ruff check --fix .
uv run ty check
```
