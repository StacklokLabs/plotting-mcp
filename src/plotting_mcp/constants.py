"""Constants for the plotting MCP server."""

import os

# Constants for plotting
PLOT_WIDTH = int(os.getenv("PLOT_WIDTH", 10))
PLOT_HEIGHT = int(os.getenv("PLOT_HEIGHT", 6))
PLOT_FIGURE_SIZE = (PLOT_WIDTH, PLOT_HEIGHT)
PLOT_DPI = int(os.getenv("PLOT_DPI", 100))

# Constants for server configuration
MCP_PORT = os.getenv("MCP_PORT", 9090)
