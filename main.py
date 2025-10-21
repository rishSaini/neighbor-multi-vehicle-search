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

