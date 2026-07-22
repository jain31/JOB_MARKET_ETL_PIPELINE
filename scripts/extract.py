import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read the URL and Path strictly from .env
API_URL = os.getenv("API_URL")
RAW_DATA_PATH = os.getenv("RAW_DATA_PATH", "data/raw/raw_jobs.json")

def extract_himalayas_jobs(max_jobs=100):
    if not API_URL:
        raise ValueError("Error: API_URL is missing from your .env file!")

    # Generic log message — API URL is hidden from terminal logs
    print("[1/3] Extracting data from configured API...")
    
    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    
    offset = 0
    limit = 20
    all_jobs = []

    while len(all_jobs) < max_jobs:
        params = {"limit": limit, "offset": offset}
        headers = {"User-Agent": "Mozilla/5.0"}
        
        response = requests.get(API_URL, params=params, headers=headers)
        if response.status_code != 200:
            print(f"API Error: HTTP {response.status_code}")
            break

        data = response.json()
        jobs_batch = data.get("jobs", [])
        total_count = data.get("totalCount", 0)

        if not jobs_batch:
            break

        all_jobs.extend(jobs_batch)
        offset += limit
        
        if offset >= total_count:
            break

    with open(RAW_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"Extracted {len(all_jobs)} jobs -> {RAW_DATA_PATH}")
    return RAW_DATA_PATH

if __name__ == "__main__":
    extract_himalayas_jobs()