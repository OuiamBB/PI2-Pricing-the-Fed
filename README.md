# Pricing the Fed: Extracting Monetary Policy Expectations from Market Data

**ESILV — Master of Science in Financial Engineering (IF-A5) — Industrial Innovation Project (PI²)**  
**Project Reference:** P153_T2  
**Academic Supervisor:** Mr. Martino Grasselli (DVHE)  

---

## Project Team

| Team Member | Role | Primary Technical Mission |
| :--- | :--- | :--- |
| **Ouiam BOUSSAID BENCHAARA** | **Team Referent** | **Mission 2:** Bloomberg WIRP analysis, Fed policy corridor, and methodological tool comparison |
| **Erian STANLEY YOGARAJ** | Member | **Mission 1:** CME FedWatch probability model replication (binary, aggregated, and probability tree) |
| **Justine RENAUD** | Member | **Mission 3:** Historical reconstruction of market expectations at $t-30, t-7, t-1$ days prior to past FOMC meetings |
| **Assunta DAMIANO** | Member | **Mission 4:** SOFR / Eurodollar term-structure repricing around FOMC announcements (Acosta et al., 2024) |
| **Yasmine PERALDI** | Member | **Mission 5:** Macroeconomic surprises (CPI, NFP, Unemployment) and 2-Year Treasury yield event study (Healy & Jia, 2024) |

---

##  Repository Architecture

```text
PI2-Pricing-the-Fed/
├── data/                                      # Cleaned, standardized historical datasets (committed on GitHub)
│   ├── fed_funds_futures_history.csv          # COMPLETE Fed Funds history (243,913 rows, 468 contracts, 1990-2028)
│   ├── eurodollar_futures_history.csv         # COMPLETE Eurodollar history (269,536 rows, 134 contracts, 1990-2023)
│   ├── sofr_futures_history.csv               # COMPLETE 3-Month SOFR history (50,509 rows, 43 contracts, 2018-2028)
│   ├── wirp_historical_snapshots.csv          # Historical Bloomberg WIRP snapshots across 6 Fed cycles (2015 to 2026)
│   ├── wirp_snapshots_2026.csv                # Current Bloomberg WIRP snapshots for the upcoming 18 FOMC meetings
│   ├── macro_surprises_clean.csv              # Raw Bloomberg macro export (columns shifted, see notebook 05)
│   ├── macro_event_study/                     # Mission 5 outputs: corrected macro surprises, event panel, regressions
│   ├── treasury_2y_yield.csv                  # Daily constant-maturity 2-Year US Treasury yield (9,602 days, 1990-2026)
│   ├── reference_rates_bloomberg.csv          # Daily Bloomberg reference rates: EFFR and SOFR (9,364 days, 1990-2026)
│   ├── fed_rates.csv                          # FRED policy corridor bounds (Upper, Lower, Midpoint) and EFFR (2015-2026)
│   ├── fomc_calendar.csv                      # Scheduled FOMC meeting dates (2024-2026) with SEP / dot plot flags
│   ├── fomc_events_history_1990_2026.csv      # Complete log of historical FOMC announcement dates & timestamps
│   └── README.md                              # Detailed dataset documentation & cleaning specifications
├── notebooks/
│   ├── 01_fedwatch_model_erian.ipynb          # Mission 1 notebook: CME FedWatch replication (Erian)
│   ├── 02_wirp_comparison_ouiam.ipynb         # Mission 2 notebook: Bloomberg WIRP vs FedWatch (Ouiam)
│   ├── 03_historical_reconstruction_justine.ipynb # Mission 3 notebook: Historical expectations reconstruction (Justine)
│   ├── 04_sofr_fomc_analysis_assunta.ipynb    # Mission 4 notebook: SOFR term structure & FOMC jumps (Assunta)
│   └── 05_macro_repricing_yasmine.ipynb       # Mission 5 notebook: Macro surprises & Healy-Jia regressions (Yasmine)
├── src/
│   ├── __init__.py
│   ├── fed_data.py                            # Automated FRED data downloader & corridor analyzer
│   ├── futures_math.py                        # Pre-/post-meeting decomposition & Kuttner surprise formulas
│   └── probabilities.py                       # Analytical 2-state, 3-state, and tree probability models
├── requirements.txt                           # Project Python dependencies
└── README.md
```

---

## Complete Historical Data Dictionary

To ensure seamless reproduction of historical policy expectations, event-study regressions, and term-structure analysis without memory overhead, **all raw Bloomberg extractions have been converted into clean, optimized CSV files**:

| Dataset Name | Period Covered | Total Rows | Underlying Contracts / Scope | Primary Users |
| :--- | :---: | :---: | :--- | :--- |
| **`fed_funds_futures_history.csv`** | **1990 – 2028** | **243,913** | **468 monthly contracts** (`FFF90` to `FFZ28`). Daily settlement prices, closing prices, volume, and open interest. | **Justine (M3), Erian (M1)** |
| **`eurodollar_futures_history.csv`** | **1990 – 2023** | **269,536** | **134 quarterly contracts** (`EDH90` to `EDM23`) covering the pre-SOFR sample up to LIBOR cessation. | **Assunta (M4)** |
| **`sofr_futures_history.csv`** | **2018 – 2028** | **50,509** | **43 quarterly contracts** (`SFRM18` to `SFRZ28`) since inception on the CME. | **Assunta (M4)** |
| **`wirp_historical_snapshots.csv`** | **2015 – 2026** | **78 meetings** | Snapshots of Bloomberg `WIRP <GO>` across 6 major Fed regime pivots (2015 liftoff, 2018 tightening, 2020 COVID, 2021 pre-hike, 2024 cuts, 2026 current regime). | **Ouiam (M2), Erian (M1)** |
| **`wirp_snapshots_2026.csv`** | **2026 – 2028** | **18 meetings** | Current Bloomberg WIRP snapshot for upcoming FOMC meetings comparing **Futures Model** (`US_FUT`) vs **OIS Model** (`US_OIS`). | **Ouiam (M2), Erian (M1)** |
| **`macro_surprises_clean.csv`** | **1997 – 2026** | **3,241 rows** | Raw Bloomberg export for CPI, Core CPI, NFP and Unemployment. Columns are shifted (release date in `actual`, published value in `survey_median`, consensus median in `survey_high`) and `surprise` is empty. Use `macro_event_study/macro_surprises_fixed.csv` instead. | **Yasmine (M5)** |
| **`macro_event_study/macro_surprises_fixed.csv`** | **1997 – 2026** | **1,424 releases** | Corrected macro panel, one row per release: `release_date`, `indicator`, `ref_period`, `actual`, `survey_median`, `survey_average`, `survey_high`, `surprise` ($A - E$). Built by notebook 05. | **Yasmine (M5)** |
| **`treasury_2y_yield.csv`** | **1990 – 2026** | **9,602 days** | Daily constant-maturity 2-year US Treasury yield (`yield_2y_pct`). | **Yasmine (M5)** |
| **`reference_rates_bloomberg.csv`** | **1990 – 2026** | **9,364 days** | Daily official Bloomberg fixings for Effective Federal Funds Rate (`effr`) and Secured Overnight Financing Rate (`sofr`). | **ALL (Team)** |
| **`fed_rates.csv`** | **2015 – 2026** | **4,331 days** | FRED official policy corridor: Upper Limit, Lower Limit, Target Midpoint, and daily EFFR-Midpoint spread. | **ALL (Team)** |
| **`fomc_events_history_1990_2026.csv`** | **1990 – 2026** | **388 events** | Historical catalog of all scheduled and unscheduled FOMC rate announcements and timestamps. | **Assunta (M4), Yasmine (M5)** |
| **`fomc_calendar.csv`** | **2024 – 2026** | **24 meetings** | Official FOMC meeting schedule with flags for Summary of Economic Projections / dot plot releases. | **ALL (Team)** |

---

## Data Cleaning Pipeline & Quality Assurance

1. **Header & Metadata Stripping:** Bloomberg terminal exports embed 5 to 6 metadata rows (*Security, Start Date, End Date, Period, Spill Area*). All files have been programmatically parsed to expose clean, typed headers at line 1.
2. **Zero Mixing of Contracts:** Every single contract sheet extracted from Bloomberg (`FFF90`, `EDH94`, `SFRZ26`, etc.) is strictly tagged with its native contract identifier in the `contract` column. Zero contracts were merged or overwritten.
3. **Date Harmonization:** All observation dates are strictly parsed into ISO 8601 format (`YYYY-MM-DD`).
4. **Unit Standards:**
   - **Rate Levels:** Recorded in percentage points (e.g., `4.00` means 4.00%).
   - **Rate Changes & Spreads:** Recorded in basis points (e.g., `25.0` means 25 bp).
   - **Probabilities:** Recorded as decimal values between 0.0 and 1.0 (e.g., `0.65` means 65%).
5. **Fast & Reliable Loading:** Clean CSV files load in under 0.05 seconds with `pandas.read_csv()`, avoiding `openpyxl` dependencies and memory spikes in Jupyter.

---

## Quickstart Guide

### 1. Clone or Update the Repository
```bash
git clone https://github.com/OuiamBB/PI2-Pricing-the-Fed.git
cd PI2-Pricing-the-Fed
# If already cloned, pull latest data:
git pull origin main
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Loading Clean Data in Python
```python
import pandas as pd

# Load 38 years of Fed Funds futures history (1990-2028):
df_ff = pd.read_csv('../data/fed_funds_futures_history.csv')

# Load historical WIRP snapshots:
df_wirp_hist = pd.read_csv('../data/wirp_historical_snapshots.csv')

# Load corrected macroeconomic surprises (1997-2026):
df_macro = pd.read_csv('../data/macro_event_study/macro_surprises_fixed.csv')

# Load current 2026 WIRP meeting expectations:
df_wirp_2026 = pd.read_csv('../data/wirp_snapshots_2026.csv')
```

### 4. Running Member Notebooks
Each team member works inside their dedicated notebook located in `notebooks/`:
- `01_fedwatch_model_erian.ipynb` — Erian
- `02_wirp_comparison_ouiam.ipynb` — Ouiam
- `03_historical_reconstruction_justine.ipynb` — Justine
- `04_sofr_fomc_analysis_assunta.ipynb` — Assunta
- `05_macro_repricing_yasmine.ipynb` — Yasmine
