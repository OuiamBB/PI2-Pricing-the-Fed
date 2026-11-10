"""
src/fed_data.py
Retrieves and analyzes Federal Reserve official policy rates:
- DFEDTARU: Federal Funds Target Range - Upper Limit
- DFEDTARL: Federal Funds Target Range - Lower Limit
- DFF: Effective Federal Funds Rate (EFFR)
Source: Federal Reserve Bank of St. Louis (FRED) public data endpoints.
"""

import pandas as pd
import numpy as np

FRED_CSV_BASE_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="

def fetch_series(series_id: str) -> pd.Series:
    """Fetch a single FRED series as a pandas Series indexed by Datetime."""
    url = f"{FRED_CSV_BASE_URL}{series_id}"
    df = pd.read_csv(url, parse_dates=['DATE'], index_col='DATE')
    # Replace non-numeric entries (such as '.') with NaN and forward fill
    df[series_id] = pd.to_numeric(df[series_id], errors='coerce')
    return df[series_id]

def fetch_fed_corridor(start_date: str = "2015-01-01") -> pd.DataFrame:
    """
    Downloads Upper Limit, Lower Limit, and EFFR.
    Computes Midpoint and the spread (EFFR - Midpoint).
    """
    upper = fetch_series("DFEDTARU")
    lower = fetch_series("DFEDTARL")
    effr = fetch_series("DFF")

    df = pd.DataFrame({
        "target_upper": upper,
        "target_lower": lower,
        "effr": effr
    }).dropna(how='all')

    # Filter by start_date
    df = df.loc[start_date:].copy()

    # Calculate midpoint and spread
    df["target_midpoint"] = (df["target_upper"] + df["target_lower"]) / 2.0
    df["effr_midpoint_spread_bp"] = (df["effr"] - df["target_midpoint"]) * 100.0

    return df

if __name__ == "__main__":
    print("Testing FRED data fetch...")
    try:
        data = fetch_fed_corridor(start_date="2024-01-01")
        print(data.tail(10))
        mean_spread = data["effr_midpoint_spread_bp"].mean()
        std_spread = data["effr_midpoint_spread_bp"].std()
        print(f"\nSpread EFFR - Midpoint since 2024: mean = {mean_spread:.2f} bp, std = {std_spread:.2f} bp")
    except Exception as e:
        print(f"Error fetching data: {e}")
