import requests

TRAVELPAYOUTS_API_TOKEN = "f07042db2e352fe2777cc4439ae24895"

def get_flight_prices(origin="DEL", destination="BOM"):
    url = "https://api.travelpayouts.com/aviasales/v3/get_latest_prices"
    params = {
        "origin": origin,
        "destination": destination,
        "currency": "inr",
        "token": TRAVELPAYOUTS_API_TOKEN
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data.get("data", [])
    except Exception:
        return []
