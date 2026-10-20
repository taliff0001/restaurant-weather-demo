# What do weather and local events do to a restaurant's sales?

A one-question analysis for a fictional downtown Roanoke, Virginia restaurant (full service, a bar with a few TVs, a patio), September 1, 2025 – August 31, 2026.

**The sales are simulated. The weather and event data are real.** The simulated year is built from published effect sizes, so the method can be shown end to end before a real restaurant's point-of-sale export goes through the same steps.

Live page: *coming soon* at tommyaliff.com/restaurant-demo/

## What's real and what isn't

| Input | Source | Real? |
|---|---|---|
| Weather | Hourly observations at Roanoke-Blacksburg Regional Airport (KROA), from the [Iowa Environmental Mesonet ASOS archive](https://mesonet.agron.iastate.edu/request/download.phtml) | Yes |
| Events | Hand-built calendar: Virginia Tech football, Downtown Roanoke festivals, Berglund Center coliseum shows, holidays. One source link per row in `data/events.csv` | Yes |
| Sales | `simulate_sales.py`, using the assumptions below | **No** |

Because the sales are simulated, every effect the analysis finds is an effect that was put in, plus random noise. The point of the demo is the method and the reads, not the numbers.

## How to run it

```bash
pip install -r requirements.txt
python build_weather.py     # downloads KROA hourly data -> data/kroa_daily.csv
python build_events.py      # writes data/events.csv
python simulate_sales.py    # writes data/sales_daily.csv
```

The simulator uses a fixed random seed, so it reproduces the same year every time.

## Weather definitions

- **Service hours:** 11 am – 10 pm local time.
- **Rain day:** 0.10 in or more during service hours (40 days in the window).
- **Patio weather:** dry during service hours and a service-hour mean temperature of 65–85 °F.
- **Snow/ice:** level 2 = moderate or heavy snow, or any ice, during service hours (2 days); level 1 = three or more hourly reports of any snow or ice that day (6 days). Flurries alone don't count.

## Assumptions in the simulated sales

Every value is tagged with its basis: **sourced** (published data), **inferred** (derived from published data), or **guess** (no published figure; set at the conservative end of a reasoned range). Sources and reliability notes are in [`research/effect-sizes.md`](research/effect-sizes.md).

| Factor | Value | Basis |
|---|---|---|
| Annual sales | ~$1.3M | guess (the fictional restaurant's size) |
| Day of week, share of weekly sales | Mon 9 · Tue 10 · Wed 11 · Thu 13 · Fri 19 · Sat 22 · Sun 16 % | inferred (Toast, Square) |
| Month (per-day index) | Jan 0.88 · Feb 0.97 · Mar 1.02 · Apr 1.00 · May 1.04 · Jun 1.05 · Jul 1.01 · Aug 1.03 · Sep 0.98 · Oct 0.98 · Nov 0.98 · Dec 1.03 | sourced (U.S. Census monthly retail trade, NAICS 7221/722) |
| Takeout share | 18% of sales | inferred (NRA/Circana off-premises traffic) |
| Rain during service | dine-in −7%, takeout +10% | inferred (Foursquare/AccuWeather foot traffic) / guess |
| Patio | +6% of the day's sales on patio-weather days | guess |
| Snow/ice | level 2 −30%, level 1 −10% | guess |
| Mother's Day | 1.55 × a normal Sunday | sourced (Toast) |
| Valentine's Day (a Saturday in 2026) | 1.30 × a normal Saturday | inferred (Toast) |
| New Year's Eve / New Year's Day / Christmas Eve | 1.20 / 0.75 / 0.70 × the December average day | sourced (Toast) |
| Super Bowl Sunday | dine-in 0.80, takeout unchanged | sourced (Toast) |
| July 4 | 0.80 | sourced (Toast) |
| Thanksgiving, Christmas Day | closed | assumption |
| Large downtown festival | +15% | guess |
| St. Patrick's Day parade | +20% | guess |
| Dickens of a Christmas (Fridays) | +10% | guess |
| Restaurant Week | traffic +15%, average check −10% | guess (2026 dates estimated) |
| Berglund Center coliseum show | +8% | guess |
| Virginia Tech game watched on TV (away games, home night games) | +8% | guess |
| Virginia Tech home day game (fans leave town) | −5% | guess |
| Day-to-day noise | 10%, log-normal | guess |

No published estimate exists for how Virginia Tech games affect Roanoke restaurants, in either direction.

## Check: does the output match the input?

A regression of log daily sales on weekday, month, weather and event indicators, over the 363 open days, recovers every assumption inside its 95% range, with residual noise of 9.8%.

It also shows a real limit: with one season of data, the Virginia Tech effects (+8% and −5%) can't be told apart from zero. One year of daily sales answers the weather and festival questions; game days need two or three seasons. Single-day holidays are one data point each.

## Files

- `build_weather.py`, `build_events.py`, `simulate_sales.py`: the pipeline
- `data/kroa_daily.csv`, `data/events.csv`, `data/sales_daily.csv`: outputs (the raw hourly download is not committed; `build_weather.py` re-creates it)
- `research/effect-sizes.md`: the research behind the assumptions, with sources

## Contact

Tommy Aliff · [tommyaliff.com](https://tommyaliff.com)
