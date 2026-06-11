import gradio as gr
from gradio.mcp import GradioMCPServer
from meteo_mcp import mcp, get_meteo

# ── Leggi il frontend HTML ─────────────────────────────────────────────────────
with open("frontend.html", "r", encoding="utf-8") as f:
    HTML_CONTENT = f.read()

# ── Wrapper Gradio per il tool meteo ──────────────────────────────────────────
async def meteo_gradio(city: str) -> str:
    """Chiama il tool MCP get_meteo e restituisce il risultato."""
    return await get_meteo(city)

# ── Interfaccia ───────────────────────────────────────────────────────────────
with gr.Blocks(title="🌤️ MCP Meteo Italia", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🌤️ MCP Meteo Server — Italia")
    gr.Markdown("Server MCP con meteo in tempo reale per le principali città italiane.")

    with gr.Tabs():
        # Tab 1: Frontend HTML interattivo
        with gr.Tab("🗺️ Frontend Interattivo"):
            gr.HTML(HTML_CONTENT)

        # Tab 2: Test rapido Gradio
        with gr.Tab("⚡ Test Rapido"):
            with gr.Row():
                city_input = gr.Textbox(
                    label="Città italiana",
                    placeholder="Es: Milano, Roma, Napoli...",
                    scale=3,
                )
                submit_btn = gr.Button("🔍 Cerca Meteo", variant="primary", scale=1)

            output = gr.Textbox(label="Risultato", lines=3)
            
            examples = gr.Examples(
                examples=[["Milano"], ["Roma"], ["Napoli"], ["Firenze"], ["Venezia"]],
                inputs=city_input,
            )

            submit_btn.click(fn=meteo_gradio, inputs=city_input, outputs=output)
            city_input.submit(fn=meteo_gradio, inputs=city_input, outputs=output)

        # Tab 3: Info endpoint MCP
        with gr.Tab("📡 Endpoint MCP"):
            gr.Markdown("""
## Come connetterti all'endpoint MCP

Il server MCP è disponibile all'endpoint `/mcp` di questo Space.

### URL completo
```
https://TUO-USERNAME-mcp-meteo-NOME.hf.space/mcp
```

### Test con curl
```bash
# Lista tools disponibili
curl -X POST https://TUO-SPACE.hf.space/mcp \\
  -H "Content-Type: application/json" \\
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'

# Chiama il tool meteo
curl -X POST https://TUO-SPACE.hf.space/mcp \\
  -H "Content-Type: application/json" \\
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_meteo","arguments":{"city":"Milano"}}}'
```

### Configura in Claude Desktop / Cursor
```json
{
  "mcpServers": {
    "meteo-italia": {
      "url": "https://TUO-SPACE.hf.space/mcp"
    }
  }
}
```
""")

    # Server MCP invisibile (necessario per esporre /mcp)
    GradioMCPServer(server=mcp, demo=demo, path="/mcp")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
