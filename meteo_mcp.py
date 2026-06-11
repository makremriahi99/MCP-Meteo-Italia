from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("Meteo Mio")

CITTA_ITALIANE = {
    "milano": {"lat": 45.4642, "lon": 9.1900, "nome": "Milano"},
    "roma": {"lat": 41.9028, "lon": 12.4964, "nome": "Roma"},
    "napoli": {"lat": 40.8518, "lon": 14.2681, "nome": "Napoli"},
    "torino": {"lat": 45.0703, "lon": 7.6869, "nome": "Torino"},
    "firenze": {"lat": 43.7696, "lon": 11.2558, "nome": "Firenze"},
    "bologna": {"lat": 44.4949, "lon": 11.3426, "nome": "Bologna"},
    "venezia": {"lat": 45.4408, "lon": 12.3155, "nome": "Venezia"},
    "genova": {"lat": 44.4056, "lon": 8.9463, "nome": "Genova"},
    "palermo": {"lat": 38.1157, "lon": 13.3615, "nome": "Palermo"},
    "bari": {"lat": 41.1171, "lon": 16.8719, "nome": "Bari"},
    "catania": {"lat": 37.5079, "lon": 15.0830, "nome": "Catania"},
    "verona": {"lat": 45.4384, "lon": 10.9916, "nome": "Verona"},
    "trieste": {"lat": 45.6495, "lon": 13.7768, "nome": "Trieste"},
    "brescia": {"lat": 45.5416, "lon": 10.2118, "nome": "Brescia"},
    "padova": {"lat": 45.4064, "lon": 11.8768, "nome": "Padova"},
}

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


@mcp.tool()
async def get_meteo(city: str) -> str:
    """
    Ottieni il meteo attuale per una città italiana.

    Args:
        city: Nome della città italiana (es. Milano, Roma, Napoli)

    Returns:
        Stringa con temperatura e condizione meteo attuale
    """
    city_key = city.lower().strip()
    
    if city_key not in CITTA_ITALIANE:
        disponibili = ", ".join(c["nome"] for c in CITTA_ITALIANE.values())
        return f"❌ Città '{city}' non trovata. Città disponibili: {disponibili}"
    
    info = CITTA_ITALIANE[city_key]
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={info['lat']}&longitude={info['lon']}"
        f"&current=temperature_2m,weathercode,windspeed_10m,relativehumidity_2m"
        f"&timezone=Europe/Rome"
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()
    
    current = data["current"]
    temp = current["temperature_2m"]
    code = current["weathercode"]
    wind = current["windspeed_10m"]
    humidity = current["relativehumidity_2m"]
    
    condizione = CODICI_METEO.get(code, f"Condizione meteo {code}")
    
    return (
        f"🏙️ {info['nome']}: {temp}°C, {condizione}\n"
        f"💨 Vento: {wind} km/h | 💧 Umidità: {humidity}%"
    )


if __name__ == "__main__":
    mcp.run()
