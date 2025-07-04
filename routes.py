from flask import Blueprint, jsonify, request
from aviation_api import fetch_flight_data

from collections import defaultdict
from datetime import datetime

api = Blueprint('api', __name__)

@api.route("/api/summary")
def summary():
    data = fetch_flight_data(200)
    total_flights = len(data)

    route_count = defaultdict(int)
    date_count = defaultdict(int)

    for flight in data:
        dep = flight.get("departure", {}).get("airport")
        arr = flight.get("arrival", {}).get("airport")
        date = flight.get("departure", {}).get("scheduled")
        if dep and arr:
            route_count[f"{dep} → {arr}"] += 1
        if date:
            try:
                date_only = datetime.fromisoformat(date).strftime("%Y-%m-%d")
                date_count[date_only] += 1
            except:
                continue

    most_popular_route = max(route_count.items(), key=lambda x: x[1], default=("N/A", 0))
    peak_date = max(date_count.items(), key=lambda x: x[1], default=("N/A", 0))

    return jsonify({
        "total_flights": total_flights,
        "most_popular_route": most_popular_route[0],
        "peak_demand_date": peak_date[0]
    })

@api.route("/api/routes")
def top_routes():
    data = fetch_flight_data(200)
    route_map = defaultdict(int)

    for flight in data:
        dep = flight.get("departure", {}).get("airport")
        arr = flight.get("arrival", {}).get("airport")
        if dep and arr:
            route_map[(dep, arr)] += 1

    sorted_routes = sorted(route_map.items(), key=lambda x: x[1], reverse=True)[:10]

    output = []
    for (dep, arr), count in sorted_routes:
        output.append({
            "route": f"{dep} → {arr}",
            "passengers": count,
            "growth": 0.0,
            "departure_code": dep,
            "arrival_code": arr
        })

    return jsonify({"routes": output})

@api.route("/api/airports")
def airports():
    data = fetch_flight_data(200)
    seen = {}
    for flight in data:
        for side in ['departure', 'arrival']:
            airport = flight.get(side, {}).get("airport")
            code = flight.get(side, {}).get("iata")
            if airport and code:
                seen[code] = airport
    return jsonify([{"code": code, "name": name} for code, name in seen.items()])

@api.route("/api/routes/filter")
def filter_routes():
    data = fetch_flight_data(200)
    dep_filter = request.args.get("departure")
    arr_filter = request.args.get("arrival")
    start = request.args.get("start")
    end = request.args.get("end")

    output = []
    for flight in data:
        dep = flight.get("departure", {}).get("airport")
        arr = flight.get("arrival", {}).get("airport")
        code_dep = flight.get("departure", {}).get("iata")
        code_arr = flight.get("arrival", {}).get("iata")
        date = flight.get("departure", {}).get("scheduled")

        if not (dep and arr and date): continue

        if dep_filter and code_dep != dep_filter: continue
        if arr_filter and code_arr != arr_filter: continue

        if start and end:
            try:
                date_obj = datetime.fromisoformat(date).date()
                start_date = datetime.strptime(start, "%Y-%m-%d").date()
                end_date = datetime.strptime(end, "%Y-%m-%d").date()
                if not (start_date <= date_obj <= end_date):
                    continue
            except:
                continue

        output.append({
            "route": f"{dep} → {arr}",
            "passengers": 1,
            "growth": 0.0,
            "departure_code": code_dep,
            "arrival_code": code_arr
        })

    return jsonify({"routes": output})

@api.route("/api/metrics")
def metrics():
    data = fetch_flight_data(200)
    total = len(data)
    carriers = set(flight.get("airline", {}).get("name") for flight in data if flight.get("airline", {}).get("name"))
    countries = set(flight.get("departure", {}).get("country") for flight in data if flight.get("departure", {}).get("country"))

    return jsonify({
        "total_flights": total,
        "unique_airlines": len(carriers),
        "countries_served": len(countries)
    })
