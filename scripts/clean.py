import json
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RAW_DATA_PATH = os.getenv("RAW_DATA_PATH", "data/raw/raw_jobs.json")

def clean_himalayas_jobs(raw_filepath=RAW_DATA_PATH):
    print(f" [2/3] Cleaning data from file: {raw_filepath}")
    
    if not os.path.exists(raw_filepath):
        raise FileNotFoundError(f"Missing file: {raw_filepath}. Did you run extract.py first?")

    with open(raw_filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # 1. Select key fields from Himalayas API response
    cols = ["guid", "title", "companyName", "minSalary", "maxSalary", "currency", "locationRestrictions", "pubDate"]
    df = df[[c for c in cols if c in df.columns]].copy()
    df = df[[c for c in cols if c in df.columns]].copy()

    # 2. Rename columns to standard SQL names
    df.rename(columns={
        "guid": "job_id",
        "title": "position",
        "companyName": "company",
        "pubDate": "posted_date"
    }, inplace=True)

    # 3. Handle missing values
    df["company"] = df["company"].fillna("Unknown")
    df["position"] = df["position"].fillna("Unspecified")
    df["currency"] = df["currency"].fillna("USD")

    # 4. Salary calculation
    df["minSalary"] = pd.to_numeric(df.get("minSalary"), errors="coerce").fillna(0)
    df["maxSalary"] = pd.to_numeric(df.get("maxSalary"), errors="coerce").fillna(0)
    df["avg_salary"] = (df["minSalary"] + df["maxSalary"]) / 2

    # 5. Format location restrictions (handles strings and dictionaries safely)
    def extract_locations(locs):
        if not isinstance(locs, list) or not locs:
            return "Worldwide"
        
        extracted = []
        for loc in locs:
            if isinstance(loc, dict):
                extracted.append(loc.get("name", "Unknown"))
            elif isinstance(loc, str):
                extracted.append(loc)
        return ", ".join(extracted) if extracted else "Worldwide"

    df["location"] = df["locationRestrictions"].apply(extract_locations)

    # 6. Datetime formatting
    df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")

    cleaned_df = df[["job_id", "company", "position", "location", "avg_salary", "currency", "posted_date"]]
    print(f"Cleaned {len(cleaned_df)} records.")
    return cleaned_df

if __name__ == "__main__":
    df = clean_himalayas_jobs()
    print(df.head())