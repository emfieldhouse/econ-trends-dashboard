"""
fetch_data.py

Pulls raw economic time-series data from the FRED (Federal Reserve
Economic Data) API and saves each series as its own CSV in data/raw/.

Requires a free FRED API key set as FRED_API_KEY in a .env file
(see .env.example).
"""

import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Series to pull: FRED series ID -> human-readable name
SERIES = {
    "GDP": "gdp",
    "UNRATE": "unemployment_rate",
    "CPIAUCSL": "cpi",
    "FEDFUNDS": "fed_funds_rate",
}


def fetch_series(series_id: str, start_date: str = "1960-01-01") -> pd.DataFrame:
    """Fetch one FRED series and return it as a DataFrame with date/value columns."""
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
    }
    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()

    df = pd.DataFrame(payload["observations"])[["date", "value"]]
    df["date"] = pd.to_datetime(df["date"])
    # FRED uses "." for missing values
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df


def main():
    if not FRED_API_KEY:
        raise SystemExit(
            "FRED_API_KEY not found. Copy .env.example to .env and add your "
            "free API key from https://fred.stlouisfed.org/docs/api/api_key.html"
        )

    for series_id, name in SERIES.items():
        print(f"Fetching {series_id} ({name})...")
        df = fetch_series(series_id)
        out_path = RAW_DIR / f"{name}.csv"
        df.to_csv(out_path, index=False)
        print(f"  Saved {len(df)} rows -> {out_path}")

    print("\nDone. Run src/process_data.py next.")


if __name__ == "__main__":
    main()
