"""MCP-Meteo-Italia: meteo attuale e previsioni per qualsiasi comune italiano.

Dati: Open-Meteo (gratuito, senza API key).
"""
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("Meteo Italia")

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = 10.0

CODICI_METEO = {
    0: "Sereno ☀️",
    1: "Prevalentemente sereno 🌤️",
    2: "Parzialmente nuvoloso ⛅",
    3: "Nuvoloso ☁️",
    45: "Nebbia 🌫️",
    48: "Nebbia con brina 🌫️",
    51: "Pioggerella leggera 🌦️",
    53: "Pioggerella moderata 🌦️",
    55: "Pioggerella intensa 🌧️",
    61: "Pioggia leggera 🌧️",
    63: "Pioggia moderata 🌧️",
    65: "Pioggia intensa 🌧️",
    71: "Neve leggera ❄️",
    73: "Neve moderata ❄️",
    75: "Neve intensa ❄️",
    80: "Rovesci leggeri 🌦️",
    81: "Rovesci moderati 🌧️",
    82: "Rovesci intensi ⛈️",
    95: "Temporale ⛈️",
    96: "Temporale con grandine ⛈️",
    99: "Temporale forte con grandine ⛈️",
}


def descrizione(code: int) -> str:
    return CODICI_METEO.get(code, f"Condizione meteo {code}")


async def trova_citta(client: httpx.AsyncClient, nome: str) -> dict | None:
    """Cerca un comune italiano per nome. Restituisce None se non trovato."""
    r = await client.get(
        GEOCODING_URL,
        params={"name": nome.strip(), "count": 5, "language": "it", "countryCode": "IT"},
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    risultati = r.json().get("results") or []
    return risultati[0] if risultati else None


def etichetta(luogo: dict) -> str:
    provincia = luogo.get("admin2") or luogo.get("admin1")
    return f"{luogo['name']} ({provincia})" if provincia else luogo["name"]


@mcp.tool()
async def get_meteo(city: str) -> str:
    """
    Meteo ATTUALE di un comune italiano qualsiasi.

    Args:
        city: Nome del comune (es. Milano, Carugate, Matera)

    Returns:
        Temperatura, condizione, vento e umidità in questo momento.
    """
    try:
        async with httpx.AsyncClient() as client:
            luogo = await trova_citta(client, city)
            if not luogo:
                return f"❌ Comune '{city}' non trovato in Italia. Controlla l'ortografia."
            r = await client.get(
                FORECAST_URL,
                params={
                    "latitude": luogo["latitude"],
                    "longitude": luogo["longitude"],
                    "current": "temperature_2m,weathercode,windspeed_10m,relativehumidity_2m",
                    "timezone": "Europe/Rome",
                },
                timeout=TIMEOUT,
            )
            r.raise_for_status()
            c = r.json()["current"]
    except httpx.HTTPError as e:
        return f"❌ Servizio meteo non raggiungibile: {e}"

    return (
        f"🏙️ {etichetta(luogo)}: {c['temperature_2m']}°C, {descrizione(c['weathercode'])}\n"
        f"💨 Vento: {c['windspeed_10m']} km/h | 💧 Umidità: {c['relativehumidity_2m']}%"
    )


@mcp.tool()
async def get_previsioni(city: str, giorni: int = 3) -> str:
    """
    Previsioni giornaliere per un comune italiano qualsiasi.

    Args:
        city: Nome del comune (es. Roma, Carugate, Matera)
        giorni: Quanti giorni di previsione, da 1 a 7 (default 3)

    Returns:
        Per ogni giorno: condizione, temperatura minima/massima,
        probabilità di precipitazioni e millimetri di pioggia attesi.
    """
    giorni = max(1, min(7, giorni))
    try:
        async with httpx.AsyncClient() as client:
            luogo = await trova_citta(client, city)
            if not luogo:
                return f"❌ Comune '{city}' non trovato in Italia. Controlla l'ortografia."
            r = await client.get(
                FORECAST_URL,
                params={
                    "latitude": luogo["latitude"],
                    "longitude": luogo["longitude"],
                    "daily": "weathercode,temperature_2m_max,temperature_2m_min,"
                             "precipitation_probability_max,precipitation_sum",
                    "forecast_days": giorni,
                    "timezone": "Europe/Rome",
                },
                timeout=TIMEOUT,
            )
            r.raise_for_status()
            d = r.json()["daily"]
    except httpx.HTTPError as e:
        return f"❌ Servizio meteo non raggiungibile: {e}"

    righe = [f"📅 Previsioni per {etichetta(luogo)}:"]
    for i, giorno in enumerate(d["time"]):
        prob = d["precipitation_probability_max"][i]
        righe.append(
            f"{giorno}: {descrizione(d['weathercode'][i])}, "
            f"{d['temperature_2m_min'][i]}°–{d['temperature_2m_max'][i]}°C, "
            f"pioggia {prob if prob is not None else '?'}% ({d['precipitation_sum'][i]} mm)"
        )
    return "\n".join(righe)


if __name__ == "__main__":
    mcp.run()
