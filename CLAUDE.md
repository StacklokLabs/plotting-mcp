## Project Overview
- The project is focused on having an MCP server producing custom plots using as main library seaborn
- The MCP server takes as input CSV data, plot type and kwargs plotting parameters

## Project Structure
- MCP server logic is located in: src/plotting_mcp/server.py
- Plotting logic is located in: src/plotting_mcp/plot.py

## Development Best Practices
- After significant code changes run `make format` and `make typecheck` to make sure the code follows best practices