"""
dashboard.py

Interactive Streamlit dashboard for exploring the merged economic
indicators dataset. Run with:

    streamlit run src/dashboard.py
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

PROCESSED_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "processed" / "merged.csv"
)

st.set_page_config(page_title="Economic Trends Dashboard", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(PROCESSED_PATH, parse_dates=["date"])
    return df


def main():
    st.title("📈 U.S. Economic Trends Dashboard")
    st.caption("Data source: FRED (Federal Reserve Economic Data)")

    if not PROCESSED_PATH.exists():
        st.error(
            "Processed data not found. Run `python src/fetch_data.py` then "
            "`python src/process_data.py` first."
        )
        return

    df = load_data()

    # --- Sidebar controls ---
    st.sidebar.header("Filters")
    min_date, max_date = df["date"].min(), df["date"].max()
    date_range = st.sidebar.slider(
        "Date range",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
    )

    filtered = df[(df["date"] >= date_range[0]) & (df["date"] <= date_range[1])]

    metric_options = {
        "GDP (nominal, $B)": "gdp",
        "Unemployment rate (%)": "unemployment_rate",
        "CPI (index)": "cpi",
        "Fed funds rate (%)": "fed_funds_rate",
        "GDP YoY growth (%)": "gdp_yoy_pct",
        "Inflation YoY (%)": "cpi_yoy_pct",
    }
    selected_labels = st.sidebar.multiselect(
        "Indicators to plot",
        options=list(metric_options.keys()),
        default=["Unemployment rate (%)", "Inflation YoY (%)", "Fed funds rate (%)"],
    )
    selected_cols = [metric_options[label] for label in selected_labels]

    # --- Main chart ---
    if selected_cols:
        long_df = filtered.melt(
            id_vars="date", value_vars=selected_cols, var_name="indicator", value_name="value"
        )
        fig = px.line(
            long_df,
            x="date",
            y="value",
            color="indicator",
            title="Selected indicators over time",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select at least one indicator from the sidebar.")

    # --- Correlation heatmap ---
    st.subheader("Correlation between indicators")
    corr_cols = ["gdp_yoy_pct", "unemployment_rate", "cpi_yoy_pct", "fed_funds_rate"]
    corr = filtered[corr_cols].corr()
    fig_corr = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="Correlation matrix (selected date range)",
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    # --- Raw data ---
    with st.expander("View raw data"):
        st.dataframe(filtered)


if __name__ == "__main__":
    main()
