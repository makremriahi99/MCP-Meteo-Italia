# Server Meteo Italiano — FastMCP + Gradio

Server meteo per città italiane costruito con **FastMCP** (Model Context Protocol) e un'interfaccia web **Gradio**, integrabile con assistenti AI come Claude.

## Cosa fa

- Recupera dati meteo in tempo reale per qualsiasi città italiana
- Espone le funzionalità tramite protocollo MCP (utilizzabile da Claude e altri LLM)
- Interfaccia web interattiva con Gradio
- Frontend HTML statico per uso standalone

## Come si usa

```bash
pip install fastmcp gradio requests
python meteo_mcp.py     # avvia il server MCP
python app.py           # avvia l'interfaccia Gradio
```

## File

| File | Descrizione |
|---|---|
| `meteo_mcp.py` | Server MCP principale |
| `app.py` | Interfaccia Gradio |
| `frontend.html` | Frontend HTML standalone |
| `requirements.txt` | Dipendenze Python |

## Tecnologie

- `FastMCP` — Model Context Protocol server
- `Gradio` — interfaccia web
- API meteo pubblica per dati italiani

## Tag

`python` `fastmcp` `mcp` `gradio` `meteo` `weather` `italia` `llm` `claude`
