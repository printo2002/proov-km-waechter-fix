# analyze.py
# Summary: the strongest breakdown predictors are km_since_service and load_factor.
# High km_since_service (approaching or over 15,000) combined with a high load_factor
# (> 0.65) consistently separates cars that later broke down from those that did not.
# Total odometer and age show almost no separation between the two groups.
#
# A simple risk score (0–100) is built from those two columns alone: each column is
# min-max normalised and the score is their weighted average (60% wear, 40% load).
# Cars are printed highest-risk first so the fleet team can act before the 80% rule fires.

import pandas as pd

df = pd.read_csv("fleet_history.csv")

# ── 1. Understand the data ──────────────────────────────────────────────────
print("Shape:", df.shape)
print("\nBreakdown rate:", df["broke_down"].mean().round(3))

# ── 2. Compare group means: broke-down vs survived ──────────────────────────
broke = df[df["broke_down"] == 1]
fine  = df[df["broke_down"] == 0]

numeric_cols = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]

print("\n--- Group means (broke_down=1 vs 0) ---")
comparison = pd.DataFrame({
    "broke_down": broke[numeric_cols].mean().round(1),
    "survived":   fine[numeric_cols].mean().round(1),
})
comparison["diff_%"] = (
    (comparison["broke_down"] - comparison["survived"])
    / comparison["survived"] * 100
).round(1)
print(comparison.to_string())

# --- 3. Correlation with broke_down ---
print("\n--- Pearson correlation with broke_down ---")
correlations = df[numeric_cols + ["broke_down"]].corr()["broke_down"].drop("broke_down").sort_values(
    key=abs, ascending=False
)
print(correlations.round(3).to_string())

# --- 4. Build a risk score ---
# Only km_since_service and load_factor show meaningful separation.
# Min-max normalise each to [0, 1], then combine (60% wear, 40% load).

def minmax(series: pd.Series) -> pd.Series:
    """Normalise a series to the [0, 1] range."""
    lo, hi = series.min(), series.max()
    return (series - lo) / (hi - lo) if hi > lo else pd.Series(0.0, index=series.index)

df["wear_norm"] = minmax(df["km_since_service"])
df["load_norm"] = minmax(df["load_factor"])
df["risk_score"] = ((df["wear_norm"] * 0.60 + df["load_norm"] * 0.40) * 100).round(1)

# --- 5. Print the fleet ranked by risk ---
ranked = df[["car_id", "km_since_service", "load_factor", "risk_score", "broke_down"]].sort_values(
    "risk_score", ascending=False
)

print("\n--- Fleet ranked by breakdown risk (highest first) ---")
print(f"{'car_id':<12} {'km_since_svc':>13} {'load':>6} {'risk':>6} {'broke_down':>11}")
print("-" * 55)
for _, row in ranked.iterrows():
    marker = " * DUE" if row["km_since_service"] >= 15000 * 0.80 else ""
    print(
        f"{row['car_id']:<12} {int(row['km_since_service']):>13,} "
        f"{row['load_factor']:>6.2f} {row['risk_score']:>6.1f} "
        f"{int(row['broke_down']):>11}{marker}"
    )

# --- 6. Quick accuracy sanity check ---
high_risk = df[df["risk_score"] >= 60]
print(f"\nCars with risk >= 60:  {len(high_risk)}")
print(f"  of which broke down: {high_risk['broke_down'].sum()} "
      f"({high_risk['broke_down'].mean():.0%})")
low_risk = df[df["risk_score"] < 60]
print(f"Cars with risk <  60:  {len(low_risk)}")
print(f"  of which broke down: {low_risk['broke_down'].sum()} "
      f"({low_risk['broke_down'].mean():.0%})")
