# PDF MCP Server Starter

This project contains a local MCP server for working with PDF files. The server provides safe, scriptable PDF tools and is designed to be run locally so you can operate on documents without uploading them to third-party services.

## Why I created this

I built this tool because using online PDF services can be slow, limiting, and frustrating: many sites force you through several steps, limit file size or usage, and often lock useful features behind subscriptions. This project gives you a local, private alternative you can run on your own machine so you can merge, extract, split, rotate, and inspect PDFs directly — no uploads, no paywalls, and no extra hassle.

Use this server when you want quick, scriptable PDF operations on files stored in the `pdf_mcp_server/workspace` folder, or when you want to integrate PDF workflows directly into an MCP-compatible client without relying on third-party online tools.

## Quick start

1. Open `pdf_mcp_server` and follow its README for setup.
2. Put PDFs into `pdf_mcp_server/workspace`.
3. Start the server with:

```powershell
cd pdf_mcp_server
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python server.py
```

For full usage and examples see `pdf_mcp_server/README.md`.
