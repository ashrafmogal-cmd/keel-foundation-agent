# Keel Semantic Layer — Q&A Answer Log

This file logs questions asked to Keel and the key findings from each answer.
Used for learning, pattern recognition, and stakeholder reference.

---

## Q1 — Daily HP Sessions (Mar 1–7, 2026)
**Asked:** What are the daily sessions on homepage from 3/1 to 3/7?
**Table:** wmt-site-content-strategy.scs_production.hp_session
**Platforms:** App: iOS + App: Android
**Key Findings:**
- Sunday 3/1 peaked at 26,715,070 sessions (weekend surge, +16% vs weekday avg)
- Weekday average: ~23,207,000 sessions/day
- Saturday 3/7: 25,526,037 sessions
- HP Visitation Rate: stable at 80.53%–80.94% across all 7 days
- iOS = ~73% of HP sessions, Android = ~27%
- Week aligns with March Savings Event (WK8 FY27, 95% Card 1 SOV)
- Total weekly sessions: 168,474,712
**Data Quality Note:** None. hp_session is a clean, small table (~10MB).

---

## Q2 — ATF Module GMV (Feb 1–14, 2026)
**Asked:** Which modules in ATF are driving the most GMV for 2/1 to 2/14?
**Table:** wmt-site-content-strategy.scs_production.hp_summary_asset
**Platforms:** App: iOS + App: Android
**ATF Definition:** content_zone IN ('contentZone1'–'contentZone6')
**Key Findings (CORRECTED — CZ1–CZ6 scope):**
- SIG Card 1: $8,862,573 GMV | GMV/click $1.25 — **#1 ATF driver**
- SIG Card 2: $1,109,948 GMV | GMV/click $1.00
- AutoScroll Card 1: $662,285 GMV | GMV/click $1.10
- P13N Item Carousel: $544,221 GMV | GMV/click null (clicks not captured in CZ1–6 scope)
- SIG Card 3: $502,998 GMV | GMV/click $0.95
- SIG Card 4: $238,520 GMV | GMV/click $1.02
- SIG Card 5: $107,247 GMV | GMV/click $0.89
- AutoScroll Card 2: $99,456 GMV | GMV/click $0.33
- AutoScroll Card 3: $76,470 GMV | GMV/click $0.32
- AutoScroll Card 5: $72,235 GMV | GMV/click $0.49
- AutoScroll Card 4: $69,946 GMV | GMV/click $0.61
- SIG Card 6: $56,082 GMV | GMV/click $0.67
- Merch Item Carousel: $42,235 GMV
**Key Insight:** P13N Item Carousel showed $18M GMV in first (wrong) query without CZ filter — dropped to
  $544K with correct ATF CZ1–6 scope. 97% of P13N GMV is actually BTF. SIG Card 1 alone ($8.86M)
  outperforms all 5 HPOV AutoScroll cards combined (~$980K).
**Data Quality Note:** atf_flag column is UNRELIABLE — tags ALL modules as 'BTF' including HPOV AutoScroll Cards.
  Use content_zone field (CZ1–CZ6 = ATF) for all ATF/BTF filtering.

**⚠️ CORRECTION (User Feedback):**
- ATF definition: Use content_zone field. contentZone1–contentZone6 = ATF. contentZone7+ = BTF.
- Do NOT use atf_flag column for ATF/BTF filtering — unreliable (tags all modules as BTF).
- Correct SQL filter: WHERE content_zone IN ('contentZone1','contentZone2','contentZone3','contentZone4','contentZone5','contentZone6')
- Excel: Keep formatting basic — no colors, simple table only.
- Metrics to report: GMV + GMV/click only (no CTR, impressions, clicks unless specifically asked).

---

## Q3 — CTR WoW: All HP Modules (Mar 28–Apr 3 vs Mar 21–27)
**Asked:** What is the CTR for this week vs last week?
**Table:** wmt-site-content-strategy.scs_production.hp_summary_asset
**Platforms:** App: iOS + App: Android
**This Week:** 2026-03-28 to 2026-04-03 (Easter week — Easter = Apr 5, 2026)
**Last Week:** 2026-03-21 to 2026-03-27

**HPOV CTR WoW (with benchmarks):**
- AutoScroll Card 1: 0.21% → TW | 0.15% → LW | +40.0% WoW | Benchmark: 0.23% (still below)
- AutoScroll Card 2: 0.16% TW | 0.09% LW | +77.5% WoW | Benchmark: 0.15% (NOW ABOVE ✅)
- AutoScroll Card 3: 0.10% TW | 0.10% LW | -1.3% WoW | Benchmark: 0.13% (below)
- AutoScroll Card 4: 0.32% TW | 0.36% LW | -10.4% WoW | Benchmark: 0.17% (above ✅)
- AutoScroll Card 5: 0.39% TW | 0.29% LW | +35.4% WoW | Benchmark: 0.25% (above ✅)

**Top Movers WoW:**
- AutoScroll Card 2: +77.5% (biggest HPOV gainer)
- Social Carousel: -62.8% (biggest drop — reduced SOV or content swap)
- Hubspoke: +36.4%
- SIG Card 5: +32.4%
- AutoScroll Card 1: +40.0%

**Key Insight:** Easter week (Mar 28–Apr 3) driving broad CTR lift across most modules. Cards 2, 4, 5 now above their benchmarks. Social Carousel -63% is an anomaly worth investigating.
**Data Quality Note:** Generic module name rows (SIG, AutoScroll, TriplePack) with near-zero impressions produce impossible CTRs (10,000%+) — excluded from output. Always filter noise rows by minimum impression threshold.
**SQL Pattern Used:** Single pivot query with CASE WHEN per week for conditional aggregation — cost efficient (one scan, two week comparison).

**⚠️ CORRECTIONS FROM USER FEEDBACK (Q3):**
1. CTR formula is `overall_click_count / module_view_count` — NOT `asset_clicks_count / module_view_count`
2. Module grain for breakdowns = `moduletype` (not `hp_module_name`). moduletype is the higher-level grouping. hp_module_name is a sub-breakdown.
3. When asked for "homepage CTR" → give ONE overall number first, then ask if user wants a breakdown.
4. Only drill to hp_module_name if explicitly asked for card-level detail.

---

**CORRECTIONS FROM USER FEEDBACK (Q3):**
- CTR formula = overall_click_count / module_view_count (NOT asset_clicks_count)
- Module breakdown grain = moduletype (NOT hp_module_name — that is a sub-level). When asked for homepage CTR: return ONE number first, then offer breakdown
- Only drill to hp_module_name when explicitly asked for card-level detail

---

**CORRECTION (Q3 + all future queries):**
- ALWAYS filter Content_Type = 'Merch' when calculating CTR, GMV, or any performance metric
- Content_Type is a derived CASE expression — not a raw column in the table
- WMC = ads content (content_served_by='ads' or specific zone/module combos)
- Merch = organic site merchandising content (everything else)
- Full formula saved in: business_context/content_type_filter.md

---

## Q4 — CVP Meet Item Coverage (Week 20 Discovery)
**Asked:** What is the CVP meet item coverage for week 20?
**Table:** wmt-site-content-strategy.scs_production.CVPsummary
**Outcome:** W-20 does not exist in the available data. User to confirm correct week.

**8-Step Process Summary:**
- Step 1: Metric = cvp_met_ind=1 / CV_Focus_SKU_IND=1. Table = CVPsummary (2.32B rows).
- Step 2: MANDATORY event_dt filter before anything. fiscal_week format = W-NN.
- Step 3: Read CVPsummary.md — noted data range documented as Aug 2025 to Mar 2026.
- Step 4: Ran cheap discovery on narrow date range to map fiscal_week to dates. Found data = W-26 (Aug 2025) to W-10 (Apr 4 2026). 37 distinct weeks.
- Step 5: W-20 not in range. FY26 W-20 = June 2025 (before data). FY27 W-20 = May 2026 (future). Stopped before expensive full query.
- Step 6: Confirmed running WHERE fiscal_week='W-20' would scan 812GB+ and return 0 rows. Correct to pause.
- Step 7: Provided full 37-week map with start/end dates. Offered 4 likely interpretations.
- Step 8: Did NOT run main CVP query (cost saved). Awaiting user clarification.

**CVPsummary Confirmed Date Range (updated from knowledge base):**
- Earliest: W-26 = 2025-08-01
- Latest: W-10 = 2026-04-04 (partial, 1 day)
- Most recent complete week: W-09 (2026-03-28 to 2026-04-03)
- Total distinct weeks: 37

**Key Fiscal Week Markers:**
- W-26: CVP data start (Aug 1, 2025)
- W-42: AE2/Cyber Monday (Nov 15-21, 2025)
- W-52: Last week of FY26 (Jan 24-30, 2026)
- W-01: FY27 begins (Jan 31, 2026)
- W-09: Most recent complete week (Mar 28 - Apr 3, 2026)
- W-10: Partial (Apr 4, 2026 only)

---

## Q5 — HPOV Card 1 W+ Impression Scenario (70% Shift)
**Asked:** If 70% of HPOV impressions in Card 1 shift to W+ messaging, how many impressions and % of HPOV impressions go to W+?
**Table:** wmt-site-content-strategy.scs_production.hp_summary_asset
**Type:** Scenario / projection analysis (not a raw data pull)
**Reference Period:** W-09 (Mar 28-Apr 3 2026) + 4-week window (Mar 7-Apr 3 2026)

**Raw Data:**
- Card 1 impressions (W-09): 165,653,671
- Total HPOV impressions (W-09): 453,753,261
- Card 1 SOV within HPOV: 36.5% (aligns with knowledge base ~35%)

**Scenario Math (70% of Card 1 to W+):**
- W+ impressions (W-09): 165,653,671 x 0.70 = 115,957,570
- W+ impressions (4-week): 636,935,262 x 0.70 = 445,854,683
- W+ daily average: ~15,923,381 impressions/day
- W+ as % of total HPOV: 25.6% (W-09) / 25.9% (4-week) — very consistent

**Key Insights:**
- This scenario = 116M W+ impressions/week vs W+ Week event benchmark of 55M (2x higher volume but lower SOV: 25.6% vs 47%)
- Card 1 SOV (36.5%) x 70% = 25.6% of HPOV — mathematically clean
- Consistent across W-09 and 4-week periods = stable base for planning

**Methodology Notes:**
- No content_type Merch filter applied — impression capacity question, not a CTR/GMV metric
- Card 1 has no WMC — filter would not change Card 1 numbers but would distort total HPOV denominator
- Scenario assumes static 70% allocation; P13N algo distributes dynamically in practice

---

## Q6 — Desktop ATF HPOV + SIG Avg Daily Impressions (Nov 18-24 2025)
**Asked:** What are the avg daily impressions on Desktop ATF HPOV and SIG from 11/18 to 11/24?
**Table:** wmt-site-content-strategy.scs_production.hp_summary_asset
**Platform:** Web: Desktop (experience_lvl2 = 'Web: Desktop')
**Date Range:** 2025-11-18 to 2025-11-24 (7 days | W-42/W-43, AE2 event period)

**KEY DATA FINDING — ATF Flag Not Available for Desktop:**
- All Desktop rows in hp_summary_asset have atf_flag = 'BTF' — zero ATF rows exist
- Desktop HPOV is visually ATF but not tagged as such in the data pipeline
- Likely a data instrumentation gap — worth flagging to data team
- Query ran without ATF filter (all Desktop data returned)

**Results:**
- Desktop HPOV (PrismAdjustableCardCarousel): 4,173,161 avg daily impressions | 29,212,130 total (7 days) | Min: 3,201,023 | Max: 6,308,037
- Desktop SIG (PrismScrollableItemGrid): 163,482 avg daily impressions | 1,144,371 total (7 days) | Min: 108,363 | Max: 333,561

**Context:**
- Desktop HPOV is 26x larger than Desktop SIG
- Desktop HPOV (4.2M/day) vs App Card 1 alone (~24M/day) = Desktop ~17% of App Card 1
- Max HPOV daily (6.3M) likely = AE2 Black Friday peak. Min (3.2M) = pre-event days
- 2x day-over-day range on HPOV confirms strong event-driven traffic variation

**Platform Discovery Learnings (save for future queries):**
- Desktop platform string: 'Web: Desktop' (NOT 'App: Desktop' or 'Desktop')
- App platforms: 'App: iOS', 'App: Android' (with space after colon)
- atf_flag column values: 'ATF' and 'BTF' for App; only 'BTF' for Desktop
- ALWAYS run platform discovery query for non-standard platforms before main query

---

## Q6b — Desktop ATF Zone Definition + HPOV/SIG Zone Correction

**Context:** User clarified that Desktop ATF = contentZone7 to contentZone27 (business definition).
**Key Finding:** Desktop HPOV and SIG are NOT in zones 7-27.

**Zone mapping confirmed (Nov 18-24 2025):**
- HPOV (PrismAdjustableCardCarousel) primary zone: contentZone3 (NOT in ATF range 7-27). Only 86 total impressions in zone 11 over 7 days (12 avg daily = negligible noise)
- SIG (PrismScrollableItemGrid) primary zones: contentZone41, contentZone42 (NOT in ATF range 7-27). Only 2,269 total impressions in zone 12 over 7 days (324 avg daily = negligible noise)

**Desktop ATF Zones 7-27 — What IS in there:**
- PrismAdjustableBanner (Adjustable Banner Small/Medium) — zones 7, 8, 9, 14, 15, 18, 19
- PrismTriplePack (Triple Pack sizes) — zones 9, 10, 15, 16
- ItemCarousel (P13N + Merch) — zones 12, 14, 15, 18, 19
- PrismHeroCarousel — zones 12, 14, 15, 18, 19
- DepartmentsGrid — zone 10

**Rule saved:** reporting_conventions.md updated with full Desktop ATF definition, zone mapping, and query pattern.

---

## Q7 — Why Does ETS (Tech) on SIG Have Higher SOV Despite Lower CTR?
**Asked:** Why does the tech message on SIG see higher share of voice despite lower CTR?
**Table:** wmt-site-content-strategy.scs_production.hp_summary_asset
**Module:** PrismScrollableItemGrid (SIG) | Merch filter applied | iOS + Android
**Date:** Last 28 days (approx Mar 10 - Apr 7, 2026)

**Premise Confirmed:**
- ETS SOV: 12.87% (2nd highest after CROSS CATEGORY at 72.31%)
- ETS CTR: 0.5312% (5th out of 7 SBUs — lower than FASHION 0.8875%, HOME 0.8185%, HARDLINES 0.7638%, CROSS CATEGORY 0.8959%)
- ETS has 2nd highest SOV but 5th lowest CTR — premise confirmed

**Full SBU Breakdown (SOV + CTR + ATCs):**
| SBU | SOV% | CTR% | ATC/1K | GMV/imp | GMV/click | Total ATCs |
|-----|------|------|--------|---------|-----------|-----------|
| CROSS CATEGORY | 72.31% | 0.8959% | 2.11 | $0.0044 | $0.49 | 2,090,953 |
| ETS | 12.87% | 0.5312% | 1.10 | $0.0019 | $0.36 | 193,117 |
| CONSUMABLES | 8.85% | 0.3596% | 0.94 | $0.0015 | $0.41 | 113,447 |
| FOOD | 2.51% | 0.4785% | 3.82 | $0.0050 | $1.04 | 130,787 |
| HOME | 1.71% | 0.8185% | 0.91 | $0.0044 | $0.54 | 21,318 |
| HARDLINES | 1.05% | 0.7638% | 0.65 | $0.0021 | $0.28 | 9,389 |
| FASHION | 0.70% | 0.8875% | 0.87 | $0.0021 | $0.23 | 8,379 |

**The 5 Business Reasons ETS Gets High SOV Despite Lower CTR:**
1. **Absolute ATC Volume** — 193K total ATCs (2nd highest). P13N reads historical ATC volume, not just rate. High absolute conversion = high algorithmic confidence.
2. **Large Customer Segment** — Tech/Electronics is one of Walmart's largest customer interest segments. More eligible customers = more P13N impression allocations = higher natural SOV.
3. **High ASP Masks True GMV** — ETS items ($200-$2000+) are high-consideration purchases. HP strict last-touch attribution undercounts ETS GMV (research → external comparison → return to buy breaks attribution chain). Real downstream value is higher than $0.36/click suggests.
4. **Message Tiering Priority** — Tech/ETS messages (seasonal, brand launches, back to school) frequently qualify for Tier 1/2 status. SIG algorithm respects message tier — higher tier = impression floor guaranteed.
5. **P13N Multi-Signal Optimization** — P13N optimizes CTR + ATC + GMV + CLTV composite. ETS scores strongly on ATC volume and customer CLTV signals despite lower CTR rate. Fewer clicks but higher-value customers.

**FOOD Anomaly:**
- FOOD: highest ATC/1K (3.82) and highest GMV/click ($1.04) but only 2.51% SOV
- Explanation: FMCG/Grocery replenishment is handled by ATF P13N carousels (Continue Your Shopping, Price Drops For You). BTF SIG is less relevant for replenishment behavior — groceries get bought from ATF P13N automatically, not from a SIG push.
