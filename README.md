# MCP Meteo Italia — Custom MCP Server

A **Model Context Protocol (MCP) server** that gives any MCP-compatible AI assistant real-time weather data for Italian cities — built with FastMCP and Gradio.

## What it does

- Exposes a `get_meteo` tool via MCP that any Claude/AI agent can call
- Returns current weather (temperature, conditions, humidity, wind) for Italian cities
- Covers all major Italian cities: Milano, Roma, Napoli, Torino, Firenze, Bologna, Venezia, Genova, Palermo, Bari, and more
- Includes a **Gradio web UI** as a standalone frontend for direct testing

## How MCP works here

```
AI Assistant (Claude / any MCP client)
    └─ calls tool: get_meteo("Roma")
    └─ MCP Server (FastMCP) receives request
    └─ calls Open-Meteo API (free, no key needed)
    └─ returns structured weather JSON
```

## Tech stack

- `fastmcp` — MCP server framework
- `gradio` — web interface + GradioMCPServer
- `httpx` — async HTTP client for weather API
- [Open-Meteo](https://open-meteo.com) — free weather API, no key required

## Run it

```bash
pip install -r requirements.txt
python app.py
```

Then open the Gradio interface or connect any MCP client to the server endpoint.

## Topics

`python` `mcp` `model-context-protocol` `fastmcp` `gradio` `weather` `ai-tools` `llm` `api`
