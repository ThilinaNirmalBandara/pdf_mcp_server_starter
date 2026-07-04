from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from tools import register_all_tools

mcp = FastMCP("PDF Utility MCP Server")
register_all_tools(mcp)


if __name__ == "__main__":
    # stdio is easiest for local MCP clients like Claude Desktop.
    mcp.run(transport="stdio")
