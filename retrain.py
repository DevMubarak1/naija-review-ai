"""Retrain models with fresh data from HuggingFace."""
import requests
import json
import time

print("Triggering training pipeline...")
start = time.time()

r = requests.post('http://localhost:8000/train', json={
    'amazon_max': 25000,
    'yelp_max': 20000,
    'goodreads_max': 15000,
}, timeout=900)

elapsed = time.time() - start
print(f"Status: {r.status_code} ({elapsed:.1f}s)")
print(json.dumps(r.json(), indent=2))
