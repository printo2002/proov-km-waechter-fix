# test_fleet_report.py
from fleet_report import fleet_summary

SAMPLE = [
    {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
    {"id": "VOS-2210", "odometer": 48400, "last_service_km": 45000},
]


def test_summary_counts_due_cars():
    # Only VOS-4471 is nearly worn, so exactly one car is due.
    assert fleet_summary(SAMPLE)["due"] == 1


def test_no_reading_does_not_crash_report():
    # A car with no last_service_km must not raise a KeyError and must not be
    # counted as due (0 km since service = 0% wear).
    fleet = [
        {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
        {"id": "VOS-7788", "odometer": 92000},   # no last_service_km
    ]
    result = fleet_summary(fleet)
    assert "average_wear" in result          # did not crash
    assert result["due"] == 1               # only VOS-4471 is flagged, not VOS-7788
