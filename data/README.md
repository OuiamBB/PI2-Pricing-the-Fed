# Data Directory — PI2 Team P153_T2

This directory contains the cleaned, standardized datasets for the project **Pricing the Fed: Extracting Monetary Policy Expectations from Market Data**.

All heavy raw Bloomberg extractions (`.xlsx`) are kept locally in raw archives to ensure fast, zero-bug loading in Python notebooks.

---

## 📁 Available Datasets & Data Dictionary

| File Name | Source | Description | Primary Users |
| :--- | :--- | :--- | :--- |
| **`wirp_snapshots_2026.csv`** | Bloomberg `WIRP <GO>` | Snapshots of upcoming 18 FOMC meetings (implied rates, expected moves in bp, probabilities under Futures and OIS models) | **Ouiam (M2), Erian (M1)** |
| **`fed_funds_recent_contracts.csv`** | Bloomberg `FFV26` to `FFZ27` | Daily price history (`px_last`, `px_settle`, `px_volume`, `open_interest`) across recent 30-Day Fed Funds contracts | **Erian (M1), Justine (M3)** |
| **`reference_rates_bloomberg.csv`** | Bloomberg | Daily official fixings for Effective Federal Funds Rate (`effr`) and Secured Overnight Financing Rate (`sofr`) | **ALL (Team)** |
| **`fed_rates.csv`** | FRED (St. Louis Fed) | Historical series for Fed target range bounds (`target_upper`, `target_lower`), `target_midpoint`, and `effr` | **ALL (Team)** |
| **`sofr_futures_recent.csv`** | Bloomberg `SFRU26` to `SFRZ27` | Daily settlement prices for 3-Month SOFR futures (3rd to 5th contracts for Acosta et al. methodology) | **Assunta (M4)** |
| **`macro_surprises_clean.csv`** | Bloomberg `ECO <GO>` | Economic releases for CPI, Core CPI, NFP, Unemployment: `actual`, `survey_median`, and computed `surprise` ($A - E$) | **Yasmine (M5)** |
| **`treasury_2y_yield.csv`** | Bloomberg `USGG2YR Index` | Daily constant-maturity 2-year US Treasury yield (1990–2026) | **Yasmine (M5)** |
| **`fomc_calendar.csv`** | Federal Reserve Board | FOMC meeting dates (2024–2026) and flags for Summary of Economic Projections / dot plot releases (`sep_dot_plot`) | **ALL (Team)** |

---

## 🧹 Data Cleaning Pipeline Applied

1. **Header & Metadata Removal:** Bloomberg terminal exports include 5 to 6 metadata rows (`Security`, `Start Date`, `End Date`, `Period`). These were stripped to expose pure column headers at row 1.
2. **Standard Column Naming:** All column headers follow lower-case `snake_case` conventions.
3. **Date Standardization:** All dates parsed into standard ISO format (`YYYY-MM-DD`).
4. **Unit Normalization:**
   - Rates: Stored in percentage points (e.g. `4.25` = 4.25%).
   - Price Changes & Moves: Stored in basis points (e.g. `25.0` = 25 bp).
   - Probabilities: Stored as decimals between 0 and 1 (e.g. `0.60` = 60%).
5. **No Broken Paths:** All notebooks can load files with relative paths, e.g.:
   ```python
   import pandas as pd
   df = pd.read_csv('../data/wirp_snapshots_2026.csv')
   ```
