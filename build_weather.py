"""
Real weather for the demo: KROA (Roanoke-Blacksburg Regional Airport) hourly
observations from the Iowa Environmental Mesonet ASOS archive, rolled up to one
row per day for Sep 1, 2025 - Aug 31, 2026.

Writes kroa_hourly_raw.csv (as downloaded) and kroa_daily.csv.
Service hours = 11 am - 10 pm local.
snow_level: 2 = moderate/heavy snow or any ice during service hours (2+ obs)
            1 = 3+ hourly obs with any snow/ice code that day
            0 = otherwise (flurries alone don't count)
"""
import urllib.request, numpy as np, pandas as pd

URL = ("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=ROA"
       "&data=tmpf&data=p01i&data=wxcodes&data=sknt"
       "&year1=2025&month1=8&day1=31&year2=2026&month2=9&day2=1"
       "&tz=America%2FNew_York&format=onlycomma&latlon=no&elev=no"
       "&missing=M&trace=T&direct=no&report_type=3")
START, END = "2025-09-01", "2026-08-31"

urllib.request.urlretrieve(URL, "data/kroa_hourly_raw.csv")
df = pd.read_csv("data/kroa_hourly_raw.csv")
df["valid"] = pd.to_datetime(df["valid"])
df["tmpf"] = pd.to_numeric(df["tmpf"], errors="coerce")
df["p01i"] = df["p01i"].replace({"T": "0.001", "M": np.nan}).astype(float)   # trace -> 0.001 in
df["date"] = df["valid"].dt.strftime("%Y-%m-%d")
df["hour"] = df["valid"].dt.hour
wx = df["wxcodes"].fillna("")
df["any_snow"] = wx.str.contains(r"SN|IP|PL|FZRA|FZDZ")
df["real_snow"] = wx.str.contains(r"(?<![-])SN|\+SN|IP|PL|FZRA")
svc = df[(df.hour >= 11) & (df.hour <= 22)]

g, gs = df.groupby("date"), svc.groupby("date")
daily = pd.DataFrame({
    "high_f": g.tmpf.max().round(0),
    "low_f": g.tmpf.min().round(0),
    "svc_mean_f": gs.tmpf.mean().round(1),
    "precip_in": g.p01i.sum().round(2),
    "svc_precip_in": gs.p01i.sum().round(2),
    "svc_rain_hours": svc[svc.p01i >= 0.01].groupby("date").size(),
    "snow_obs": g.any_snow.sum(),
    "svc_real_snow_obs": gs.real_snow.sum(),
    "obs": g.size(),
}).fillna({"svc_rain_hours": 0, "svc_real_snow_obs": 0})
daily = daily.loc[START:END]
daily["snow_level"] = np.where(daily.svc_real_snow_obs >= 2, 2, np.where(daily.snow_obs >= 3, 1, 0))

# Frozen roads: up to 5 days after a level-2 snow/ice day, for as long as every
# day's high stays at or below 36 F (snow and ice stay on the streets).
frozen, streak = [], None
for _, r in daily.iterrows():
    if r.snow_level == 2:
        streak = 0; frozen.append(False); continue
    if streak is not None and streak < 5 and r.high_f <= 36:
        streak += 1; frozen.append(True)
    else:
        streak = None; frozen.append(False)
daily["frozen_roads"] = frozen
daily.index.name = "date"
daily.drop(columns=["snow_obs", "svc_real_snow_obs"]).to_csv("data/kroa_daily.csv")

print(f"{len(daily)} days | min obs/day {int(daily.obs.min())} | "
      f"rain >=0.10 in during service: {(daily.svc_precip_in >= 0.10).sum()} | "
      f"snow level 2: {list(daily.index[daily.snow_level == 2])} | level 1: {(daily.snow_level == 1).sum()} | "
      f"frozen roads: {list(daily.index[daily.frozen_roads])}")
