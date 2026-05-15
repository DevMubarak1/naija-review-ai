"""Quick test script for Task B — Recommendations."""
import requests
import json

r = requests.post('http://localhost:8000/task-b/recommend', json={
    'user_id': 'demo_user_001',
    'query': 'I need good headphones for music in Lagos traffic',
    'is_nigerian': True,
    'top_k': 5,
    'user_reviews': [
        {'rating': 5, 'review_text': 'Amazing product! Best thing I bought.', 'item_name': 'JBL Speaker', 'category': 'Electronics'},
        {'rating': 4, 'review_text': 'Great book, really enjoyed reading it.', 'item_name': 'Things Fall Apart', 'category': 'Books'},
    ]
}, timeout=120)

print('Status:', r.status_code)
data = r.json()
print(f"Got {len(data.get('recommendations', []))} recommendations")
print(f"Candidates considered: {data.get('total_candidates_considered')}")
print()

for rec in data.get('recommendations', []):
    print(f"  #{rec['rank']}. {rec['item_name']}")
    print(f"     Category: {rec.get('category', 'N/A')}")
    print(f"     Score: {rec.get('score', 0):.2f}")
    print(f"     Why: {rec.get('explanation', '')[:150]}")
    print()
