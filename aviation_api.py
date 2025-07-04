import requests

def fetch_flight_data(limit=10):
    url = "http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": "985ad138641e4a0ee42fa7c197bf09ae",  # Your real key
        "limit": limit
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        else:
            return []
    except Exception as e:
        print(f"[ERROR] Failed to fetch flight data: {e}")
        return []
