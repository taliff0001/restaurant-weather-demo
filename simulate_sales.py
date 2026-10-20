"""
Simulated daily sales for a fictional downtown Roanoke full-service restaurant
with a bar, a few TVs and a patio. Sep 1, 2025 - Aug 31, 2026.

Inputs (real):  kroa_daily.csv  (KROA airport hourly weather, Iowa Environmental Mesonet)
                events.csv      (hand-built calendar, one source URL per row)
Output:         sales_daily.csv (one row per day; dine-in, patio, takeout)

The sales are simulated. Every effect the page shows is an effect set here,
plus random noise. Values approved 2026-10-20; each is tagged with its basis:
  [S] sourced  [I] inferred from sources  [G] guess (conservative end of a range)
Full sourcing: effect-sizes.md
"""
import numpy as np, pandas as pd

P = {
    "seed": 20250901,
    "annual_sales": 1_300_000,                                   # [G] the fictional restaurant's size

    # Share of weekly sales by weekday.                          [I] Toast, Square
    "weekday": {"Mon": .09, "Tue": .10, "Wed": .11, "Thu": .13, "Fri": .19, "Sat": .22, "Sun": .16},
    # Per-day seasonality index.                                 [S] Census NAICS 7221/722, NSA
    "month": {1: .88, 2: .97, 3: 1.02, 4: 1.00, 5: 1.04, 6: 1.05,
              7: 1.01, 8: 1.03, 9: .98, 10: .98, 11: .98, 12: 1.03},
    # Base channel split (dine-in includes the bar).             [I] NRA/Circana off-premises traffic
    "takeout_share": 0.18,

    # Rain during service hours (11 am-10 pm) of 0.10 in or more. [I] Foursquare -7.4% visits; [G] takeout
    "rain_min_in": 0.10,
    "rain": {"dine_in": 0.93, "takeout": 1.10},
    # Patio: adds 6% of the day's base on dry days with service-hour temp 65-85 F.  [G] middle of 4-8%
    "patio_bonus": 0.06, "patio_temp": (65, 85),
    # Snow/ice (all channels).                                   [G]
    "snow": {2: 0.70, 1: 0.90},

    # Event effects: multiplier on the day's sales, per channel where it matters.
    "effects": {
        # holidays                                               [S] Toast unless noted
        "mothers_day": {"all": 1.55},
        "valentines":  {"all": 1.30},                            # [I] Toast +77% was vs a Wednesday
        "nye":         {"ref": "dec_avg", "all": 1.20},
        "nyd":         {"ref": "dec_avg", "all": 0.75},
        "xmas_eve":    {"ref": "dec_avg", "all": 0.70},
        "super_bowl":  {"dine_in": 0.80, "takeout": 1.00},
        "july4":       {"all": 0.80},
        # downtown events                                        [G] low end of reasoned ranges
        "festival_big":      {"all": 1.15},
        "st_pats_parade":    {"all": 1.20},
        "dickens":           {"all": 1.10},
        "restaurant_week":   {"all": 1.15 * 0.90},               # traffic +15%, check -10%
        "berglund_coliseum": {"all": 1.08},
        # Virginia Tech football                                 [G] bar with TVs
        "vt_watch":    {"all": 1.08},                            # away games, home night games
        "vt_home_day": {"all": 0.95},                            # fans leave town for the game
    },
    # Day-to-day noise, log-normal so it can't go below zero.    [G]
    "noise_cv": 0.10,
}


def load():
    wx = pd.read_csv("data/kroa_daily.csv", parse_dates=["date"]).set_index("date")
    ev = pd.read_csv("data/events.csv", parse_dates=["date"])
    return wx, ev


def expected_day(d, w, todays, p, weekly_base):
    """Expected sales by channel for one day, before noise. Returns (dict, closed)."""
    if "closed" in set(todays.effect):
        return {"dine_in": 0.0, "patio": 0.0, "takeout": 0.0}, True
    wd = d.strftime("%a")
    base = weekly_base * p["weekday"][wd] * p["month"][d.month]
    dec_avg = weekly_base / 7 * p["month"][12]
    exp = {"dine_in": base * (1 - p["takeout_share"]), "takeout": base * p["takeout_share"], "patio": 0.0}

    dry = w.svc_precip_in < 0.01 and w.snow_level == 0
    lo, hi = p["patio_temp"]
    if dry and lo <= w.svc_mean_f <= hi:
        exp["patio"] = base * p["patio_bonus"]
    if w.svc_precip_in >= p["rain_min_in"]:
        exp["dine_in"] *= p["rain"]["dine_in"]
        exp["takeout"] *= p["rain"]["takeout"]
    if w.snow_level:
        for k in exp: exp[k] *= p["snow"][int(w.snow_level)]

    for eff in todays.effect:
        e = p["effects"].get(eff)
        if not e: continue
        if e.get("ref") == "dec_avg":          # Toast reports these vs the December average day
            scale = dec_avg * e["all"] / base
            for k in exp: exp[k] *= scale
            continue
        for k in exp:
            exp[k] *= e.get(k, e.get("all", 1.0))
    return exp, False


def simulate(p=P):
    wx, ev = load()
    rng = np.random.default_rng(p["seed"])
    sigma = np.sqrt(np.log(1 + p["noise_cv"] ** 2))

    # Scale so the expected year equals annual_sales.
    def year_total(weekly_base):
        return sum(sum(expected_day(d, wx.loc[d], ev[ev.date == d], p, weekly_base)[0].values()) for d in wx.index)
    weekly_base = p["annual_sales"] / 52
    weekly_base *= p["annual_sales"] / year_total(weekly_base)

    rows = []
    for d in wx.index:
        w, todays = wx.loc[d], ev[ev.date == d]
        exp, closed = expected_day(d, w, todays, p, weekly_base)
        day_noise = rng.lognormal(-sigma**2 / 2, sigma)   # one draw per day: busy or slow, all channels together
        out = {k: round(v * day_noise, 2) for k, v in exp.items()}
        rows.append(dict(date=d.date(), weekday=d.strftime("%a"), closed=closed, **out,
                         events="; ".join(todays.name), effects=";".join(e for e in todays.effect if e != "none"),
                         high_f=w.high_f, svc_mean_f=w.svc_mean_f, svc_precip_in=w.svc_precip_in,
                         rain=bool(w.svc_precip_in >= p["rain_min_in"]), snow_level=int(w.snow_level)))
    df = pd.DataFrame(rows)
    df["total"] = df[["dine_in", "patio", "takeout"]].sum(axis=1).round(2)
    return df


if __name__ == "__main__":
    df = simulate()
    df.to_csv("data/sales_daily.csv", index=False)
    print(f"{len(df)} days, {int(df.closed.sum())} closed, total ${df.total.sum():,.0f}")
