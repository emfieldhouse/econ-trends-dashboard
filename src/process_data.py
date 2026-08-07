"""
process_data.py

Loads the raw CSVs from data/raw/, resamples everything to a common
monthly frequency, merges into a single tidy DataFrame, computes a few
derived metrics (YoY % change, rolling averages), and saves the result
to data/processed/merged.csv.
"""

from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

SERIES_FILES = {
    "gdp": "gdp.csv",                       # quarterly
    "unemployment_rate": "unemployment_rate.csv",  # monthly
    "cpi": "cpi.csv",                       # monthly
    "fed_funds_rate": "fed_funds_rate.csv", # monthly
}


def load_series(filename: str, value_name: str) -> pd.DataFrame:
    df = pd.read_csv(RAW_DIR / filename, parse_dates=["date"])
    df = df.rename(columns={"value": value_name})
    return df.set_index("date")[[value_name]]


def main():
    frames = []
    for name, filename in SERIES_FILES.items():
        path = RAW_DIR / filename
        if not path.exists():
            raise SystemExit(
                f"Missing {path}. Run src/fetch_data.py first."
            )
        frames.append(load_series(filename, name))

    # Resample everything to month-end frequency, forward-filling
    # quarterly series (like GDP) so it lines up with monthly ones.
    resampled = [f.resample("ME").mean().ffill() for f in frames]
    merged = pd.concat(resampled, axis=1).dropna(how="all")

    # Derived metrics
    merged["gdp_yoy_pct"] = merged["gdp"].pct_change(12) * 100
    merged["cpi_yoy_pct"] = merged["cpi"].pct_change(12) * 100  # headline inflation
    merged["unemployment_rate_3m_avg"] = (
        merged["unemployment_rate"].rolling(3).mean()
    )

    merged = merged.reset_index().rename(columns={"index": "date"})
    out_path = PROCESSED_DIR / "merged.csv"
    merged.to_csv(out_path, index=False)

    print(f"Saved merged dataset ({len(merged)} rows) -> {out_path}")
    print("\nPreview:")
    print(merged.tail())


if __name__ == "__main__":
    main()
