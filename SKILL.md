---
name: meteo-italia
description: Meteo attuale e previsioni fino a 7 giorni per qualsiasi comune italiano. Usa questa skill quando l'utente chiede tempo, temperatura, pioggia, neve, vento o se serve l'ombrello in una località in Italia.
---

# Meteo Italia

Skill che insegna all'agente a usare il server MCP **MCP-Meteo-Italia** (dati Open-Meteo, nessuna API key).

## Setup

1. Installa le dipendenze: `pip install -r requirements.txt`
2. Registra il server MCP nel tuo agente, ad esempio per Claude Code:
   `claude mcp add meteo-italia -- python /percorso/meteo_mcp.py`

## Tool disponibili

| Tool | Quando usarlo |
|------|---------------|
| `get_meteo(city)` | "Che tempo fa ora a...?", temperatura o condizioni **adesso** |
| `get_previsioni(city, giorni)` | "Domani piove?", weekend, settimana, "serve l'ombrello?" (1-7 giorni) |

Funzionano per **qualsiasi comune italiano**, anche piccolo (es. Carugate, Matera).

## Come usarli

- Il parametro `city` è solo il nome del comune, senza provincia né "Italia": `Bologna`, non `Bologna, Emilia-Romagna`.
- Se l'utente dice "domani", chiama `get_previsioni` con `giorni=2` e leggi la seconda riga. Per "weekend" o "settimana" usa `giorni=7` e scegli i giorni giusti.
- Se l'utente non indica la località, **chiedila**: non indovinare.
- Se la risposta inizia con ❌ "non trovato", chiedi di controllare l'ortografia o proponi un comune vicino. Non inventare dati.
- Se il servizio non è raggiungibile, dillo chiaramente e non fornire stime a memoria.

## Come rispondere

- In italiano, breve e diretto: prima la risposta alla domanda, poi i dettagli.
- Usa i dati restituiti così come sono, senza arrotondarli in modo fuorviante.
- Pioggia: sotto il 30% di probabilità "poco probabile", tra 30% e 60% "possibile", sopra il 60% "probabile, porta l'ombrello".
- Non sono allerte ufficiali. Per allerte meteo e protezione civile rimanda alla Protezione Civile o alla ARPA regionale.

## Esempi

**Utente:** Serve l'ombrello domani a Milano?
**Azione:** `get_previsioni(city="Milano", giorni=2)`, leggere il secondo giorno.
**Risposta:** "Domani a Milano pioggia probabile (70%, circa 4 mm), tra 12° e 17°C: sì, porta l'ombrello."

**Utente:** Com'è il tempo a Carugate?
**Azione:** `get_meteo(city="Carugate")`
**Risposta:** "Ora a Carugate ci sono 14°C, nuvoloso, vento leggero e umidità al 78%."

## Limiti

- Solo Italia (la ricerca è limitata ai comuni italiani).
- Nessuna allerta ufficiale né dati storici.
- Previsioni fino a 7 giorni.
