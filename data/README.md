# Data Directory — PI2 Team P153_T2 (Complete Historical Datasets)

This directory contains the **COMPLETE historical datasets** extracted from the Bloomberg Terminal (1990–2028), cleaned, standardized, and ready to be loaded by Python notebooks with zero bugs.

---

## 📁 Available Historical Datasets

| File Name | Horizon / Scope | Rows | Description | Primary Users |
| :--- | :--- | :---: | :--- | :--- |
| **`fed_funds_futures_history.csv`** | **2010 – 2028** | **181 067** | All 228 monthly 30-Day Fed Funds contracts (`FFF10` to `FFZ28`). Daily settlement prices, volumes, open interest. | **Justine (M3), Erian (M1)** |
| **`sofr_futures_history.csv`** | **2018 – 2028** | **50 509** | All 43 quarterly 3-Month SOFR futures contracts (`SFRM18` to `SFRZ28`) since inception on CME. | **Assunta (M4)** |
| **`eurodollar_futures_history.csv`** | **2010 – 2023** | **138 064** | All 54 quarterly Eurodollar futures contracts (`EDH10` to `EDM23`) up to LIBOR cessation. | **Assunta (M4)** |
| **`wirp_historical_snapshots.csv`** | **2015 – 2026** | **78** | Real Bloomberg WIRP snapshots at key pivot dates (2015, 2018, 2020, 2021, 2024, 2026). | **Ouiam (M2), Erian (M1)** |
| **`wirp_snapshots_2026.csv`** | **2026 – 2028** | **18** | Current Bloomberg WIRP snapshot for upcoming FOMC meetings (Futures vs OIS models). | **Ouiam (M2), Erian (M1)** |
| **`macro_surprises_clean.csv`** | **1997 – 2026** | **3 241** | Raw Bloomberg export for CPI, Core CPI, NFP, Unemployment. Columns are shifted and `surprise` is empty: use `macro_event_study/macro_surprises_fixed.csv` instead. | **Yasmine (M5)** |
| **`macro_event_study/macro_surprises_fixed.csv`** | **1997 – 2026** | **1 424** | Corrected panel, one row per release, with `actual`, `survey_median` and `surprise` ($A - E$). Built by notebook 05. | **Yasmine (M5)** |
| **`treasury_2y_yield.csv`** | **1990 – 2026** | **9 602** | Full daily constant-maturity 2-year US Treasury yield. | **Yasmine (M5)** |
| **`reference_rates_bloomberg.csv`** | **1990 – 2026** | **9 364** | Daily official fixings for Effective Federal Funds Rate (`effr`) and Secured Overnight Financing Rate (`sofr`). | **ALL (Team)** |
| **`fomc_events_history_1990_2026.csv`** | **1990 – 2026** | **388** | Complete list of all historical FOMC announcement events, timestamps, and metadata. | **Assunta (M4), Yasmine (M5)** |
| **`fomc_calendar.csv`** | **2024 – 2026** | **24** | Scheduled FOMC meeting dates and SEP dot plot release flags. | **ALL (Team)** |

---

## ⚡ Loading in Python

```python
import pandas as pd

# Load 15 years of Fed Funds futures daily history:
df_ff = pd.read_csv('../data/fed_funds_futures_history.csv')

# Load historical WIRP snapshots:
df_wirp_hist = pd.read_csv('../data/wirp_historical_snapshots.csv')

# Load corrected macroeconomic surprises (1997-2026):
df_macro = pd.read_csv('../data/macro_event_study/macro_surprises_fixed.csv')
```
