# fleet_utils.py
# Utility helpers for KM-Waechter. Modernized 2024.
# Dead functions removed: chunk_list, parse_service_date, format_percent, mean.

KM_TO_MILES_FACTOR: float = 0.621371


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles."""
    return km * KM_TO_MILES_FACTOR


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"
