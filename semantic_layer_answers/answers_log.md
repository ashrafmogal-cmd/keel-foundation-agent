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

## Q7 — SIG contentZone5 SOV by Message Category (Tech Premise Was False)
**Asked:** Why does the Tech message on SIG see higher Share of Voice despite lower CTR?
**Keel Finding:** PREMISE IS INCORRECT. Tech is 7th out of 10 categories in SOV (3.88%). It does NOT have the highest SOV.
**Self-correction:** Step 6 (Evaluate) failed — Keel initially wrote "Premise Confirmed" without checking if Tech was actually #1 in SOV. It was not.

**Zone context:**
- contentZone4 = 100% P13N/Unattributed. No named merch messages.
- contentZone5 = Site merch driven. All named campaigns live here.

**Full CZ5 Results (message_name REGEX classifier, Last 28 Days):**
| Rank | Category | SOV% | CTR% | ATC/1K | GMV/imp | GMV/click |
|------|----------|------|------|--------|---------|----------|
| 1 | Cross Category / Savings | 44.47% | 0.9283% | 1.804 | $0.0049 | $0.53 |
| 2 | Toys / Kids / Baby | 21.89% | 0.6309% | 2.784 | $0.0033 | $0.53 |
| 3 | Home | 8.98% | 1.0405% | 1.059 | $0.0033 | $0.32 |
| 4 | Beauty / Personal Care | 5.52% | 0.3115% | 0.486 | $0.0009 | $0.29 |
| 5 | Fashion | 4.83% | 0.5010% | 0.765 | $0.0014 | $0.29 |
| 6 | Consumables / Health | 4.44% | 0.4375% | 1.757 | $0.0024 | $0.55 |
| **7** | **Tech / Electronics** | **3.88%** | **0.4232%** | **0.362** | $0.0018 | $0.43 |
| 8 | Other | 2.04% | 0.4836% | 2.097 | $0.0026 | $0.53 |
| 9 | Food | 1.97% | 0.4017% | 2.406 | $0.0039 | $0.98 |
| 10 | Sports / Auto / Pets | 1.36% | 0.6973% | 0.696 | $0.0019 | $0.27 |
| 11 | P13N / Unattributed | 0.61% | 0.4489% | 0.506 | $0.0013 | $0.30 |

**What the data actually shows:**
- Tech is NOT highest SOV — 6 categories outrank it
- Tech has LOWEST ATC/1K (0.362) — arguably over-indexed at 7th SOV given its weak performance
- Home: highest CTR (1.04%) but only 3rd SOV — under-indexed vs performance
- Sports: strong CTR (0.70%) but only 10th SOV — most under-indexed vs CTR
- Food: highest ATC/1K (2.406) but only 9th SOV — served by ATF P13N instead, not BTF SIG

**REGEX Tech messages confirmed (CZ5):**
- Tech Rollbacks And More: 51,254,598 imp, 0.4243% CTR
- 2026 March Savings Event Tech: 1,187,889 imp, 0.3771% CTR
- Pattern: r'tech|electron|gaming and media|pc gaming|laptop|tablet|computer'
- Game Time excluded intentionally (sports event)

**Keel self-correction rule added:**
ALWAYS verify the premise in a question against the data BEFORE building an explanation. If the premise is false, state it clearly first. Do not "confirm" premises that contradict the data.

---

## Q8 — WMC Impressions This Week (WTD)
**Asked:** What is the volume of impressions that went into Ads/WMC this week?
**Rule Applied:** HPsummary + Content_Type = 'WMC' (user correction from using content_served_by = 'ads' on hp_summary_asset)
**Platform discovery:** WMC rows in HPsummary use 'App: iOS' WITH space (same as hp_summary_asset — NOT 'App:iOS' without space as documented for Merch rows)

**Date:** WTD Sat Apr 4 – Sun Apr 5, 2026 (2 of 4 days loaded — Apr 6+7 pending pipeline)
**Note:** HPsummary WMC only shows Apr 5. Apr 4 present in hp_summary_asset but not HPsummary WMC rows.

**Results (Apr 5 — 1 day loaded in HPsummary WMC):**
| Module | Impressions | Clicks | CTR |
|--------|------------|--------|-----|
| AutoScroll Card 2 | 9,584,775 | 10,227 | 0.1067% |
| AutoScroll Card 3 | 7,302,306 | 10,955 | 0.1500% |
| Adjustable Banner Small | 4,875,059 | 18,779 | 0.3852% |
| Triple Pack Small | 2,621,659 | 5,112 | 0.1950% |
| Adjustable Banner Medium | 12 | — | — |
| AutoScroll Card 4 | 3 | — | — |
| **TOTAL WMC (WTD)** | **24,383,814** | **45,073** | **0.1848%** |

**Key findings:**
- HPsummary provides richer WMC data than hp_summary_asset: Adjustable Banner Small clicks tracked (hp_summary_asset showed null), Triple Pack Small visible as WMC module
- Card 3 CTR (0.15%) at benchmark. Card 2 CTR (0.11%) below benchmark (0.15%)
- Adjustable Banner Small CTR (0.39%) highest of all WMC modules — unexpected given it showed null clicks in hp_summary_asset

---

## Q8 (CORRECTED) — WMC Impressions This Week using Correct Method
**Rule confirmed:** NEVER use HPsummary. Always use hp_summary_asset + CASE WHEN content type classifier.
**Table:** wmt-site-content-strategy.scs_production.hp_summary_asset
**Content Type classifier:** CASE WHEN content_served_by='ads' → WMC; CONTAINS(disable_content_personalization,'true') → Merch; legacy WMC conditions → WMC; else → Merch
**Saved to:** wmc_wplus_ost_amend.md + hp_summary_asset.md + HPsummary.md (deprecated)
