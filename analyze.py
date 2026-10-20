"""
Turn the daily sales file into the numbers the page shows. Writes data/page.json.

Method: every open day is compared with a "typical day" = the median of plain
days (no event, no rain, no snow, no frozen roads) with the same weekday and
month. Rain, event and weather effects are reported as the median ratio to
that typical day, with the number of days behind each figure. This is the
like-for-like comparison an owner would trust: a rainy Friday in June is
compared with dry Fridays in June, not with the whole year.
"""
import json, numpy as np, pandas as pd

df = pd.read_csv("data/sales_daily.csv", parse_dates=["date"])
ev = pd.read_csv("data/events.csv", parse_dates=["date"])
op = df[~df.closed].copy()
op["month"] = op.date.dt.month
op["effects"] = op.effects.fillna("")
op["events"] = op.events.fillna("")
op["storm"] = op.effects.str.contains("storm_day")
op["plain"] = (op.effects == "") & ~op.rain & (op.snow_level == 0) & ~op.frozen_roads

# ---- typical day per weekday x month (fallback: neighbouring months) -------
plain = op[op.plain]
def typical(wd, m):
    ref = plain[(plain.weekday == wd) & (plain.month == m)]
    if len(ref) < 3:
        near = [m, m - 1, m + 1]
        near = [((x - 1) % 12) + 1 for x in near]
        ref = plain[(plain.weekday == wd) & plain.month.isin(near)]
    return ref.total.median(), len(ref)

op["typical"], op["typical_n"] = zip(*[typical(w, m) for w, m in zip(op.weekday, op.month)])
op["ratio"] = op.total / op.typical
op["delta"] = op.total - op.typical

def summarize(g, label):
    return dict(label=label, n=int(len(g)), median_ratio=round(float(g.ratio.median()), 3),
                median_delta=round(float(g.delta.median()), 0))

out = {"window": {"start": str(df.date.min().date()), "end": str(df.date.max().date()),
                  "days": int(len(df)), "open_days": int(len(op)), "closed_days": int(df.closed.sum())},
       "annual_total": round(float(df.total.sum()), 0)}

# ---- rain ------------------------------------------------------------------
fs = op[op.weekday.isin(["Fri", "Sat"]) & ~op.storm & (op.snow_level == 0) & (op.effects == "")]
warm = fs[fs.svc_mean_f >= 65]; cold = fs[fs.svc_mean_f < 65]
out["rain"] = {
    "fri_sat_all": {"rainy": summarize(fs[fs.rain], "rainy Fri/Sat"), "dry": summarize(fs[~fs.rain], "dry Fri/Sat")},
    "fri_sat_warm": {"rainy": summarize(warm[warm.rain], "rainy warm Fri/Sat"), "dry": summarize(warm[~warm.rain], "dry warm Fri/Sat")},
    "fri_sat_cold": {"rainy": summarize(cold[cold.rain], "rainy cold Fri/Sat"), "dry": summarize(cold[~cold.rain], "dry cold Fri/Sat")},
    "all_days": {"rainy": summarize(op[op.rain & ~op.storm & (op.effects == "")], "rainy days"),
                 "n_rainy_days_year": int(op.rain.sum())},
    "takeout_on_rain": {
        "rainy_median": round(float(op[op.rain & ~op.storm & (op.effects == "")].takeout.median()), 0),
        "dry_median": round(float(op[op.plain].takeout.median()), 0),
    },
}
# per-channel on rainy vs typical (warm Fri/Sat, where the patio matters)
ch = {}
for c in ["dine_in", "patio", "takeout"]:
    ch[c] = {"rainy": round(float(warm[warm.rain][c].median()), 0), "dry": round(float(warm[~warm.rain][c].median()), 0)}
out["rain"]["channels_warm_fri_sat"] = ch

# ---- events ----------------------------------------------------------------
EVENT_TYPES = [
    ("festival_big", "Big downtown festival"), ("st_pats_parade", "St. Patrick's Day parade"),
    ("dickens", "Dickens of a Christmas"), ("restaurant_week", "Restaurant Week"),
    ("berglund_coliseum", "Berglund coliseum show"), ("vt_watch", "Tech game on TV (away or night)"),
    ("vt_home_day", "Tech home game, daytime"), ("mothers_day", "Mother's Day"), ("valentines", "Valentine's Day"),
    ("nye", "New Year's Eve"), ("super_bowl", "Super Bowl Sunday"), ("july4", "July 4"),
    ("xmas_eve", "Christmas Eve"), ("nyd", "New Year's Day"),
]
events = []
for key, label in EVENT_TYPES:
    m = op.effects.str.contains(key) & ~op.rain & (op.snow_level == 0) & ~op.frozen_roads
    g = op[m]
    if len(g) == 0:
        continue
    events.append(dict(key=key, label=label, n=int(len(g)), median_ratio=round(float(g.ratio.median()), 3),
                       median_delta=round(float(g.delta.median()), 0),
                       lo=round(float(g.ratio.min()), 3), hi=round(float(g.ratio.max()), 3)))
out["events"] = events

# ---- the January storm -----------------------------------------------------
storm_days = df[(df.date >= "2026-01-24") & (df.date <= "2026-01-31")].copy()
storm_days["month"] = storm_days.date.dt.month
exp = sum(typical(w, m)[0] for w, m in zip(storm_days.weekday, storm_days.month))
out["storm"] = {"start": "2026-01-24", "end": "2026-01-31", "actual": round(float(storm_days.total.sum()), 0),
                "typical_week": round(float(exp), 0), "lost": round(float(exp - storm_days.total.sum()), 0),
                "days": [dict(date=str(r.date.date()), weekday=r.weekday, total=round(float(r.total), 0),
                              closed=bool(r.closed), note=str(ev[(ev.date == r.date) & (ev.category == "weather_event")].notes.iloc[0])
                              if len(ev[(ev.date == r.date) & (ev.category == "weather_event")]) else "")
                         for _, r in storm_days.iterrows()]}
# other snow days (outside the storm)
snow = op[(op.snow_level > 0) & ~op.storm]
out["snow_other"] = summarize(snow, "snow/ice days outside the storm")

# ---- temperature (dry, event-free days) ------------------------------------
dry = op[op.plain | ((op.effects == "") & ~op.rain & (op.snow_level == 0) & ~op.frozen_roads)]
bins = [(-99, 35), (35, 45), (45, 55), (55, 65), (65, 75), (75, 85), (85, 199)]
temp = []
for lo, hi in bins:
    g = dry[(dry.svc_mean_f >= lo) & (dry.svc_mean_f < hi)]
    if len(g):
        temp.append(dict(lo=lo, hi=hi, n=int(len(g)), median_ratio=round(float(g.ratio.median()), 3),
                         patio_share=round(float(g.patio.sum() / g.total.sum()), 3)))
out["temperature"] = temp
out["patio"] = {"share_of_year": round(float(df.patio.sum() / df.total.sum()), 3),
                "days_with_patio": int((df.patio > 0).sum())}

# ---- weekly Fri/Sat series for chart 1 -------------------------------------
fs_all = df[df.weekday.isin(["Fri", "Sat"])].copy()
out["fri_sat_series"] = [dict(date=str(r.date.date()), weekday=r.weekday, total=round(float(r.total), 0),
                              rain=bool(r.rain), snow=int(r.snow_level), closed=bool(r.closed),
                              storm=bool(isinstance(r.effects, str) and "storm" in r.effects),
                              events=(r.events if isinstance(r.events, str) else ""))
                         for _, r in fs_all.iterrows()]

# ---- best and worst days ---------------------------------------------------
def dayrow(r):
    wx = "snow/ice" if r.snow_level else ("frozen roads" if r.frozen_roads else ("rain" if r.rain else "dry"))
    return dict(date=str(r.date.date()), weekday=r.weekday, total=round(float(r.total), 0),
                typical=round(float(r.typical), 0), ratio=round(float(r.ratio), 2),
                high_f=int(r.high_f), weather=wx, events=r.events)
out["best_days"] = [dayrow(r) for _, r in op.nlargest(10, "ratio").iterrows()]
out["worst_days"] = [dayrow(r) for _, r in op.nsmallest(10, "ratio").iterrows()]
out["biggest_dollar_days"] = [dayrow(r) for _, r in op.nlargest(5, "total").iterrows()]

# ---- monthly totals --------------------------------------------------------
out["monthly"] = [dict(month=str(p), total=round(float(t), 0))
                  for p, t in df.groupby(df.date.dt.to_period("M")).total.sum().items()]

json.dump(out, open("data/page.json", "w"), indent=1)

# ---- console summary -------------------------------------------------------
r = out["rain"]
print(f"Open days {out['window']['open_days']}, rainy {r['all_days']['n_rainy_days_year']}")
print(f"Fri/Sat warm: rainy n={r['fri_sat_warm']['rainy']['n']} {r['fri_sat_warm']['rainy']['median_ratio']:.2f} of typical"
      f" (median {r['fri_sat_warm']['rainy']['median_delta']:+,.0f}); dry n={r['fri_sat_warm']['dry']['n']}")
print(f"Fri/Sat cold: rainy n={r['fri_sat_cold']['rainy']['n']} {r['fri_sat_cold']['rainy']['median_ratio']:.2f}; dry n={r['fri_sat_cold']['dry']['n']}")
print(f"All rainy days: n={r['all_days']['rainy']['n']} {r['all_days']['rainy']['median_ratio']:.2f} ({r['all_days']['rainy']['median_delta']:+,.0f})")
print("Channels, warm Fri/Sat rainy vs dry:", ch)
print(f"Storm week: ${out['storm']['actual']:,.0f} vs typical ${out['storm']['typical_week']:,.0f} -> lost ${out['storm']['lost']:,.0f}")
print("\nEvents (dry days only):")
for e in events:
    print(f"  {e['label']:32s} n={e['n']:2d}  {e['median_ratio']:.2f}  ({e['median_delta']:+,.0f})  range {e['lo']:.2f}-{e['hi']:.2f}")
print("\nTemperature bins (dry, event-free):")
for t in temp:
    print(f"  {t['lo']:>3}-{t['hi']:<3} n={t['n']:3d} ratio {t['median_ratio']:.2f} patio share {t['patio_share']:.0%}")
print("\nWorst 5:"); [print(" ", d) for d in out["worst_days"][:5]]
print("Best 5:"); [print(" ", d) for d in out["best_days"][:5]]
