# water/utils/weather.py
from decimal import Decimal
import requests

def fetch_temperature_c(lat, lng, when):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lng,
        "hourly": "temperature_2m",
        "start": when.strftime("%Y-%m-%dT%H:00"),
        "end": when.strftime("%Y-%m-%dT%H:00"),
        "timezone": "auto"
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    if "hourly" in data and "temperature_2m" in data["hourly"]:
        return Decimal(str(data["hourly"]["temperature_2m"][0]))
    return None
