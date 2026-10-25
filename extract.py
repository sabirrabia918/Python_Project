import requests, time
from config import API_URL, PAGES, LIMIT

def fetch_launches():
    results, offset = [], 0
    for _ in range(PAGES):
        r = requests.get(
            API_URL,
            params={"limit": LIMIT, "offset": offset, "mode": "detailed"},
            timeout=30,
        )
        if r.status_code == 429:
            print("Rate limit reached. Saving the data collected so far.")
            break
        r.raise_for_status()
        data = r.json()
        results += data["results"]
        print(f"Fetched {len(results)} launches")
        if not data.get("next"):
            break
        offset += LIMIT
        time.sleep(2)
    return results