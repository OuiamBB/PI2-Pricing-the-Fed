"""
src/probabilities.py
Computes meeting-implied probabilities from expected rates (CME FedWatch style).
"""

from typing import Dict

def compute_binary_probabilities(
    r_after: float,
    r_base: float,
    step_bp: float = 25.0
) -> Dict[str, float]:
    """
    Computes probabilities between two adjacent outcomes:
    E.g. No change vs. 25 bp hike (if r_after >= r_base)
    or No change vs. 25 bp cut (if r_after < r_base)
    
    Parameters:
    - r_after: Expected post-meeting EFFR (percent)
    - r_base: Expected pre-meeting EFFR / Status quo rate (percent)
    - step_bp: Policy move increment (typically 25.0 basis points)
    
    Returns:
    - Dict with probabilities for the two states (between 0.0 and 1.0)
    """
    diff_bp = (r_after - r_base) * 100.0
    
    if diff_bp >= 0:
        p_hike = min(max(diff_bp / step_bp, 0.0), 1.0)
        return {
            "no_change": round(1.0 - p_hike, 4),
            f"hike_{int(step_bp)}bp": round(p_hike, 4)
        }
    else:
        p_cut = min(max(-diff_bp / step_bp, 0.0), 1.0)
        return {
            "no_change": round(1.0 - p_cut, 4),
            f"cut_{int(step_bp)}bp": round(p_cut, 4)
        }

def compute_three_state_probabilities(
    r_after: float,
    r_base: float,
    step_bp: float = 25.0
) -> Dict[str, float]:
    """
    Computes probabilities across 3 states: [Cut 25 bp, No change, Hike 25 bp].
    """
    diff_bp = (r_after - r_base) * 100.0
    
    if diff_bp > 0:
        p_hike = min(diff_bp / step_bp, 1.0)
        return {
            f"cut_{int(step_bp)}bp": 0.0,
            "no_change": round(1.0 - p_hike, 4),
            f"hike_{int(step_bp)}bp": round(p_hike, 4)
        }
    elif diff_bp < 0:
        p_cut = min(-diff_bp / step_bp, 1.0)
        return {
            f"cut_{int(step_bp)}bp": round(p_cut, 4),
            "no_change": round(1.0 - p_cut, 4),
            f"hike_{int(step_bp)}bp": 0.0
        }
    else:
        return {
            f"cut_{int(step_bp)}bp": 0.0,
            "no_change": 1.0,
            f"hike_{int(step_bp)}bp": 0.0
        }
