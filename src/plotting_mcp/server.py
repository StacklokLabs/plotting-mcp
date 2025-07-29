"""MCP server for generating plots from CSV data."""

import base64
import io
import json

import anyio
import click
import pandas as pd
import structlog
import uvicorn
from mcp.server.fastmcp import FastMCP

from plotting_mcp.configure_logging import configure_logging
from plotting_mcp.constants import MCP_PORT
from plotting_mcp.plot import plot_to_bytes

mcp = FastMCP(name="plotting-mcp", port=MCP_PORT, host="0.0.0.0")

logger = structlog.get_logger(__name__)


@mcp.tool()
def generate_plot(csv_data: str, plot_type: str = "line", json_kwargs: str = "{}") -> str:
    """
    Generate a plot from CSV data.

    Args:
        csv_data (str): CSV data as a string
        plot_type (str): Type of plot to generate (line, bar, scatter, pie).
         If not specified, defaults to "line".
        json_kwargs (str):
            Additional plotting parameters in JSON format. In the background Seaborn is used,
            so any parameters supported by Seaborn's plotting functions can be passed.
            Basic parameters include:
                - `x`: Column name for x-axis
                - `y`: Column name for y-axis
                - `hue`: Column name for color encoding
            If not specified, defaults to an empty JSON object.

    Returns:
        Base64-encoded PNG image of the plot
    """
    try:
        kwargs = json.loads(json_kwargs)
    except json.JSONDecodeError:
        logger.exception("Invalid JSON for kwargs")
        raise

    try:
        df = pd.read_csv(io.StringIO(csv_data))

        plot_bytes = plot_to_bytes(df, plot_type, **kwargs)

        encoded_image = base64.b64encode(plot_bytes).decode("utf-8")
        logger.info("Plot generated successfully", plot_type=plot_type)
        return f"data:image/png;base64,{encoded_image}"
    except Exception:
        logger.exception("Error generating plot")
        raise


# This function is used to run the server with StreamableHTTP transport.
# It is a direct copy of the `run_streamable_http_async` function from the MCP library.
# This is necessary to be able to add middleware to the Starlette app and proper logging if needed.
async def run_streamable_http_async(logging_dict: dict) -> None:
    """Run the server using StreamableHTTP transport."""
    starlette_app = mcp.streamable_http_app()

    config = uvicorn.Config(
        starlette_app, host=mcp.settings.host, port=mcp.settings.port, log_config=logging_dict
    )
    server = uvicorn.Server(config)
    await server.serve()


@click.option(
    "--log-level",
    default="INFO",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    help="Set the logging level (default: INFO)",
)
def main(log_level: str = "INFO") -> None:
    """Main entry point for the MCP server."""
    logging_dict = configure_logging(log_level=log_level)
    anyio.run(run_streamable_http_async, logging_dict)


if __name__ == "__main__":
    main()
