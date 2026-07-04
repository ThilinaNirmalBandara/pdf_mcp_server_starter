# PDF Utility MCP Server

This project starts a local MCP server that exposes safe PDF tools to MCP-compatible clients such as Claude Desktop. The server only allows access inside the workspace folder, which helps keep file operations contained and predictable.

## What the server can do

- List PDF files in the workspace
- Read PDF metadata and page count
- Extract text from one or more pages
- Merge multiple PDFs into one file
- Split one PDF into single-page files
- Create a new PDF from selected pages
- Rotate selected pages
- Apply basic PDF optimization

## Requirements

- Python 3.10 or newer
- pip

## Setup

1. Open the project folder and create a virtual environment.

   PowerShell:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the dependencies.

   ```powershell
   pip install -r requirements.txt
   ```

3. Create a local environment file.

   ```powershell
   Copy-Item .env.example .env
   ```

4. Put your PDF files in the workspace folder.

   ```powershell
   mkdir workspace -Force
   ```

5. Start the MCP server.

   ```powershell
   python server.py
   ```

## Using the server with an MCP client

A typical Claude Desktop configuration looks like this:

```json
{
  "mcpServers": {
    "pdf-utility": {
      "command": "python",
      "args": ["C:/absolute/path/to/pdf_mcp_server/server.py"]
    }
  }
}
```

Replace the path with the location of the server script on your machine.

## Example prompts

You can try prompts like these after the server is running:

```text
List all PDFs in the workspace.
```

```text
Extract text from pages 1 to 2 of sample.pdf.
```

```text
Merge file1.pdf and file2.pdf into merged/output.pdf.
```

```text
Create a new PDF from pages 1, 3, and 5 of report.pdf.
```

## Safety note

The server only accesses files inside the workspace folder. That prevents the LLM from reading or modifying unrelated files on your system.

