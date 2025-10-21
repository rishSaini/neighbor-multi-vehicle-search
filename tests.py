from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_single_vehicle():
    """Single vehicle should return valid location results."""
    data = [{"length": 10, "quantity": 1}]
    response = client.post("/", json=data)
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    assert all("location_id" in r for r in results)
    assert all("listing_ids" in r for r in results)
    print("\nSingle vehicle test passed. Results count:", len(results))


def test_multiple_vehicles():
    """Multiple vehicle request should return at least one valid location."""
    data = [
        {"length": 10, "quantity": 1},
        {"length": 20, "quantity": 2},
        {"length": 25, "quantity": 1},
    ]
    response = client.post("/", json=data)
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    assert len(results) > 0
    print("\nMulti-vehicle test passed. Cheapest location:", results[0]["location_id"])


def test_too_many_vehicles():
    """Too many vehicles should return an error response."""
    data = [{"length": 10, "quantity": 6}]
    response = client.post("/", json=data)
    assert response.status_code == 200
    results = response.json()
    assert "error" in results
    print("\nToo many vehicles test passed.")


def test_no_vehicles():
    """Empty input should return an empty list."""
    data = []
    response = client.post("/", json=data)
    assert response.status_code == 200
    assert response.json() == []
    print("\nNo vehicle test passed (empty request).")


def test_vehicle_too_long():
    """Vehicle too long to fit in any listing should return no results."""
    data = [{"length": 9999, "quantity": 1}]
    response = client.post("/", json=data)
    assert response.status_code == 200
    results = response.json()
    assert results == [] 
    print("\nVehicle too long test passed (no fit possible).")


def test_max_vehicle_limit():
    """Exactly 5 vehicles should be allowed."""
    data = [
        {"length": 10, "quantity": 2},
        {"length": 15, "quantity": 3},
    ]
    response = client.post("/", json=data)
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    print("\nMax vehicle limit (5 vehicles) test passed.")


def test_exceed_vehicle_limit():
    """More than 5 vehicles should trigger an error."""
    data = [{"length": 10, "quantity": 6}]
    response = client.post("/", json=data)
    assert response.status_code == 200
    assert "error" in response.json()
    print("\nExceeded vehicle limit test passed (error shown).")


def test_sorting_correctness():
    """Ensure results are sorted by total price ascending."""
    data = [{"length": 10, "quantity": 1}]
    response = client.post("/", json=data)
    assert response.status_code == 200
    results = response.json()
    prices = [r["total_price_in_cents"] for r in results]
    assert prices == sorted(prices)
    print("\nSorting correctness test passed (ascending price order).")


def test_duplicate_length_requests():
    """Ensure multiple identical vehicle requests are handled correctly."""
    data = [{"length": 20, "quantity": 2}]
    response = client.post("/", json=data)
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    print("\nDuplicate length requests test passed (two same-length vehicles).")


def test_fit_across_multiple_listings():
    """Ensure vehicles can be distributed across multiple listings if needed."""
    data = [
        {"length": 20, "quantity": 1},
        {"length": 25, "quantity": 1},
    ]
    response = client.post("/", json=data)
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert any(len(r["listing_ids"]) > 1 for r in results)
    print("\nMulti-listing fit test passed (vehicles split correctly).")


def test_large_request_stability():
    """Ensure large but valid request runs without errors."""
    data = [{"length": 50, "quantity": 5}]
    response = client.post("/", json=data)
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    print("\nLarge request stability test passed.")