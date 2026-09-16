# MCP Server

A local [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server built with Python that lets AI assistants like Claude for Desktop securely interact with local data and custom tools.

This server exposes tools that read and summarize tabular data files (CSV and Parquet), and serves as a template for building additional MCP tools.

## What It Does

- Runs a local MCP server (`mcp[cli]` SDK) that Claude for Desktop can connect to
- Exposes tools Claude can call in natural language, e.g.:
  - "Summarize the CSV file named sample.csv."
  - "How many rows are in sample.parquet?"
- Provides a clean, modular folder structure for adding new tools over time

## Project Structure

```
mcp_server/
│
├── data/                 # Sample CSV and Parquet files
├── tools/                # MCP tool definitions
│   ├── csv_tools.py
│   └── parquet_tools.py
├── utils/                # Reusable file reading logic
│   └── file_reader.py
├── server.py             # Creates the shared MCP server instance
├── main.py                # Entry point for the MCP server
└── README.md
```

## Requirements

- Python (managed via [uv](https://github.com/astral-sh/uv))
- Dependencies: `mcp[cli]`, `pandas`, `pyarrow`

## Setup

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal, then confirm it installed correctly:

```bash
uv --version
```

### 2. Set up the project environment

```bash
uv venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
uv add "mcp[cli]" pandas pyarrow
```

### 4. Generate sample data (optional)

If you want to test with the sample dataset, add a `data/sample.csv` file and convert it to Parquet:

```bash
uv run generate_parquet.py
```

This produces `data/sample.csv` and `data/sample.parquet`.

## Running the Server

From the project root:

```bash
uv run main.py
```

The server will start and wait for a connection from an MCP client (e.g., Claude for Desktop). No output in the terminal at this stage is expected.

## Connecting to Claude for Desktop

1. Install [Claude for Desktop](https://www.anthropic.com/claude) (not currently available on Linux).
2. Open the Claude config file:
   - **macOS/Linux:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
3. Add this server to the config, replacing the path with the absolute path to this project:

   ```json
   {
     "mcpServers": {
       "mcp_server": {
         "command": "uv",
         "args": [
           "--directory",
           "/ABSOLUTE/PATH/TO/mcp_server",
           "run",
           "main.py"
         ]
       }
     }
   }
   ```

4. Restart Claude for Desktop. A hammer/tools icon should appear showing the registered tools.

## Available Tools

| Tool | Description |
|---|---|
| `summarize_csv_file` | Reads a CSV file from `/data` and reports its row and column counts |
| `summarize_parquet_file` | Reads a Parquet file from `/data` and reports its row and column counts |

## Troubleshooting

- Confirm the server process is running and hasn't crashed
- Double-check the absolute path in `claude_desktop_config.json`
- Verify the target data files exist in `/data`
- Check Claude's UI for tool-loading errors

## Extending This Template

Ideas for adding more capabilities:

- **More tools** — filter rows by column value, return column names/dtypes, compute statistics
- **Resources** (`@mcp.resource()`) — expose static or dynamic data as context
- **Prompts** (`@mcp.prompt()`) — reusable interaction templates
- **Async tools** — use `async def` for tools that call external APIs or databases
- **Custom clients** — build your own client with the SDK's `ClientSession` interface


