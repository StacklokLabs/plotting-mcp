"""MCP server for generating plots from CSV data."""

import base64
import io
from typing import Any

import anyio
import pandas as pd
import uvicorn
from mcp.server.fastmcp import FastMCP

from plotting_mcp.plot import plot_to_bytes

mcp = FastMCP(name="plotting-mcp")


@mcp.tool()
def generate_plot(csv_data: str, plot_type: str, **kwargs: Any) -> str:
    """
    Generate a plot from CSV data.

    Args:
        csv_data: CSV data as a string
        plot_type: Type of plot to generate
            (line, bar, scatter, pie)
        **kwargs: Additional plotting parameters. In the background Seaborn is used,
            so any parameters supported by Seaborn's plotting functions can be passed.
            Basic parameters include:
            - `x`: Column name for x-axis
            - `y`: Column name for y-axis
            - `hue`: Column name for color encoding

    Returns:
        Base64-encoded PNG image of the plot
    """
    try:
        df = pd.read_csv(io.StringIO(csv_data))

        if df.empty:
            raise ValueError("CSV data is empty")

        plot_bytes = plot_to_bytes(df, plot_type, **kwargs)

        encoded_image = base64.b64encode(plot_bytes).decode("utf-8")
        return f"data:image/png;base64,{encoded_image}"
    except Exception as e:
        raise ValueError(f"Error generating plot: {str(e)}") from e


# This function is used to run the server with StreamableHTTP transport.
# It is a direct copy of the `run_streamable_http_async` function from the MCP library.
# This is necessary to be able to add middleware to the Starlette app and proper logging if needed.
async def run_streamable_http_async() -> None:
    """Run the server using StreamableHTTP transport."""
    starlette_app = mcp.streamable_http_app()

    config = uvicorn.Config(starlette_app, host=mcp.settings.host, port=mcp.settings.port)
    server = uvicorn.Server(config)
    await server.serve()


def main():
    """Main entry point for the MCP server."""
    anyio.run(run_streamable_http_async())


if __name__ == "__main__":
    main()
