# Data Guidelines & Shared Conventions

To keep all notebooks interoperable, all team members should follow these rules:

### 1. Formats
- **Dates**: `YYYY-MM-DD` (e.g. `2024-09-18`). If intraday, store UTC with New York time noted.
- **Rates (Levels)**: Percent units (`4.25` means `4.25%`).
- **Rate Changes**: Basis points (`25` means `25 bp`).
- **Probabilities**: Decimal between `0` and `1` (`0.65` means `65%`).

### 2. Standard Column Names
When creating datasets, use these column names where applicable:
```text
observation_date, fomc_meeting_date, contract_id, instrument, source, futures_price, implied_rate_pct, expected_change_bp, scenario_label, probability
```

### 3. File Paths
Always use relative paths from the root of the repository, for example:
```python
import pandas as pd
fomc_df = pd.read_csv('../data/fomc_calendar.csv')  # inside notebooks/
```
