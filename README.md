# fhir-mcp-toolkit

An MCP (Model Context Protocol) server that exposes healthcare data tools to LLM-powered applications. It wraps the public HAPI FHIR R4 sandbox, so no real patient data is involved — all "patients" are synthetic test records.

Built as a learning project to understand how MCP servers work and how LLMs consume tools in the emerging agent ecosystem.

## What is this?

MCP is an open standard (introduced by Anthropic in late 2024) for connecting LLM applications to external tools and data sources. An MCP server exposes a set of tools; an MCP client (like Claude Desktop, Cursor, or Zed) gives an LLM access to those tools during a conversation.

This server exposes FHIR healthcare tools. When connected, an LLM can look up patient records, search by name, and (eventually) pull medications, conditions, and lab results — all from a public test sandbox.

## Tools

| Tool | Description |
|---|---|
| `get_patient(patient_id)` | Fetch a patient's demographic record by FHIR ID |
| `search_patients(name, count)` | Search for patients by name, returns up to `count` matches |

More tools are planned — see [Roadmap](#roadmap).

## Stack

- **Python 3.10+**
- **[mcp](https://github.com/modelcontextprotocol/python-sdk)** — official MCP Python SDK
- **[httpx](https://www.python-httpx.org/)** — HTTP client for FHIR requests
- **[HAPI FHIR public sandbox](https://hapi.fhir.org/)** — upstream data source

## Setup

Clone the repo and create a virtual environment:

```bash
git clone https://github.com/YOUR_USERNAME/fhir-mcp-toolkit.git
cd fhir-mcp-toolkit
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run locally with the MCP inspector

The SDK ships with a browser-based inspector for testing tools in isolation:

```bash
mcp dev server.py
```

Open the inspector URL it prints, pick a tool, invoke it, and watch the JSON-RPC messages in real time.

## Use with Claude Desktop

Add this to your `claude_desktop_config.json`:

- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fhir-toolkit": {
      "command": "/absolute/path/to/fhir-mcp-toolkit/.venv/bin/python",
      "args": ["/absolute/path/to/fhir-mcp-toolkit/server.py"]
    }
  }
}
```

Fully quit and reopen Claude Desktop. The `fhir-toolkit` tools should appear in the tools menu.

Try asking: *"Search for patients named Smith on the FHIR server."*

## How it works# fhir-mcp-toolkit
