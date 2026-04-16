# fhir-mcp-toolkit

An MCP (Model Context Protocol) server that exposes healthcare data tools to LLM-powered applications. It wraps the public HAPI FHIR R4 sandbox, so no real patient data is involved — all "patients" are synthetic test records.

Built as a learning project to understand how MCP servers work and how LLMs consume tools in the emerging agent ecosystem.

## Learning Objectives

Tracking what I'm aiming to understand by building this. Checked items are things I've actually done hands-on, not just read about.

**MCP fundamentals**
- [ ] Understand what MCP is and why it exists (vs. each app inventing its own tool plugin system)
- [ ] Understand the difference between an MCP server, an MCP client, and the LLM itself
- [ ] Understand stdio vs. SSE/HTTP transports and when to use each
- [ ] Read and interpret JSON-RPC messages between client and server
- [ ] Write a tool with `@mcp.tool()` and understand how type hints become the input schema
- [ ] Understand why the docstring matters (it's the prompt the LLM reads to decide when to call the tool)

**Running and debugging**
- [ ] Run the server with the `mcp dev` inspector and invoke tools manually
- [ ] Wire the server into Claude Desktop via `claude_desktop_config.json`
- [ ] See a real end-to-end loop: chat message → LLM → tool call → FHIR response → chat reply
- [ ] Debug a broken tool call by reading inspector output

**FHIR basics**
- [ ] Understand what FHIR is and why it's the standard for healthcare data exchange
- [ ] Know the common resource types: Patient, Observation, MedicationRequest, Condition, Encounter
- [ ] Query a FHIR server using search parameters (`?name=`, `?patient=`, `_count`, `_sort`)
- [ ] Parse a FHIR Bundle response and extract useful fields

**Python for a JS developer**
- [ ] Set up a virtual environment with `venv` (the Python equivalent of `node_modules`)
- [ ] Use `pip` and `requirements.txt` for dependency management
- [ ] Use `httpx` to make HTTP calls (the `fetch`/`axios` equivalent)
- [ ] Get comfortable with Python type hints and decorators

**Stretch goals**
- [ ] Switch transport from stdio to SSE so the server can be hosted remotely
- [ ] Deploy the server to a real host (Railway, Fly.io, or similar)
- [ ] Add basic auth/token handling for a non-public FHIR server
- [ ] Write a second MCP server in TypeScript to compare the DX

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

## How it works