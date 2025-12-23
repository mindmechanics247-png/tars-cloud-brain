# agent/tools_weather.py
"""
tools_weather.py
Fetches current weather using OpenWeatherMap API.
Returns: {"city":..., "temp_c":..., "desc":..., "raw":...}
"""

import os
import requests
from typing import Dict

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

def get_weather(city: str) -> Dict:
    """
    Get current weather for city. If city is empty string, the caller should supply a city.
    """
    if not OPENWEATHER_API_KEY:
        return {"error": "OPENWEATHER_API_KEY not set"}
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
        main = data.get("main", {})
        weather = data.get("weather", [{}])[0]
        return {
            "city": data.get("name"),
            "temp_c": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "description": weather.get("description"),
            "raw": data
        }
    except Exception as e:
        return {"error": str(e)}
