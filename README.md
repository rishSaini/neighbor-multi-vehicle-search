# Multi-Vehicle Search API

A **FastAPI-powered application** built for the *Multi-Vehicle Search Take-Home Challenge*.  
This API helps renters find the **best storage locations** that can accommodate multiple vehicles —  
always returning the **cheapest possible combination of listings** per location.

## Overview

You provide a list of vehicles (each with a specific length and quantity),  
and the API determines:

1. Which **locations** can fit all of those vehicles  
2. The **lowest-cost** combination of listings that meets the space requirements  
3. One result per location, **sorted by total price (lowest first)**  

**Assumption**: Each vehicle has a width of **10 feet**.

## Key Features

- Supports multiple vehicles per listing (lane-based storage)
- Always returns the **cheapest valid setup** for each location
- Handles up to **five vehicles per request**
- Optimized for performance (**under 300ms**)
- Fully tested using **pytest** and FastAPI’s **TestClient**

## Example Request

```bash
curl -X POST "http://127.0.0.1:8000/" \
  -H "Content-Type: application/json" \
  -d '[
        {"length": 10, "quantity": 1},
        {"length": 20, "quantity": 2},
        {"length": 25, "quantity": 1}
      ]'
