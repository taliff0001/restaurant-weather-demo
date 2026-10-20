# Effect sizes for a simulated year of daily sales — independent full-service restaurant, downtown Roanoke, VA (~$1.3M/yr)

Demo window: **Sep 1, 2025 – Aug 31, 2026.** Compiled 2026-10-19. Every figure below carries a source URL and a reliability note. Where no published figure exists, this says so and gives a range with reasoning. Nothing here is a precise invented number.

> **Note:** this is the research behind the simulator. The "Recommended simulator parameters" table at the end is the research's starting point; the values actually used are more conservative in places (and differ for Virginia Tech games) and are listed in `simulate_sales.py` and the README.

Reliability scale used: **A** = government statistics or peer-reviewed; **B** = large POS/platform dataset (Toast, Square, Circana) published by the vendor; **C** = trade press, survey, or single-venue study; **D** = no published figure; range is reasoned.

---

## 1. Day-of-week distribution

No vendor publishes a clean "share of weekly sales by weekday" for independent full-service restaurants. What exists:

| Finding | Value | Source | Reliability |
|---|---|---|---|
| Saturday vs. other days, items sold (all Toast restaurants, 2018) | Saturday +41% vs. other days | [Toast 2018 Year in Review](https://pos.toasttab.com/year-in-review) | B |
| Reservations by weekday, full-service, Q3 2023 | Saturday ~+85%, Friday ~+54% vs. weekly average | [Toast Q3 2023 Trends (BusinessWire)](https://www.businesswire.com/news/home/20231207135338/en) | B (reservations, not sales; overstates the weekend skew because walk-ins fill weekdays) |
| Weekend (Sat+Sun all day) share of food-and-drink transactions, 2023 | ~34–35% (up from ~30% in 2019); weekday lunch fell from 21% to 18% | [Square Spring Restaurant Report via Axios](https://www.axios.com/2024/05/14/restaurants-eating-out-rates-weekend-weekday) | B (all Square F&B sellers incl. coffee/QSR, which are weekday-heavy, so a dinner house skews more to the weekend) |
| Saturday 8am–1pm share of weekly spend, 2023 | 10.06% (was 8.54% in 2019) | [Square Q2 2023 via TSG](https://tsgpayments.com/square-q2-restaurant-industry-reportin-post-pandemic-era-restaurantspending-shifts-from-friday-to-saturday/) | B |
| Mon/Tue reservations YoY, Q3 2024 | +11% (Saturday −1%) — weekdays gaining share | [Toast Q3 2024 (BusinessWire)](https://www.businesswire.com/news/home/20241210819521/en/Toast-Data-Reservation-Trends-Shift-to-Slower-Days-and-Early-Dinners) | B |

**Recommended weights (inferred):** Mon 9%, Tue 10%, Wed 11%, Thu 13%, Fri 19%, Sat 22%, Sun 16% (Fri+Sat ≈ 41%, Sat/weekday-avg ≈ 2.0×). This is consistent with Toast's Saturday +41% items and sits below the reservation-only skew. If the restaurant does Sunday brunch, raise Sunday to 17–18% and trim Tue/Wed.

## 2. Monthly seasonality

Hard source: Census Monthly Retail Trade, not seasonally adjusted. Full-service restaurants (NAICS 7221, series MRTSSM7221USN) was discontinued after Jan 2020; NAICS 722 (food services & drinking places, MRTSSM722USN) continues. Per-day index = (month sales / days in month) ÷ annual daily mean, computed from the FRED CSVs ([7221](https://fred.stlouisfed.org/series/MRTSSM7221USN), [722](https://fred.stlouisfed.org/series/MRTSSM722USN)). Reliability **A** (note: NSA series carries ~3–4%/yr trend growth, so Dec is biased up ~1–2 pts vs. Jan).

| Month | FSR 2017 | FSR 2018 | FSR 2019 | 722 2023 | 722 2024 | 722 2025 | Recommended |
|---|---|---|---|---|---|---|---|
| Jan | 0.92 | 0.89 | 0.88 | 0.91 | 0.88 | 0.88 | **0.88** |
| Feb | 1.02 | 0.99 | 0.98 | 0.98 | 0.99 | 0.96 | **0.97** |
| Mar | 1.04 | 1.03 | 1.01 | 1.01 | 1.01 | 1.02 | **1.02** |
| Apr | 1.04 | 1.00 | 0.99 | 1.01 | 1.01 | 1.02 | **1.00** |
| May | 1.02 | 1.03 | 1.04 | 1.02 | 1.04 | 1.06 | **1.04** |
| Jun | 1.03 | 1.07 | 1.06 | 1.04 | 1.03 | 1.04 | **1.05** |
| Jul | 0.99 | 1.03 | 1.02 | 1.01 | 1.00 | 1.01 | **1.01** |
| Aug | 0.98 | 1.03 | 1.04 | 1.01 | 1.03 | 1.04 | **1.03** |
| Sep | 0.97 | 0.97 | 0.97 | 1.02 | 1.00 | 1.00 | **0.98** |
| Oct | 0.95 | 0.96 | 0.97 | 0.99 | 1.01 | 1.01 | **0.98** |
| Nov | 0.96 | 0.96 | 0.99 | 0.97 | 1.01 | 0.99 | **0.98** |
| Dec | 1.08 | 1.06 | 1.05 | 1.02 | 1.00 | 0.99 | **1.03** |

Takeaways: January is reliably the trough (−12%); May–June and August are the peaks; December is high for full-service specifically (parties, gift cards) but flat-to-average for the broader 722 series. Trade press confirms February is historically the weakest month for same-store traffic ([QSRweb/Black Box](https://www.qsrweb.com/news/february-a-tough-month-for-restaurants-study-finds/), C).

## 3. Weather

**Rain (same day):**

| Finding | Value | Source | Reliability |
|---|---|---|---|
| Foursquare × AccuWeather, 2018 foot traffic, NYC/Chicago/Atlanta | Medium-to-heavy rain: −7.4% restaurant visits; light rain: −1.6%; heavy rain (>0.5 in) winter −11%, summer −10%, fall −1% | [Foursquare blog, Jun 2019](https://foursquare.com/?p=8611) | B (panel foot traffic, not sales; 3 big cities) |
| APT Index, June 2015 | Metros with >5 rainy days ran ~0.8 pts lower YoY comps (full-service +2.0% vs +2.8%) | [Fast Casual / APT](https://www.fastcasual.com/news/rain-impacts-june-restaurant-sales/) | C (monthly, not daily) |
| Ohio State (Bujisic) hotel-restaurant POS study, Central FL | "Rain did not appear to affect sales"; temperature was the top factor; lunch most sensitive | [Restaurant Dive, 2019](https://www.restaurantdive.com/news/fair-weather-diners-how-temperature-influences-consumer-cravings/549897/) | C (47 days, one venue) |
| Fed working paper, monthly retail | Unusual weather has a "modest but significant" role monthly; largely washes out quarterly | [Starr-McCluer 2000](https://www.federalreserve.gov/econres/feds/the-effects-of-weather-on-retail-sales.htm) | A (retail broadly; no restaurant coefficient published) |

**Temperature:** Only directional findings are published. Foursquare/AccuWeather: visits rise on unusually warm winter/spring days and cool summer days, fall on unusually cold days and hot summer days; QSR is less weather-sensitive than casual dining ([QSRweb, Jul 2019](https://www.qsrweb.com/news/the-weather-effect-report-tracks-weather-trends-related-to-dining-traffic), B/C). Snow is the big one: BJ's Restaurants reported −40% on a snowy weekend in WA/OR (single-chain anecdote, C). Black Box attributed a Jan 2018 traffic slowdown of roughly 1–1.5 pts to winter storms in the Mid-Atlantic/Midwest/Northeast ([Restaurant Business](https://www.restaurantbusinessonline.com/financing/black-box-weather-hurts-sales-january), C).

**Patio / outdoor:** No published share of sales that occurs outdoors, and no published temperature band. Toast's 2025 survey of 850 diners: 54% more likely to pick a restaurant with outdoor seating "when weather permits"; 52% say weather is the main deterrent; 62% prefer a covered patio ([Toast outdoor seating insights](https://pos.toasttab.com/blog/data/restaurant-outdoor-seating-insights), C — the "70°" figures in that article are illustrative, not measured).

**Recommended (inferred/guess):** dine-in multiplier on rainy days: light rain 0.98, measurable rain (≥0.1 in) 0.93, heavy rain/snow 0.85; snow day 0.6–0.75. Temperature: a patio bonus of +4% to +8% on days with high 65–85°F and no rain, April–October, scaled to a patio of ~20–25% of seats; a −3% to −5% penalty on days below 25°F or above 95°F. These are consistent with the Foursquare magnitudes and Toast's survey but are not measured.

## 4. Local-event effects

| Finding | Value | Source | Reliability |
|---|---|---|---|
| One full-service restaurant in Uptown Charlotte, 2007–2013, daily revenue | NFL Panthers home game: **+58.6% game day, +18.4% day before**, no effect day after; NBA home games ≈ no effect | [Depken & Fore 2016, UNC Charlotte WP 2016-016](https://belkcollegeofbusiness.charlotte.edu/economic-working-papers/wp-content/uploads/sites/850/2012/10/wp2016-016.pdf) | A/C (econometric, but n=1 restaurant steps from the stadium) |
| College football and local sales tax, 4 Texas cities | Home games generally raise monthly taxable sales, but the net effect is small and the authors answer "no" on whether it justifies policy | [Coates & Depken 2009, Eastern Economic Journal](https://ideas.repec.org/a/pal/easeco/v35y2009i4p531-547.html) | A (monthly, city level; no daily restaurant effect) |
| GO Outside Festival (downtown Roanoke/Explore Park) | ~40,000 attendees, ~$3M regional impact (2025); 44,000 and $3M (2024) | [GO Fest 2025 recap](https://roanokegofest.com/go-outside-2025-recap/); [Roanoke Regional Partnership](https://roanoke.org/go-outside-festival-drives-regional-growth-and-highlights-roanokes-outdoor-economy/) | C (organizer-reported) |

**Virginia Tech specifics:** no published estimate of VT home-game effects on Roanoke restaurants exists. Lane Stadium is ~40 miles from downtown Roanoke; game-day spending concentrates in Blacksburg. For a downtown Roanoke dinner house, a defensible range is **−5% to +5%** on Saturday day games (fans leave town midday, return for late dinner) and a small **+3% to +8%** on night games for pre-game or post-game traffic from Roanoke-based alumni; the Cal Friday-night game (Oct 24) likely pulled traffic *out* of Roanoke. Treat as a guess.

**Downtown festivals:** no published restaurant-level lift for Roanoke events. Reasoned ranges, consistent with the Charlotte study scaled for distance and the fact that festival food vendors compete with restaurants: Festival-in-the-Park / GO Fest / Local Colors / Dickens nights **+10% to +25%** on the event day for a restaurant inside the market area; Restaurant Week **+10% to +20%** traffic but check averages down (fixed-price menus); St. Patrick's parade day **+15% to +30%** for a place with a bar. Berglund Center (10,000-seat coliseum, 2,148-seat theatre, 1.5 mi from the market): **+5% to +15%** on a coliseum concert night, **+0% to +5%** for a theatre show or hockey game. All **D/guess**.

## 5. Holidays

All Toast figures are full-service restaurants on the Toast platform unless noted. Reliability **B**.

| Day | Effect | Source |
|---|---|---|
| Mother's Day (2025) | GMV **+57%** vs. avg Sunday; transactions +18%; check +32%; reservations +319% | [Toast](https://pos.toasttab.com/blog/data/mothers-day-restaurant-trends-data) |
| Mother's Day | NRA: "busiest restaurant day of the year"; 37% of adults plan to dine out (2017 survey) | [FSR / NRA](https://www.fsrmagazine.com/industry-news/research-92-million-americans-dine-out-mother-s-day/) (C) |
| Valentine's Day (Wed, 2024) | GMV **+77%** vs. avg Wednesday; transactions +41%; ticket +25%; takeout +46% | [Toast](https://pos.toasttab.com/blog/on-the-line/valentines-day-food-insights) |
| New Year's Eve (2019/20, all Toast) | **+20%** vs. December avg (open restaurants); 89% open; ticket +17% | [Toast](https://pos.toasttab.com/blog/on-the-line/new-years-2020-restaurant-trends) |
| New Year's Day | **−24%** vs. Dec avg; 67% open | same |
| Christmas Eve (2019, all Toast) | **−31%** vs. Dec avg; 76% open; check +19% | [Toast](https://pos.toasttab.com/blog/on-the-line/2019-christmas-and-christmas-eve-restaurant-trends) |
| Christmas Day | **−84%**; only 19% open | same |
| Super Bowl Sunday (2024) | transactions **−16%**, ticket −9%, dine-in −20%, delivery −9%, takeout flat; wings +87% | [Toast](https://pos.toasttab.com/blog/on-the-line/super-bowl-food-stats) |
| July 4 (Thu, 2024) | sales **−21%**, transactions −20% vs. avg Thursday; 7 p.m. hour −42% | [Toast](https://pos.toasttab.com/blog/data/fourth-of-july-restaurant-insights) |
| Thanksgiving | No Toast multiplier found. Most independent FSRs close; those open run a fixed-price meal. Model as closed or −60% to −80% (**D**) | — |

Note Valentine's 2026 is a Saturday, so the +77%-vs-Wednesday figure should be applied against a Saturday base at a smaller multiplier (~+25% to +35%, inferred). Mother's Day 2026 = May 10; Father's Day = June 21 (Toast reports it as a strong but smaller day than Mother's Day; no multiplier retrieved).

## 6. Channel mix

| Finding | Value | Source | Reliability |
|---|---|---|---|
| Full-service off-premises share of traffic, 2024 | **30%** (takeout 24%, delivery 5%, drive-thru 2%) vs. 19% in 2019 | [NRA Off-Premises Restaurant Trends 2025 (Circana/CREST data)](https://www.ncrla.org/wp-content/uploads/2025/08/Restaurant-OffPremises-Report.pdf) | B |
| Share of FSR operators offering delivery | 37% | same | B |

Sales share will be lower than traffic share because off-premises checks are smaller and carry no alcohol: for an independent dinner house with a bar, **dine-in ≈ 80–85% of dollars, takeout 12–17%, delivery 3–5%** (inferred).

**Rain bump on takeout:** no published figure for restaurants. Evidence is anecdotal (delivery platforms and local news report order spikes in storms and extreme cold: [CBS Minnesota](https://www.cbsnews.com/minnesota/news/food-delivery-orders-expected-to-spike-amidst-deep-freeze/), [NBC blizzard orders](https://www.nbcnews.com/storyline/blizzard-15/what-nyc-ordered-online-eat-during-blizzard-n295396), C). Toast's Valentine's and Super Bowl data show takeout holding or growing while dine-in falls, which supports partial substitution. Recommended: takeout/delivery **+10% to +20%** on rainy days, offsetting roughly a quarter of the dine-in loss (**D**).

## 7. Profit margin

| Finding | Value | Source | Reliability |
|---|---|---|---|
| NRA: typical restaurant pre-tax margin, pre-pandemic baseline | **~5%** | [NRA Economist's Notebook, Aug 2022](https://restaurant.org/research-and-media/research/economists-notebook/analysis-commentary/bottom-line-impact-of-rising-costs-for-restaurants/); [Bar & Restaurant, 2026](https://www.barandrestaurant.com/operations/nra-rising-costs-continue-squeeze-restaurant-profitability) | B |
| TouchBistro survey of 600+ independent full-service operators | self-reported average margin 9.8% (2024), 9.3% (2023), 10.6% (2022) | [FSR Magazine, Jan 2025](https://www.fsrmagazine.com/growth/finance/why-the-independent-restaurant-industry-has-a-chance-to-win-in-2025/) | C (self-reported; likely not pre-tax net) |
| Trade-press consensus for full-service | 3–5% net | e.g. [Restaurant365](https://www.restaurant365.com/blog/what-is-the-avg-restaurant-profit-margin/) | C |

"Single-digit margins" is correct. Use **3–6% pre-tax net** as the headline; $1.3M revenue ⇒ roughly $40k–$80k.

## 8. Daily noise

This is thin, as expected. No published coefficient of variation for daily sales at independent full-service restaurants was found; academic forecasting papers report error metrics (MAPE), not raw CVs. Starr-McCluer (A) and Black Box (C) only confirm that unexplained day-level variation is material. From the holiday and weather magnitudes above, a residual day-to-day noise of **CV ≈ 8–12%** after removing weekday, month, holiday, weather and event effects is defensible; a Saturday with 150 covers has Poisson noise alone of ~8% (**D**). Use a log-normal or gamma residual, not Gaussian, so bad days are bounded at zero.

## 9. Virginia Tech 2025 home games (confirmed)

Source: [hokiesports.com schedule release](https://hokiesports.com/news/2025/1/27/virginia-tech-footballs-2025-schedule-unveiled), [kickoff times](https://hokiesports.com/news/2025/05/29/virginia-tech-football-kickoff-times-set-for-three-more-virginia-tech-football-games), [Cal set for Fri Oct 24](https://hokiesports.com/news/2025/03/5/virginia-tech-football-set-to-host-cal-on-friday-oct-24), full results/times via [Wikipedia 2025 season](https://en.wikipedia.org/wiki/2025_Virginia_Tech_Hokies_football_team) (A/B).

| Date | Day | Opponent | Kickoff ET | Result | Attendance |
|---|---|---|---|---|---|
| Sep 6, 2025 | Sat | Vanderbilt | 7:30 pm | L 20–44 | 65,632 |
| Sep 13 | Sat | Old Dominion | 7:00 pm | L 26–45 | 57,627 |
| Sep 20 | Sat | Wofford | 12:00 pm | W 38–6 | 57,229 |
| Oct 4 | Sat | Wake Forest | 1:00 pm | L 23–30 | 65,632 |
| Oct 24 | **Fri** | California | 7:30 pm | W 42–34 (2OT) | 53,837 |
| Nov 1 | Sat | Louisville | 3:00 pm | L 16–28 | 54,030 |
| Nov 22 | Sat | Miami | 12:00 pm | L 17–34 | 65,632 |

All seven home dates are confirmed. (2026 games fall outside the Sep 2025–Aug 2026 window; for reference the first two are Sep 5 VMI 7:30 pm and Sep 12 ODU noon, per [hokiesports](https://hokiesports.com/news/2026/05/27/virginia-tech-football-acc-announces-kickoff-times-tv-designations-for-five-virginia-tech-football-games).)

## 10. Roanoke events, Sep 1 2025 – Aug 31 2026

### Downtown Roanoke Inc. and other downtown festivals

| Event | Date(s) | Venue | Source | Notes |
|---|---|---|---|---|
| Downtown Candy Crawl (DRI/Macaroni KID) | Sat Oct 26, 2025, 10am–noon | downtown | [Macaroni KID](https://roanoke.preview.macaronikid.com/articles/5f78a9ea6bca240421c57401/6th-annual-macaroni-kid-roanoke-downtown-candy-crawl) | 500+ families in 2025 ([DRI](https://www.DowntownRoanoke.org/events/signature-events)) |
| Anthem GO Outside Festival | Fri–Sun Oct 17–19, 2025 | Elmwood Park + Explore Park | [GO Fest](https://roanokegofest.com/anthem-go-outside-festival-marks-15-years-with-biggest-celebration-yet/) | ~40,000 attendees |
| Dickens of a Christmas (DRI) | Fri Dec 5, 12, 19, 2025, 6–10pm | Market Square area | [Macaroni KID guide](https://nrv.mobile.macaronikid.com/articles/69310e50e5c2f52a7c233f9e/dickens-of-a-christmas-2025-a-complete-guide-for-families) | Dec 5 tree lighting; Dec 12 parade; Dec 19 pet costume contest |
| Downtown Restaurant Week (DRI) | **2026 dates not found.** 2025 ran Fri Jan 17–Sun Jan 26 (31–33 restaurants); pattern is the 3rd–4th weekend of January, so Jan 16–25, 2026 is the best guess | downtown restaurants | [DRI 2025 page](https://www.downtownroanoke.org/do/restaurant-week-2025) | guess for 2026 |
| Roanoke Arts Pop! | Mar 6–8, 2026 | Taubman Museum | [Roanoker festival guide](https://theroanoker.com/magazine/features/the-roanoker-magazine-festivals-guide/) | |
| Freedom First St. Patrick's Day Parade & Shamrock Festival (DRI) | Sat Mar 14, 2026 | downtown | [DRI](https://www.downtownroanoke.org/news-item/freedom-first-st-patrick-s-day-parade-and-shamrock-festival-2026); [WDBJ](https://www.wdbj7.com/2026/03/13/st-patricks-day-parade-festival-return-downtown-roanoke-saturday) | |
| Down by Downtown Music Festival | Apr 16–19, 2026 | downtown venues / Elmwood | Roanoker guide | |
| Blue Ridge Marathon & finish festival | Sat Apr 18, 2026 | Elmwood Park | Roanoker guide | |
| Roanoke Pride Festival | Sun Apr 26, 2026 | Elmwood Park | Roanoker guide | |
| Community School Strawberry Festival | Fri–Sat May 1–2, 2026 | Elmwood Park | [Roanoker May–Jun calendar](https://theroanoker.com/events-calendar-may-june-2026/) | |
| Local Colors Festival | Sat May 16, 2026 | Elmwood Park | same | |
| Festival in the Park | Fri–Sun May 22–24, 2026 (Memorial Day wknd; 2025 was May 23–25) | Elmwood Park | same; [Roanoker 2025](https://theroanoker.com/seasonal-celebrations/) | |
| Sidewalk Art Show | May 30–31, 2026 | around Taubman | same | |
| First Fridays | first Friday monthly, May–Oct | Franklin Rd | Roanoker guide | |
| Party in Elmwood (DRI) | Thursdays in summer (dates not published) | Elmwood Park | [DRI](https://www.DowntownRoanoke.org/events/signature-events) | |
| Budweiser Summer Series (DRI) | 2–3 concerts/summer, dates not found for 2026 | Elmwood amphitheater | DRI | |
| Downtown Sidewalk Sale (DRI) | August, exact dates not found | downtown retail | DRI | |
| Roanoke Taco Fest | Sat Aug 29, 2026 | Elmwood Park | Roanoker guide | |

Not found: **Big Lick BBQ** and a downtown **Chili Cook-off** do not appear on DRI's current signature-event list or in 2025–26 press; treat as not held in this window. Movies in the Market (DRI, summer) exists but no 2026 dates were published.

### Berglund Center, Sep 2025 – Aug 2026 (partial — see note)

Songkick and Bandsintown blocked scraping; this list is assembled from [concertarchives.org](https://www.concertarchives.org/venues/berglund-center), [The Roanoker](https://theroanoker.com/category/berglund-center/), [WSLS](https://www.wsls.com/topic/Berglund_Center/), the [Roanoke Rambler calendar](https://www.roanokerambler.com/happenings-the-only-roanoke-events-calendar-youll-ever-need-week-of-9-24-25-to-10-1-25/), and [Broadway in Roanoke season release](https://www.wsls.com/news/local/2025/05/17/berglund-center-announces-20252026-broadway-in-roanoke-lineup). The city says Berglund books ~400 events/yr ([Cardinal News](https://cardinalnews.org/2026/03/19/roanokes-berglund-center-was-built-for-the-entertainment-landscape-of-1971-that-world-doesnt-exist-today/)), most of them small; the list below is the ticketed shows that got press. Reliability C; dates marked (?) have conflicting sources.

| Date | Event | Hall |
|---|---|---|
| Thu Sep 11, 2025 | Alabama w/ Exile | Coliseum |
| Mon Sep 15 | Ryan Adams | Theatre |
| Thu Sep 18 or Sun Sep 28 (?) | KALEO | Coliseum |
| Sat Sep 20 | Jerry Seinfeld | Theatre |
| Wed Sep 24 | Avatar: The Last Airbender in Concert | Theatre |
| Thu Sep 25 | The Fab Four | Theatre |
| Oct 3–5 | Craftsmen's Fall Classic | Special Events Ctr |
| Fri Oct 10 | Jo Koy | Theatre |
| Oct 10–12 | Heritage Arts Tattoo Convention | Special Events Ctr |
| Fri Oct 17 | Rail Yard Dawgs home opener (SPHL; 29 home games Oct–Apr, Fri/Sat-heavy, 7:05 pm) | Coliseum |
| Sat Oct 18 | Matt Mathews (comedy) | Theatre |
| Sat Oct 25 | Randy Travis "More Life" | Theatre |
| Nov 6–9 | Disney On Ice: Road Trip Adventures | Coliseum |
| Thu Nov 20 | Jim Henson's Labyrinth in Concert | Theatre |
| Tue Nov 25 | Dolly Parton's Smoky Mountain Christmas Carol (Broadway) | Theatre |
| Fri Nov 28 | Rail Yard Dawgs Black Friday game | Coliseum |
| Sat Dec 20 | Rail Yard Dawgs Teddy Bear Toss | Coliseum |
| Sun Dec 21 | Vienna Light Orchestra | Theatre |
| Wed Dec 31 | Rail Yard Dawgs NYE game | Coliseum |
| Wed Feb 4, 2026 | Hadestown (Broadway) | Theatre |
| Feb 6–8 (wknd) | Big Lick Comic Con | Special Events Ctr |
| Feb 20–22 (wknd) | Greater Roanoke Home & Garden Show | Special Events Ctr |
| Tue Feb 24 | Riverdance 30 | Theatre |
| Wed Mar 11 | Harlem Globetrotters | Coliseum |
| Thu Apr 16 | William Shatner | Theatre |
| Mon Apr 27 | Clue – Live on Stage (Broadway) | Theatre |
| Sat May 2 | Taco'Ritas festival | Special Events Ctr |
| Fri May 29 | Tracy Lawrence | Theatre |
| Sun May 31 | Josh Gates | Theatre |
| Thu Jun 4 | Journey – Final Frontier Tour | Coliseum |
| Wed Jun 10 | Mrs. Doubtfire (Broadway) | Theatre |
| Thu Jun 18 | Josh Turner | Theatre |
| Tue Jul 14 | Billy Strings | Coliseum |
| Sat Aug 1 | Jason Isbell & the 400 Unit | Theatre |
| Aug 7–9 (wknd) | Big Lick Comic Con (summer) | Special Events Ctr |
| Sat Aug 8 | Leanne Morgan | Coliseum |

For the simulator, the coliseum concerts (Alabama, KALEO, Journey, Billy Strings, Leanne Morgan) and Disney On Ice are the only ones large enough to plausibly move a downtown restaurant's night; Rail Yard Dawgs games (2,000–4,000 fans) and theatre shows are marginal.

---

## Recommended simulator parameters

| Parameter | Value | Confidence |
|---|---|---|
| Annual revenue | $1.3M (given) | — |
| Weekday weights Mon–Sun | 9 / 10 / 11 / 13 / 19 / 22 / 16 % | inferred (Toast Sat +41% items, Square weekend 35%) |
| Monthly index Jan–Dec | 0.88 / 0.97 / 1.02 / 1.00 / 1.04 / 1.05 / 1.01 / 1.03 / 0.98 / 0.98 / 0.98 / 1.03 | sourced (Census NAICS 7221 & 722, NSA) |
| Rain, dine-in multiplier | light 0.98; ≥0.1 in 0.93; heavy 0.85 | inferred (Foursquare −1.6% / −7.4% / −10–11%) |
| Snow day, dine-in | 0.60–0.75 | guess (BJ's −40% weekend anecdote; Black Box) |
| Rain, takeout/delivery multiplier | 1.10–1.20 | guess |
| Patio bonus (65–85°F, dry, Apr–Oct) | +4% to +8% | guess (Toast survey directional) |
| Extreme temp penalty (<25°F or >95°F) | −3% to −5% | guess (Foursquare directional) |
| Dine-in / takeout / delivery $ share | 82 / 14 / 4 % | inferred (NRA/Circana 30% off-prem traffic) |
| Mother's Day | 1.55 × avg Sunday | sourced (Toast +57% GMV) |
| Valentine's Day (Sat 2026) | 1.30 × Saturday | inferred (Toast +77% vs Wed) |
| New Year's Eve | 1.20 × December avg | sourced (Toast) |
| New Year's Day | 0.75 | sourced (Toast) |
| Christmas Eve | 0.70 (or 0 if closed) | sourced (Toast) |
| Christmas Day | closed (0) | sourced (81% closed) |
| Thanksgiving | closed (0) | guess |
| Super Bowl Sunday (Feb 8, 2026) | 0.80 dine-in; takeout 1.0 | sourced (Toast) |
| July 4 | 0.80 | sourced (Toast −21%) |
| Major downtown festival day (GO Fest, Festival in the Park, Local Colors, Dickens, St. Pat's) | +10% to +25% | guess (Charlotte NFL +58% is the only daily restaurant estimate; scaled down) |
| Restaurant Week | traffic +15%, check −10% | guess |
| Berglund coliseum concert night | +5% to +15% | guess |
| Berglund theatre / hockey | 0% to +5% | guess |
| VT home game (Sat day) | −5% to +5% | guess |
| VT home game (night) | +3% to +8% | guess |
| Pre-tax net margin | 3–6% | sourced (NRA ~5%) |
| Residual daily noise | CV 8–12%, log-normal | guess |

## Sources

1. FRED, Retail Sales: Full Service Restaurants, NSA (MRTSSM7221USN) — https://fred.stlouisfed.org/series/MRTSSM7221USN
2. FRED, Retail Sales: Food Services and Drinking Places, NSA (MRTSSM722USN) — https://fred.stlouisfed.org/series/MRTSSM722USN
3. Toast, 2018 Year in Review — https://pos.toasttab.com/year-in-review
4. Toast Q3 2023 Restaurant Trends (BusinessWire) — https://www.businesswire.com/news/home/20231207135338/en
5. Toast Q3 2024 reservation trends (BusinessWire) — https://www.businesswire.com/news/home/20241210819521/en/Toast-Data-Reservation-Trends-Shift-to-Slower-Days-and-Early-Dinners
6. Square Spring Restaurant Report 2024 via Axios — https://www.axios.com/2024/05/14/restaurants-eating-out-rates-weekend-weekday
7. Square Q2 2023 via TSG — https://tsgpayments.com/square-q2-restaurant-industry-reportin-post-pandemic-era-restaurantspending-shifts-from-friday-to-saturday/
8. Foursquare × AccuWeather, "Fair-weather foodies" (2019) — https://foursquare.com/?p=8611
9. QSRweb on Foursquare/AccuWeather report — https://www.qsrweb.com/news/the-weather-effect-report-tracks-weather-trends-related-to-dining-traffic
10. Fast Casual / APT Index, rain and June 2015 sales — https://www.fastcasual.com/news/rain-impacts-june-restaurant-sales/
11. Restaurant Dive, OSU weather research — https://www.restaurantdive.com/news/fair-weather-diners-how-temperature-influences-consumer-cravings/549897/
12. Starr-McCluer, "The Effects of Weather on Retail Sales," Fed FEDS 2000-08 — https://www.federalreserve.gov/econres/feds/the-effects-of-weather-on-retail-sales.htm
13. Restaurant Business / Black Box, Jan 2018 weather — https://www.restaurantbusinessonline.com/financing/black-box-weather-hurts-sales-january
14. Toast outdoor seating survey — https://pos.toasttab.com/blog/data/restaurant-outdoor-seating-insights
15. Depken & Fore (2016), UNC Charlotte WP 2016-016 — https://belkcollegeofbusiness.charlotte.edu/economic-working-papers/wp-content/uploads/sites/850/2012/10/wp2016-016.pdf
16. Coates & Depken (2009), Eastern Economic Journal — https://ideas.repec.org/a/pal/easeco/v35y2009i4p531-547.html
17. Toast Mother's Day data — https://pos.toasttab.com/blog/data/mothers-day-restaurant-trends-data
18. Toast Valentine's Day data — https://pos.toasttab.com/blog/on-the-line/valentines-day-food-insights
19. Toast Christmas Eve/Day 2019 — https://pos.toasttab.com/blog/on-the-line/2019-christmas-and-christmas-eve-restaurant-trends
20. Toast New Year's 2020 — https://pos.toasttab.com/blog/on-the-line/new-years-2020-restaurant-trends
21. Toast Super Bowl data — https://pos.toasttab.com/blog/on-the-line/super-bowl-food-stats
22. Toast July 4 data — https://pos.toasttab.com/blog/data/fourth-of-july-restaurant-insights
23. FSR / NRA Mother's Day survey — https://www.fsrmagazine.com/industry-news/research-92-million-americans-dine-out-mother-s-day/
24. NRA Off-Premises Restaurant Trends 2025 (hosted by NCRLA) — https://www.ncrla.org/wp-content/uploads/2025/08/Restaurant-OffPremises-Report.pdf
25. NRA Economist's Notebook, rising costs (2022) — https://restaurant.org/research-and-media/research/economists-notebook/analysis-commentary/bottom-line-impact-of-rising-costs-for-restaurants/
26. Bar & Restaurant / NRA profitability (2026) — https://www.barandrestaurant.com/operations/nra-rising-costs-continue-squeeze-restaurant-profitability
27. FSR Magazine / TouchBistro margins — https://www.fsrmagazine.com/growth/finance/why-the-independent-restaurant-industry-has-a-chance-to-win-in-2025/
28. hokiesports.com 2025 schedule — https://hokiesports.com/news/2025/1/27/virginia-tech-footballs-2025-schedule-unveiled
29. hokiesports.com 2025 kickoff times — https://hokiesports.com/news/2025/05/29/virginia-tech-football-kickoff-times-set-for-three-more-virginia-tech-football-games
30. hokiesports.com Cal on Fri Oct 24 — https://hokiesports.com/news/2025/03/5/virginia-tech-football-set-to-host-cal-on-friday-oct-24
31. Wikipedia, 2025 Virginia Tech Hokies football team — https://en.wikipedia.org/wiki/2025_Virginia_Tech_Hokies_football_team
32. Downtown Roanoke Inc. signature events — https://www.DowntownRoanoke.org/events/signature-events
33. DRI Restaurant Week 2025 — https://www.downtownroanoke.org/do/restaurant-week-2025
34. DRI St. Patrick's 2026 — https://www.downtownroanoke.org/news-item/freedom-first-st-patrick-s-day-parade-and-shamrock-festival-2026
35. The Roanoker 2026 festival guide — https://theroanoker.com/magazine/features/the-roanoker-magazine-festivals-guide/
36. The Roanoker May–June 2026 calendar — https://theroanoker.com/events-calendar-may-june-2026/
37. The Roanoker 2025 seasonal celebrations — https://theroanoker.com/seasonal-celebrations/
38. GO Fest 2025 recap — https://roanokegofest.com/go-outside-2025-recap/
39. Roanoke Regional Partnership on GO Fest 2024 — https://roanoke.org/go-outside-festival-drives-regional-growth-and-highlights-roanokes-outdoor-economy/
40. Macaroni KID, Dickens 2025 guide — https://nrv.mobile.macaronikid.com/articles/69310e50e5c2f52a7c233f9e/dickens-of-a-christmas-2025-a-complete-guide-for-families
41. Macaroni KID, Candy Crawl 2025 — https://roanoke.preview.macaronikid.com/articles/5f78a9ea6bca240421c57401/6th-annual-macaroni-kid-roanoke-downtown-candy-crawl
42. concertarchives.org Berglund Center — https://www.concertarchives.org/venues/berglund-center
43. The Roanoker Berglund Center category — https://theroanoker.com/category/berglund-center/
44. WSLS Berglund Center topic page — https://www.wsls.com/topic/Berglund_Center/
45. WSLS Broadway in Roanoke 2025–26 — https://www.wsls.com/news/local/2025/05/17/berglund-center-announces-20252026-broadway-in-roanoke-lineup
46. Rail Yard Dawgs 2025–26 home schedule — https://www.railyarddawgs.com/25-26-home-game-scheduled-announced
47. Cardinal News on Berglund Center — https://cardinalnews.org/2026/03/19/roanokes-berglund-center-was-built-for-the-entertainment-landscape-of-1971-that-world-doesnt-exist-today/
48. Roanoke Rambler calendar, week of 9/24/25 — https://www.roanokerambler.com/happenings-the-only-roanoke-events-calendar-youll-ever-need-week-of-9-24-25-to-10-1-25/
