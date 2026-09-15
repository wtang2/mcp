# server.py
from mcp.server.mcpserver import MCPServer

# This is the shared MCP server instance
mcp = MCPServer("mix_server")

# Import tools so they get registered via decorators
import tools.csv_tools
import tools.parquet_tools

# Entry point to run the server
if __name__ == "__main__":
    mcp.run()# server.py

