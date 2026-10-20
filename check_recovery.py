"""
Sanity check: does a regression on the simulated year recover the assumptions
that went into it? Log daily sales on weekday, month, weather and event
indicators, open days only. Prints each factor's estimate with a 95% range.
"""
import numpy as np, pandas as pd

df = pd.read_csv("data/sales_daily.csv", parse_dates=["date"])
op = df[~df.closed].copy()
op["month"] = op.date.dt.month
eff = op.effects.fillna("")

X = pd.get_dummies(op.weekday).drop(columns="Mon").astype(float)
X = X.join(pd.get_dummies(op.month, prefix="m").drop(columns="m_4").astype(float))
storm = eff.str.contains("storm_day")
X["rain"] = (op.rain & ~storm).astype(float)
X["patio_weather"] = ((op.svc_precip_in < 0.01) & (op.snow_level == 0) & op.svc_mean_f.between(65, 85) & ~storm).astype(float)
X["snow_level_2"] = ((op.snow_level == 2) & ~storm).astype(float)
X["snow_level_1"] = ((op.snow_level == 1) & ~storm).astype(float)
X["frozen_roads"] = (op.frozen_roads & ~storm).astype(float)
EVENTS = ["festival_big", "st_pats_parade", "dickens", "restaurant_week", "berglund_coliseum", "vt_watch",
          "vt_home_day", "mothers_day", "valentines", "nye", "nyd", "xmas_eve", "super_bowl", "july4",
          "storm_day1", "storm_day4", "storm_day5", "storm_day6", "storm_day7", "storm_day8"]
for e in EVENTS:
    X[e] = eff.str.contains(e).astype(float)
X.insert(0, "const", 1.0)

y = np.log(op.total.values)
A = X.values
b = np.linalg.lstsq(A, y, rcond=None)[0]
resid = y - A @ b
s2 = resid @ resid / (len(y) - A.shape[1])
se = np.sqrt(np.diag(s2 * np.linalg.inv(A.T @ A)))

print(f"{len(op)} open days | residual noise (CV) {np.sqrt(s2):.3f}\n")
print(f"{'factor':18s} {'n':>3s} {'estimate':>9s}   95% range")
for i, c in enumerate(X.columns):
    if c == "const" or c in set(op.weekday) or c.startswith("m_"):
        continue
    lo, hi = np.exp(b[i] - 1.96 * se[i]), np.exp(b[i] + 1.96 * se[i])
    print(f"{c:18s} {int(X[c].sum()):3d} {np.exp(b[i]):9.2f}   {lo:.2f} – {hi:.2f}")
