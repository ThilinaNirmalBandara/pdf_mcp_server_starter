from .pdf_operations import register_pdf_operations
from .workspace_tools import register_workspace_tools


def register_all_tools(mcp):
    register_workspace_tools(mcp)
    register_pdf_operations(mcp)
