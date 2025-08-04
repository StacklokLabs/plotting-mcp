## Project Overview
- The project is focused on having an MCP server producing custom plots using as main library seaborn
- The MCP server takes as input CSV data, plot type and kwargs plotting parameters

## Project Structure
- MCP server logic is located in: src/plotting_mcp/server.py
- Plotting logic is located in: src/plotting_mcp/plot.py

## Development Best Practices
- After significant code changes run `make format` and `make typecheck` to make sure the code follows best practices

## Code Maintenance Guidelines
- When there is a new plot type added in plot.py we need to update the mcp tool in server.py

## Dependency Management
- This project uses uv for managing dependencies. In case you need to add a dependency use the command `uv add <dependency>`
- If the dependency is for developing, e.g. for testing use `uv add <dependency> --dev`
- All of the configuration of the project should be centralized in the pyproject.toml file