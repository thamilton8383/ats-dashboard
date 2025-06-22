
import requests
import json
from datetime import datetime, timedelta
import time

# Replace with your actual key
API_KEY = "5f3bac27957d4f16a6da61f097f51ccf"

# Example game schedule with kickoff times (UTC) and stadium coordinates
games = [
    {"team": "Alabama", "kickoff": "2025-10-25T19:00:00Z", "lat": 33.208, "lon": -87.550},
    {"team": "Ohio State", "kickoff": "2025-10-25T23:30:00Z", "lat": 40.001, "lon": -83.019},
    {"team": "NFL Game", "kickoff": "2025-10-26T01:20:00Z", "lat": 40.8136, "lon": -74.0741}
]

def get_forecast(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
    response = requests.get(url)
    return response.json()

def analyze_forecast(forecast):
    alerts = []
    now = datetime.utcnow()
    for item in forecast.get("list", []):
        forecast_time = datetime.utcfromtimestamp(item["dt"])
        weather = item["weather"][0]["main"]
        wind_speed = item["wind"]["speed"]
        temp = item["main"]["temp"]

        if wind_speed >= 20:
            alerts.append({"time": forecast_time.isoformat(), "type": "High Wind", "value": wind_speed})
        if "rain" in weather.lower():
            alerts.append({"time": forecast_time.isoformat(), "type": "Rain"})
        if temp >= 90:
            alerts.append({"time": forecast_time.isoformat(), "type": "High Temp", "value": temp})
        if temp <= 32:
            alerts.append({"time": forecast_time.isoformat(), "type": "Cold Temp", "value": temp})
    return alerts

def update_alerts():
    all_alerts = {}
    now = datetime.utcnow()
    for game in games:
        kickoff = datetime.strptime(game["kickoff"], "%Y-%m-%dT%H:%M:%SZ")
        hours_to_kick = (kickoff - now).total_seconds() / 3600
        if hours_to_kick > 24:
            continue
        forecast = get_forecast(game["lat"], game["lon"])
        alerts = analyze_forecast(forecast)
        all_alerts[game["team"]] = alerts
    with open("weather_alerts.json", "w") as f:
        json.dump(all_alerts, f, indent=2, default=str)

# Run once when executed
if __name__ == "__main__":
    update_alerts()
    print("Weather alerts updated.")
