"""
src/futures_math.py
Formulas for converting 30-Day Fed Funds futures prices into meeting-implied rates.
References:
- Kuttner (2001)
- CME Group FedWatch Methodology (2023)
"""

def implied_monthly_rate(futures_price: float) -> float:
    """Return the implied average EFFR for the contract month: r = 100 - P."""
    return 100.0 - futures_price

def decompose_meeting_month(
    futures_price: float,
    meeting_day: int,
    total_days: int,
    r_before: float
) -> float:
    """
    Computes expected EFFR after an FOMC meeting (Equation 3):
    r_after = (N * r_bar - n_before * r_before) / n_after
    
    Parameters:
    - futures_price: Price of the contract of the meeting month
    - meeting_day: Calendar day of the meeting statement release (e.g. 28 for Oct 28)
    - total_days: Number of days in the month (e.g. 31)
    - r_before: Expected EFFR prior to the meeting (in percent)
    
    Returns:
    - Expected post-meeting EFFR (in percent)
    """
    r_bar = implied_monthly_rate(futures_price)
    n_before = meeting_day
    n_after = total_days - n_before
    if n_after <= 0:
        raise ValueError("Meeting day must be strictly less than total days in the month.")
    return (total_days * r_bar - n_before * r_before) / n_after

def kuttner_surprise(
    p_t: float,
    p_t_minus_1: float,
    meeting_day: int,
    total_days: int
) -> float:
    """
    Computes Kuttner (2001) monetary policy surprise in basis points (Equation 7):
    Delta r = (N / (N - d)) * (f_t - f_{t-1})
    where f = 100 - P
    """
    f_t = 100.0 - p_t
    f_prev = 100.0 - p_t_minus_1
    scaling = total_days / (total_days - meeting_day)
    return scaling * (f_t - f_prev) * 100.0  # in basis points
