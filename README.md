# Economic Trends Dashboard

Analyze and visualize U.S. macroeconomic indicators — GDP, unemployment,
inflation (CPI), and interest rates — using data from the Federal Reserve
Economic Data (FRED) API.

## What this project shows

- Pulling and cleaning real time-series data from a public API
- Merging multiple series with different frequencies (monthly/quarterly) onto
  a common timeline
- Computing derived metrics (YoY % change, rolling averages)
- Visualizing trends and correlations between indicators
- An optional interactive Streamlit dashboard for exploring the data live

## Key question this analysis answers

> How have inflation, unemployment, and interest rates moved together (or
> apart) over the last several decades — and what does that suggest about
> the trade-offs policymakers face?

(Feel free to adjust this to whatever angle interests you — e.g. focus on a
specific recession, compare pre/post-2020, etc.)

## Project structure

```
econ-trends-dashboard/
├── src/
│   ├── fetch_data.py       # pulls raw series from FRED, saves to data/raw
│   ├── process_data.py     # cleans/merges series, saves to data/processed
│   └── dashboard.py        # Streamlit interactive dashboard
├── notebooks/
│   └── analysis.ipynb      # main exploratory analysis + charts
├── data/
│   ├── raw/                # untouched API responses (gitignored)
│   └── processed/          # cleaned, merged datasets (gitignored)
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

1. Get a free FRED API key: https://fred.stlouisfed.org/docs/api/api_key.html

2. Create your environment file:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and paste in your API key.

3. Install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows (Git Bash): source venv/Scripts/activate
   pip install -r requirements.txt
   ```

4. Fetch and process the data:
   ```bash
   python src/fetch_data.py
   python src/process_data.py
   ```

5. Open the notebook:
   ```bash
   jupyter notebook notebooks/analysis.ipynb
   ```

6. (Optional) Launch the interactive dashboard:
   ```bash
   streamlit run src/dashboard.py
   ```

## Indicators used (default)

| Series ID  | Description                          |
|------------|---------------------------------------|
| `GDP`      | Gross Domestic Product (quarterly)    |
| `UNRATE`   | Unemployment Rate (monthly)           |
| `CPIAUCSL` | Consumer Price Index (monthly)        |
| `FEDFUNDS` | Federal Funds Effective Rate (monthly)|

You can add more by editing the `SERIES` dict in `src/fetch_data.py` —
browse available series at https://fred.stlouisfed.org/

## Next steps / ideas to extend this

- Add recession shading (using NBER recession dates) to your charts
- Build a simple forecast (e.g. ARIMA or Prophet) for one series
- Compare the U.S. to another country's equivalent indicators
- Deploy the Streamlit dashboard publicly (Streamlit Community Cloud is free)
