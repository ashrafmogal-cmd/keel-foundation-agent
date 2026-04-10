# Message Engagement Benchmarking Framework
**Implemented:** April 2026 | **Source:** Tableau → BigQuery SQL translation
**Author:** Keel Agent (keel-efa1e7)

---

## Overview

This framework classifies every HPOV message as **High Engagement**, **Avg Engagement**, or **Trailing Engagement** based on how its actual CTR compares to a dynamically computed, impressions-weighted benchmark CTR. The benchmark is "fair" — it accounts for WHERE (which card, which platform) the message actually ran, not a flat HPOV average.

## Engagement Tiers

| Tier | Benchmark Index | Color | Meaning |
|------|----------------|-------|---------|
| 🟢 **High Engagement** | ≥ 1.3 | Green | Outperforming benchmark by 30%+ |
| 🟡 **Avg Engagement** | ≥ 0.7 and < 1.3 | Orange | Within 30% of benchmark (either direction) |
| 🔴 **Trailing Engagement** | < 0.7 | Red | Underperforming benchmark by 30%+ |

**Benchmark Index** = `Message CTR Raw / Final Weighted Benchmark CTR`

---

## Logic Chain (Translated from Tableau LOD → BigQuery SQL)

### Step 1 — Message Clicks & Impressions
**Tableau:** `{ FIXED [Message Name], [Platform], [Module Type] : SUM([overall_click_count]) }`
**SQL equivalent:** Aggregate `asset_clicks_count` and `module_view_count` grouped by `(message_name, experience_lvl2, moduletype, hp_module_name)`
- Uses `COALESCE(asset_clicks_count, 0)` to handle null click rows

### Step 2 — Message CTR Raw
**Formula:** `SUM(message_clicks) / SUM(message_impressions)`
**SQL:** `SAFE_DIVIDE(SUM(asset_clicks_count), SUM(module_view_count))`
- This is the actual achieved CTR for the message at each platform × card location

### Step 3 — Location Benchmark CTR
**Tableau:** `{ FIXED [Platform], [Module Type] : SUM(clicks) / SUM(impressions) }`
**SQL:** Group by `(experience_lvl2, moduletype, hp_module_name)` — aggregate ALL messages
- Produces benchmark at `hp_module_name` grain (Card 1, Card 2, Card 3, Card 4, Card 5) per platform
- **KEY DESIGN DECISION:** Using `hp_module_name` (not just `moduletype`) gives card-specific benchmarks.
  A message on Card 3 (lower-traffic, lower benchmark) won't be unfairly judged by Card 1's benchmark.
- **IMPORTANT:** This benchmark is DATA-DRIVEN from the selected date range — it reflects the actual period performance, not pre-set static benchmarks. More responsive to seasonality.

### Step 4 — Total Message Impressions
**Tableau:** `{ FIXED [Message Name] : SUM([Message Impressions]) }`
**SQL:** Group by `message_name` only — sum across all platforms + all cards
- Denominator for the weighted average benchmark calculation

### Step 5 — Final Weighted Benchmark CTR
**Tableau:** `SUM([Location Benchmark CTR] * [Message Impressions]) / MAX([Total Message Impressions])`
**Formula:**
```
Weighted Benchmark = SUM(location_benchmark_ctr × impressions_at_this_location) / total_impressions_for_message
```
**Example:**
- Message ran 70% on Card 1 iOS (data-driven benchmark: 0.18%) + 30% on Card 3 Android (benchmark: 0.12%)
- Weighted benchmark = (0.18 × 0.70) + (0.12 × 0.30) = 0.162%
- **NOT** a flat HPOV average — the benchmark reflects the actual card/platform distribution of the message

### Step 6 — Benchmark Index & Tier Classification
```sql
benchmark_index = SAFE_DIVIDE(msg_ctr_raw, final_weighted_benchmark_ctr)

engagement_ranking = CASE
  WHEN benchmark_index >= 1.3 THEN 'High Engagement'
  WHEN benchmark_index >= 0.7 THEN 'Avg Engagement'
  WHEN benchmark_index <  0.7 THEN 'Trailing Engagement'
  ELSE 'Unclassified'
END
```

---

## The Canonical SQL Query

**Table:** `wmt-site-content-strategy.scs_production.hp_summary_asset`
**Scope:** HPOV only (`moduletype = 'PrismAdjustableCardCarousel'`)
**Platform:** `experience_lvl2 IN ('App: iOS', 'App: Android')`
**Date:** Dynamic — replace `DATE('YYYY-MM-DD')` values based on user's question
**Output:** Top 10 messages by impressions with engagement tier

```sql
-- ============================================================
-- KEEL: HPOV MESSAGE ENGAGEMENT RANKING
-- Translated from Tableau LOD expressions → BigQuery SQL
-- Table: hp_summary_asset | Scope: HPOV (PrismAdjustableCardCarousel)
-- Platform: iOS + Android | Date: DYNAMIC (replace dates below)
-- ============================================================

WITH

-- ── STEP 1: BASE DATA ────────────────────────────────────────
base AS (
  SELECT
    experience_lvl2,
    moduletype,
    hp_module_name,
    message_name,
    SUM(module_view_count)                AS impressions,
    SUM(COALESCE(asset_clicks_count, 0))  AS clicks
  FROM `wmt-site-content-strategy.scs_production.hp_summary_asset`
  WHERE session_start_dt BETWEEN DATE('{{START_DATE}}') AND DATE('{{END_DATE}}')
    AND moduletype      = 'PrismAdjustableCardCarousel'
    AND experience_lvl2 IN ('App: iOS', 'App: Android')
    AND message_name    IS NOT NULL
  GROUP BY 1, 2, 3, 4
),

-- ── STEP 2: MESSAGE METRICS ───────────────────────────────────
-- Tableau: { FIXED [Message Name], [Platform], [Module Type] : SUM(clicks/impressions) }
message_metrics AS (
  SELECT
    message_name,
    experience_lvl2,
    moduletype,
    hp_module_name,
    SUM(impressions)                                  AS msg_impressions,
    SUM(clicks)                                       AS msg_clicks,
    SAFE_DIVIDE(SUM(clicks), SUM(impressions))        AS msg_ctr_raw
  FROM base
  GROUP BY 1, 2, 3, 4
),

-- ── STEP 3: LOCATION BENCHMARK CTR ───────────────────────────
-- Tableau: { FIXED [Platform], [Module Type] : SUM(clicks) / SUM(impressions) }
-- Card-specific benchmarks per platform (Card 1 iOS, Card 2 iOS, etc.)
location_benchmark AS (
  SELECT
    experience_lvl2,
    moduletype,
    hp_module_name,
    SAFE_DIVIDE(SUM(clicks), SUM(impressions))        AS location_benchmark_ctr
  FROM base
  GROUP BY 1, 2, 3
),

-- ── STEP 4: TOTAL MESSAGE IMPRESSIONS ────────────────────────
-- Tableau: { FIXED [Message Name] : SUM([Message Impressions]) }
total_msg_impressions AS (
  SELECT
    message_name,
    SUM(impressions)                                  AS total_msg_imp
  FROM base
  GROUP BY 1
),

-- ── STEP 5: JOIN — Attach benchmark to each message location ──
message_with_benchmark AS (
  SELECT
    mm.message_name,
    mm.experience_lvl2,
    mm.hp_module_name,
    mm.msg_impressions,
    mm.msg_clicks,
    mm.msg_ctr_raw,
    lb.location_benchmark_ctr,
    tmi.total_msg_imp,
    lb.location_benchmark_ctr * mm.msg_impressions   AS weighted_bench_contribution
  FROM message_metrics mm
  JOIN location_benchmark lb
    ON  mm.experience_lvl2 = lb.experience_lvl2
    AND mm.moduletype      = lb.moduletype
    AND mm.hp_module_name  = lb.hp_module_name
  JOIN total_msg_impressions tmi
    ON  mm.message_name    = tmi.message_name
),

-- ── STEP 6: COLLAPSE TO MESSAGE LEVEL ────────────────────────
-- Tableau: SUM([Location Benchmark CTR] * [Message Impressions]) / MAX([Total Message Impressions])
message_final AS (
  SELECT
    message_name,
    SUM(msg_impressions)                              AS total_impressions,
    SUM(msg_clicks)                                   AS total_clicks,
    SAFE_DIVIDE(SUM(msg_clicks), SUM(msg_impressions)) AS msg_ctr_raw,
    SAFE_DIVIDE(
      SUM(weighted_bench_contribution),
      MAX(total_msg_imp)
    )                                                 AS final_weighted_benchmark_ctr
  FROM message_with_benchmark
  GROUP BY 1
),

-- ── STEP 7: BENCHMARK INDEX + ENGAGEMENT TIER ────────────────
classified AS (
  SELECT
    message_name,
    total_impressions,
    total_clicks,
    ROUND(msg_ctr_raw * 100, 4)                       AS msg_ctr_pct,
    ROUND(final_weighted_benchmark_ctr * 100, 4)      AS weighted_benchmark_ctr_pct,
    ROUND(
      SAFE_DIVIDE(msg_ctr_raw, final_weighted_benchmark_ctr),
      3
    )                                                 AS benchmark_index,
    CASE
      WHEN SAFE_DIVIDE(msg_ctr_raw, final_weighted_benchmark_ctr) >= 1.3
        THEN 'High Engagement'
      WHEN SAFE_DIVIDE(msg_ctr_raw, final_weighted_benchmark_ctr) >= 0.7
        THEN 'Avg Engagement'
      WHEN SAFE_DIVIDE(msg_ctr_raw, final_weighted_benchmark_ctr) <  0.7
        THEN 'Trailing Engagement'
      ELSE 'Unclassified'
    END                                               AS engagement_ranking
  FROM message_final
)

-- ── FINAL OUTPUT: Top 10 by Impressions ──────────────────────
SELECT
  ROW_NUMBER() OVER (ORDER BY total_impressions DESC)   AS rank,
  message_name,
  total_impressions,
  total_clicks,
  CONCAT(CAST(msg_ctr_pct AS STRING), '%')              AS msg_ctr,
  CONCAT(CAST(weighted_benchmark_ctr_pct AS STRING), '%') AS weighted_benchmark_ctr,
  benchmark_index,
  engagement_ranking
FROM classified
ORDER BY total_impressions DESC   -- ORDER BY NUMERIC (not formatted string)
LIMIT 10
```

---

## Key Design Decisions & Gotchas

### ✅ Why weighted benchmark (not flat HPOV average)?
A message running mostly on Card 3 (lower average CTR) should NOT be compared to the Card 1 benchmark. The weighted approach makes the comparison fair by reflecting where each message actually appeared.

### ✅ Why hp_module_name vs moduletype for benchmark grain?
`moduletype = 'PrismAdjustableCardCarousel'` is constant for all HPOV. If we benchmarked at moduletype level only, ALL cards would share one flat benchmark. Using `hp_module_name` creates 5 separate benchmarks (one per card × platform), which is the correct design.

### ✅ Why data-driven benchmark (not pre-set card benchmarks)?
The benchmark is computed from actual data in the user's selected date range. This adapts to seasonality — during a high-traffic event week, all messages may perform higher, and the benchmark adjusts accordingly. Pre-set benchmarks (0.23%, 0.15% etc.) are directional guides but not the right denominator for relative ranking.

### ⚠️ Bug that was fixed: ORDER BY on string column
Original query aliased `total_impressions` to a formatted string using `FORMAT('%\'d', ...)`, then tried to `ORDER BY total_impressions DESC`. String comparison made "98" > "10,000,000" lexicographically, returning lowest-impression messages first. Fix: keep `total_impressions` as numeric for the `ORDER BY`, only format for display if needed.

### ⚠️ Null message_name rows
hp_summary_asset contains rows where `message_name IS NULL` (typically 1 row per card × platform combination). These must be filtered out with `AND message_name IS NOT NULL` in the base CTE. Without this filter, a "null message" would appear in the results and distort the benchmark.

### ⚠️ Null asset_clicks_count rows
Some rows in hp_summary_asset have `asset_clicks_count = NULL`. Use `COALESCE(asset_clicks_count, 0)` in the base CTE to treat these as zero clicks rather than propagating NULLs through CTR calculations.

---

## Look-Ahead Workflow (Coming Soon)

**Purpose:** Proactively identify trailing messages that are scheduled to continue running next week.

**Workflow:**
1. User provides a look-ahead doc (Excel/SharePoint) listing messages scheduled for HPOV next week
2. Keel queries BigQuery using the engagement ranking SQL above for the current week's date range
3. Keel cross-references: which of the live messages are classified as Trailing Engagement?
4. Keel surfaces the top trailing messages that are continuing and recommends specific optimization actions

**Optimization Actions for Trailing Messages:**
- 🎨 **Creative refresh** — new image, updated headline, seasonal angle
- 📉 **SOV reduction** — reduce impression allocation, shift SOV to high-performing messages
- 🔄 **Card swap** — move message to a different card (e.g., Card 5 for lifestyle/aspirational content)
- 🎯 **Persona targeting adjustment** — expand or narrow audience targeting; try different persona signals
- 📆 **Takedown / retirement** — if no strategic reason to maintain, remove from HPOV rotation
- 🔗 **Landing page audit** — verify the click destination is relevant and converting (low CTR may be creative; low ATC may be landing page)

**Sample question pattern:**
> "What are the top 2 trailing messages on HPOV that will continue next week and what can we do to optimize them?"

**Keel workflow for that question:**
1. Run engagement ranking SQL for current week date range
2. Filter to `engagement_ranking = 'Trailing Engagement'`
3. Check look-ahead doc for messages continuing next week
4. Cross-reference → find trailing messages that overlap with next week's schedule
5. For each: surface benchmark index, CTR vs benchmark, card position, SOV context
6. Recommend optimization action from playbook above

---

## Sample Output Format

Matches the Tableau screenshot layout:

| Rank | Message Name | Total Impressions | CTR | Weighted Benchmark CTR | Benchmark Index | Engagement Ranking |
|------|-------------|-------------------|-----|----------------------|-----------------|-------------------|
| 1 | 2026 Spring New And Trending | 56,660,206 | 0.2306% | 0.15% | 1.537 | 🟢 High Engagement |
| 2 | Resold At Walmart | 112,306,245 | 0.0768% | 0.0875% | 0.878 | 🟡 Avg Engagement |
| 3 | Apple Macbook M2 Shop Now | 65,327,601 | 0.0846% | 0.1267% | 0.668 | 🔴 Trailing Engagement |

---

## Related Files
- `business_context/reporting_conventions.md` — HPOV module name mappings
- `business_context/message_tiering.md` — tier framework (Tier 1/2/3)
- `business_context/msp_training.md` — message management workflow
- `datasets/hp_summary_asset.md` — full schema reference
