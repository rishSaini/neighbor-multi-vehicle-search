import json
from fastapi import FastAPI
from itertools import combinations

app = FastAPI()

# Load data
with open("listings.json", "r") as f:
    listings_data = json.load(f)

listings_by_location = {}
for l in listings_data:
    listings_by_location.setdefault(l["location_id"], []).append(l)

VEHICLE_WIDTH = 10

# Helpers
def capacity(listing):
    """Compute how many 10ft-wide lanes and the lane length for one orientation."""
    lanes = listing["width"] // VEHICLE_WIDTH
    lane_length = listing["length"]
    return lanes, lane_length

def can_fit_all(vehicles, listings):
    """Return True if the given listings can fit all vehicle lengths."""
    lanes = []
    for l in listings:
        num, length = capacity(l)
        lanes.extend([length] * num)

    lanes.sort(reverse=True)
    vehicles = sorted(vehicles, reverse=True)

    for v in vehicles:
        for i in range(len(lanes)):
            if lanes[i] >= v:
                lanes[i] -= v
                break
        else:
            return False
    return True

@app.get("/")
def home():
    return {
        "message": "Multi-Vehicle Search API is running!",
        "usage": "Send a POST request to '/' with a JSON body like [{'length':10,'quantity':1}]"
    }

@app.post("/")
def find_storage(request: list[dict]):
    body = request

    vehicles = []
    for item in body:
        vehicles += [item["length"]] * item["quantity"]

    if len(vehicles) == 0:
        return [] 
    
    if len(vehicles) > 5:
        return {"error": "Too many vehicles"}

    results = []

    for loc_id, listings in listings_by_location.items():
        best = None

        # Try all combinations of listings (1..N)
        for r in range(1, len(listings) + 1):
            for combo in combinations(listings, r):
                if can_fit_all(vehicles, combo):
                    total_price = sum(l["price_in_cents"] for l in combo)
                    if not best or total_price < best["total_price_in_cents"]:
                        best = {
                            "location_id": loc_id,
                            "listing_ids": [l["id"] for l in combo],
                            "total_price_in_cents": total_price,
                        }
        if best:
            results.append(best)

    results.sort(key=lambda x: x["total_price_in_cents"])
    return results
