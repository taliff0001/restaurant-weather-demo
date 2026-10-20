"""
Hand-built event calendar for Sep 1, 2025 - Aug 31, 2026. One source URL per row.
'effect' is a key into simulate_sales.P["effects"]; 'none' = listed but not modeled.
Research and reliability notes: effect-sizes.md
"""
import pandas as pd

VT = "https://en.wikipedia.org/wiki/2025_Virginia_Tech_Hokies_football_team"
TOAST = {
    "md": "https://pos.toasttab.com/blog/data/mothers-day-restaurant-trends-data",
    "vd": "https://pos.toasttab.com/blog/on-the-line/valentines-day-food-insights",
    "ny": "https://pos.toasttab.com/blog/on-the-line/new-years-2020-restaurant-trends",
    "xm": "https://pos.toasttab.com/blog/on-the-line/2019-christmas-and-christmas-eve-restaurant-trends",
    "sb": "https://pos.toasttab.com/blog/on-the-line/super-bowl-food-stats",
    "j4": "https://pos.toasttab.com/blog/data/fourth-of-july-restaurant-insights",
}
R26 = "https://theroanoker.com/magazine/features/the-roanoker-magazine-festivals-guide/"
RMJ = "https://theroanoker.com/events-calendar-may-june-2026/"
CA = "https://www.concertarchives.org/venues/berglund-center"
DRI = "https://www.DowntownRoanoke.org/events/signature-events"

rows = []
def add(d, name, cat, eff, src, note=""):
    rows.append((d, name, cat, eff, src, note))

# Virginia Tech football, all games in the window. Home games before 6 pm = fans leave town.
for d, opp, kick, home in [
    ("2025-09-06", "Vanderbilt", "7:30 pm", 1), ("2025-09-13", "Old Dominion", "7:00 pm", 1),
    ("2025-09-20", "Wofford", "12:00 pm", 1), ("2025-09-27", "at NC State", "7:00 pm", 0),
    ("2025-10-04", "Wake Forest", "1:00 pm", 1), ("2025-10-11", "at Georgia Tech", "3:30 pm", 0),
    ("2025-10-24", "California", "7:30 pm", 1), ("2025-11-01", "Louisville", "3:00 pm", 1),
    ("2025-11-15", "at Florida State", "7:30 pm", 0), ("2025-11-22", "Miami", "12:00 pm", 1),
    ("2025-11-29", "at Virginia", "7:00 pm", 0)]:
    hour = int(kick.split(":")[0]) % 12 + 12      # all kickoffs are pm
    eff = "vt_home_day" if (home and hour < 18) else "vt_watch"
    add(d, f"VT {'vs ' if home else ''}{opp} ({kick})", "vt_football", eff, VT, "home" if home else "away")

# Holidays with published multipliers (Toast). Others are not modeled.
add("2025-11-27", "Thanksgiving", "holiday", "closed", "", "assumed closed (no published multiplier)")
add("2025-12-24", "Christmas Eve", "holiday", "xmas_eve", TOAST["xm"])
add("2025-12-25", "Christmas Day", "holiday", "closed", TOAST["xm"], "81% of Toast restaurants closed")
add("2025-12-31", "New Year's Eve", "holiday", "nye", TOAST["ny"])
add("2026-01-01", "New Year's Day", "holiday", "nyd", TOAST["ny"])
add("2026-02-08", "Super Bowl LX", "holiday", "super_bowl", TOAST["sb"])
add("2026-02-14", "Valentine's Day (Sat)", "holiday", "valentines", TOAST["vd"], "multiplier inferred for a Saturday")
add("2026-05-10", "Mother's Day", "holiday", "mothers_day", TOAST["md"])
add("2026-07-04", "Independence Day", "holiday", "july4", TOAST["j4"])

# Downtown festivals
for d in ["2025-10-17", "2025-10-18", "2025-10-19"]:
    add(d, "GO Outside Festival", "festival", "festival_big", "https://roanokegofest.com/go-outside-2025-recap/",
        "Elmwood Park + Explore Park; ~40k attendees (organizer)")
for d, n in [("2025-12-05", "tree lighting"), ("2025-12-12", "parade"), ("2025-12-19", "pet costume contest")]:
    add(d, f"Dickens of a Christmas ({n})", "festival", "dickens",
        "https://nrv.mobile.macaronikid.com/articles/69310e50e5c2f52a7c233f9e/dickens-of-a-christmas-2025-a-complete-guide-for-families")
for d in pd.date_range("2026-01-16", "2026-01-23"):
    add(d.strftime("%Y-%m-%d"), "Downtown Restaurant Week (dates estimated)", "festival", "restaurant_week",
        "https://www.downtownroanoke.org/do/restaurant-week-2025",
        "2026 dates not published; 2025 pattern, cut off before the Jan 24 storm")

# January 24-25, 2026 winter storm (snow, then sleet; state of emergency declared Jan 23).
# Hand-set recovery curve; overrides the generic snow/frozen-roads rules for these days.
STORM = [
    ("2026-01-24", "storm_day1", "storm starts", "https://www.wdbj7.com/2026/01/23/city-roanoke-declares-state-emergency-winter-storm/"),
    ("2026-01-25", "closed", "closed (streets impassable)", "https://www.wsls.com/news/local/2026/01/27/snow-covered-streets-leave-downtown-roanoke-businesses-empty/"),
    ("2026-01-26", "closed", "closed (streets impassable)", "https://www.wsls.com/news/local/2026/01/27/snow-covered-streets-leave-downtown-roanoke-businesses-empty/"),
    ("2026-01-27", "storm_day4", "downtown nearly empty (~15 diners vs ~100 at one brunch spot)", "https://www.wsls.com/news/local/2026/01/27/snow-covered-streets-leave-downtown-roanoke-businesses-empty/"),
    ("2026-01-28", "storm_day5", "roads still iced", "https://www.wdbj7.com/2026/01/28/days-after-winter-storm-many-roanoke-residents-still-trapped-by-ice/"),
    ("2026-01-29", "storm_day6", "roads still iced", "https://www.wdbj7.com/2026/01/29/some-roanoke-neighborhoods-still-dealing-with-icy-unplowed-roads-days-after-winter-weather/"),
    ("2026-01-30", "storm_day7", "recovering", "https://www.wdbj7.com/2026/01/29/some-roanoke-neighborhoods-still-dealing-with-icy-unplowed-roads-days-after-winter-weather/"),
    ("2026-01-31", "storm_day8", "another round of snow", "https://www.wdbj7.com/2026/01/31/another-round-snow-keeps-roanoke-crews-24-hour-response-mode/"),
]
for d, eff, note, src in STORM:
    add(d, "January winter storm", "weather_event", eff, src, note)
add("2026-03-14", "St. Patrick's Day Parade & Shamrock Festival", "festival", "st_pats_parade",
    "https://www.downtownroanoke.org/news-item/freedom-first-st-patrick-s-day-parade-and-shamrock-festival-2026")
for d in ["2026-04-16", "2026-04-17", "2026-04-18", "2026-04-19"]:
    add(d, "Down by Downtown Music Festival", "festival", "festival_big", R26)
add("2026-05-16", "Local Colors Festival", "festival", "festival_big", RMJ)
for d in ["2026-05-22", "2026-05-23", "2026-05-24"]:
    add(d, "Festival in the Park", "festival", "festival_big", RMJ)

# Smaller events: listed, no effect modeled
for d, n, s in [("2025-10-26", "Downtown Candy Crawl", DRI), ("2026-03-06", "Roanoke Arts Pop!", R26),
                ("2026-04-18", "Blue Ridge Marathon", R26), ("2026-04-26", "Roanoke Pride Festival", R26),
                ("2026-05-01", "Strawberry Festival", RMJ), ("2026-05-02", "Strawberry Festival", RMJ),
                ("2026-05-30", "Sidewalk Art Show", RMJ), ("2026-05-31", "Sidewalk Art Show", RMJ),
                ("2026-08-29", "Roanoke Taco Fest", R26)]:
    add(d, n, "festival_small", "none", s, "listed, no effect modeled")

# Berglund Center coliseum shows (KALEO left out: sources disagree on the date)
for d, n in [("2025-09-11", "Alabama w/ Exile"), ("2025-11-06", "Disney On Ice"), ("2025-11-07", "Disney On Ice"),
             ("2025-11-08", "Disney On Ice"), ("2025-11-09", "Disney On Ice"), ("2026-06-04", "Journey"),
             ("2026-07-14", "Billy Strings"), ("2026-08-08", "Leanne Morgan")]:
    add(d, f"Berglund Coliseum: {n}", "berglund", "berglund_coliseum", CA)

ev = pd.DataFrame(rows, columns=["date", "name", "category", "effect", "source", "notes"]).sort_values(["date", "name"])
ev.to_csv("data/events.csv", index=False)
print(f"{len(ev)} rows:", ev.groupby("effect").size().to_dict())
