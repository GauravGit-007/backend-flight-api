import requests
from datetime import datetime

# AviationStack API
AVIATIONSTACK_API_KEY = "985ad138641e4a0ee42fa7c197bf09ae"

def fetch_flight_data(limit=10):
    url = "http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "limit": limit
    }
    response = requests.get(url, params=params)
    #print(f"[DEBUG] AviationStack Status: {response.status_code}")
   #print(f"[DEBUG] AviationStack Body: {response.text}")
    data = response.json()
    return data.get("data", [])

# Travelpayouts API
TRAVELPAYOUTS_API_TOKEN = "f07042db2e352fe2777cc4439ae24895"

def get_flight_prices(origin="DEL", destination="BOM"):
    url = "https://api.travelpayouts.com/aviasales/v3/get_latest_prices"
    params = {
        "origin": origin,
        "destination": destination,
        "currency": "inr",
        "token": TRAVELPAYOUTS_API_TOKEN
    }
    response = requests.get(url, params=params)
    #print(f"[DEBUG] Travelpayouts Status: {response.status_code}")
    #print(f"[DEBUG] Travelpayouts Body: {response.text}")
    try:
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        print(f"[ERROR] Failed to fetch flight prices: {e}")
        return []

# Print final combined result
def print_combined_output():
    print("\n✈️  TOP 10 LIVE FLIGHTS (From AviationStack)")
    print("==============================================")
    flights = fetch_flight_data(limit=10)

    if not flights:
        print("No flight data returned.")
    else:
        for i, flight in enumerate(flights, 1):
            dep = flight.get("departure", {}) or {}
            arr = flight.get("arrival", {}) or {}
            airline = flight.get("airline", {}) or {}
            print(f"{i}. {dep.get('iata', 'N/A')} → {arr.get('iata', 'N/A')} | Airline: {airline.get('name', 'N/A')} | Status: {flight.get('flight_status', 'N/A')}")

    print("\n💸 TOP FLIGHT PRICES (From Travelpayouts)")
    print("==============================================")
    prices = get_flight_prices(origin="DEL", destination="BOM")

    if not prices:
        print("No pricing data returned.")
        return

    for i, item in enumerate(prices[:10], 1):
        origin = item.get("origin", "N/A")
        destination = item.get("destination", "N/A")
        price = item.get("value", "N/A")
        airline = item.get("gate", "N/A")
        depart_date = item.get("depart_date", "N/A")

        print(f"{i}. {origin} → {destination} | Provider: {airline} | Price: ₹{price} | Date: {depart_date}")
        print("------------------------------------------------------")

if __name__ == "__main__":
    print_combined_output()
