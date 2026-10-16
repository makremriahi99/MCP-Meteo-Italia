# Server Meteo Italiano — MCP + Gradio

Server MCP per il meteo di **qualsiasi comune italiano**, con interfaccia web Gradio, integrabile con assistenti AI come Claude, Cursor e Copilot. Dati da [Open-Meteo](https://open-meteo.com) (gratuito, senza API key).

## Tool MCP

| Tool | Cosa fa |
|---|---|
| `get_meteo(city)` | Meteo attuale: temperatura, condizione, vento, umidità |
| `get_previsioni(city, giorni)` | Previsioni da 1 a 7 giorni: min/max, probabilità e mm di pioggia |

## Come si usa

```bash
pip install -r requirements.txt
python meteo_mcp.py     # avvia il server MCP (stdio)
python app.py           # avvia l'interfaccia Gradio
```

Per usarlo in Claude Code:

```bash
claude mcp add meteo-italia -- python /percorso/meteo_mcp.py
```

## Skill per agenti AI

`SKILL.md` insegna all'agente quando e come usare i tool (formato SKILL.md, compatibile con Claude Code, Cursor, Copilot e altri).

## File

| File | Descrizione |
|---|---|
| `meteo_mcp.py` | Server MCP principale |
| `SKILL.md` | Skill per agenti AI |
| `app.py` | Interfaccia Gradio |
| `frontend.html` | Frontend HTML standalone |
| `requirements.txt` | Dipendenze Python |

## Tecnologie

- `mcp` (FastMCP, versione 1.x) — server Model Context Protocol
- `httpx` — chiamate HTTP asincrone
- `Gradio` — interfaccia web
- Open-Meteo — meteo e ricerca dei comuni

## Tag

`python` `fastmcp` `mcp` `gradio` `meteo` `weather` `italia` `llm` `claude`
