# 📊 Dataset: `CVPsummary`

**Project:** `wmt-site-content-strategy`  
**Dataset:** `scs_production`  
**Full Reference:** `wmt-site-content-strategy.scs_production.CVPsummary`  
**Size:** ~812 GB per partial scan 🔴🔴 **CRITICAL: ALWAYS filter by `event_dt` — this is a 2.32 BILLION row table**  
**Keel Role:** Customer Value Proposition SKU-level performance. Tracks whether CVP-designated items shown on the homepage met their value proposition criteria. Essentially `item_hp_scs` + 3 CVP program indicator columns.

---

## 🧭 What It Represents

One row = one **item/SKU** shown in a specific homepage module on a specific date and platform, enriched with CVP program enrollment and outcome flags.

The **CVP program funnel**:
```
CV_Focus_SKU_IND = 1  →  Is this SKU in the CVP program?
        ↓
trnsctbl_ind = 1       →  Is it actually purchasable on HP?
        ↓
cvp_met_ind = 1        →  Did it meet the CVP criteria? (the outcome metric)
```

~1.07B rows are CVP-enrolled SKUs, of which only ~374M (~35%) actually met the CVP bar.

---

## 📋 Column Reference

| # | Column | Type | Description | Sample Values |
|---|--------|------|-------------|---------------|
| 1 | `experience_lvl2` | STRING | Platform/device | `App: iOS`, `App: Android` |
| 2 | `moduletype` | STRING | Prism module type | `PrismHeroCarousel`, `PrismScrollableItemGrid` |
| 3 | `modl_nm` | STRING | Module/campaign name | `04/28 (CZ 39) Hero Carousel IOS CC-App` |
| 4 | `modl_zone_nm` | STRING | Content zone placement | `contentZone24`, `contentZone42` |
| 5 | `prod_nm` | STRING | Product name | Product name or `null` |
| 6 | `rpt_lvl_0_nm` | STRING | Taxonomy level 0 — division | Division or `null` |
| 7 | `rpt_lvl_1_nm` | STRING | Taxonomy level 1 — department | Department or `null` |
| 8 | `rpt_lvl_2_nm` | STRING | Taxonomy level 2 — category | Category or `null` |
| 9 | `rpt_lvl_3_nm` | STRING | Taxonomy level 3 — subcategory | Subcategory or `null` |
| 10 | `rpt_lvl_4_nm` | STRING | Taxonomy level 4 — leaf/item type | Item type or `null` |
| 11 | `prod_class_type_nm` | STRING | Product class type | `Apparel`, `null` |
| 12 | `prod_type_nm` | STRING | Product type | `Sandals`, `null` |
| 13 | `itemid` | STRING | Item/SKU identifier — can be numeric ID or hex hash | `2769707461` or `8D4D35CF...` |
| 14 | `is_sponsored` | STRING | Sponsored placement flag | `0` (organic), `1` (sponsored) |
| 15 | `1p_3p_flag` | STRING | First-party vs third-party seller | `1P`, `3P`, `NA` |
| 16 | `event_dt` | STRING | Event date — **PRIMARY DATE FILTER (MANDATORY)** | `2025-08-05`, `2026-03-31` |
| 17 | `atc_clicks` | INTEGER | Add-to-cart clicks for this item | numeric or `null` |
| 18 | `clicks` | INTEGER | Total clicks on this item | numeric or `null` |
| 19 | `viewed_impressions` | INTEGER | Times item was viewed (in-viewport) | `1`, `2`, `63` |
| 20 | `load_impressions` | INTEGER | Times item was loaded/rendered | `1`, `2`, `63` |
| 21 | `total_gmv` | FLOAT | Revenue attributed to this item | dollar amount or `null` |
| 22 | `all_clicks_count_flag` | INTEGER | All-inclusive click count flag | `null` or count |
| 23 | `asset_clicks_count` | INTEGER | Clicks on the containing asset | `null` or count |
| 24 | `fiscal_week` | STRING | Walmart fiscal week | `W-31`, `W-42`, `W-03` |
| 25 | `cvp_met_ind` | INTEGER | **CVP MET — Did the SKU meet CVP criteria?** 1=yes, 0=no, null=not a CVP SKU | `1`, `0`, `null` |
| 26 | `trnsctbl_ind` | INTEGER | **Transactable — Can the item be purchased on HP?** 1=yes, 0=no | `1`, `0` |
| 27 | `CV_Focus_SKU_IND` | INTEGER | **CVP Focus SKU — Is this SKU in the CVP program?** 1=yes, 0=no | `1`, `0`, `null` |

---

## 🎯 The Three CVP Indicator Columns Explained

| Column | Meaning | Count |
|--------|---------|-------|
| `CV_Focus_SKU_IND = 1` | SKU is **enrolled** in the CVP program | ~1.07B rows |
| `trnsctbl_ind = 1` | SKU is **purchasable** on the homepage | ~1.06B rows |
| `cvp_met_ind = 1` | SKU **met the CVP bar** — the success metric | ~374M rows (~35% pass rate) |

---

## 📊 Table Stats

| Metric | Value |
|--------|-------|
| **Total Rows** | **2.32 Billion** 🤯 |
| **Date Range** | Aug 2025 → Mar 2026 (8 months) |
| **Distinct Dates** | 243 |
| **Distinct Fiscal Weeks** | 36 |
| **Platform Split** | iOS ~53%, Android ~38%, other ~9% |
| **Seller Split** | 3P ~41%, NA ~32%, 1P ~27% |

---

## 🔑 Key Queries

```sql
-- ✅ CVP Performance by Category (ALWAYS filter event_dt first!)
SELECT
    event_dt,
    rpt_lvl_1_nm AS category,
    COUNT(DISTINCT itemid) AS unique_skus,
    SUM(CASE WHEN CV_Focus_SKU_IND = 1 THEN 1 ELSE 0 END) AS cvp_enrolled_rows,
    SUM(CASE WHEN cvp_met_ind = 1 THEN 1 ELSE 0 END) AS cvp_met_rows,
    SAFE_DIVIDE(
        SUM(CASE WHEN cvp_met_ind = 1 THEN 1 ELSE 0 END),
        SUM(CASE WHEN CV_Focus_SKU_IND = 1 THEN 1 ELSE 0 END)
    ) AS cvp_pass_rate,
    SUM(viewed_impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    SAFE_DIVIDE(SUM(clicks), SUM(viewed_impressions)) AS ctr,
    SUM(total_gmv) AS total_gmv
FROM `wmt-site-content-strategy.scs_production.CVPsummary`
WHERE event_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)  -- MANDATORY
  AND CV_Focus_SKU_IND = 1
GROUP BY 1, 2
ORDER BY event_dt DESC, cvp_pass_rate DESC

-- ✅ CVP vs Non-CVP Performance Comparison
SELECT
    CASE WHEN CV_Focus_SKU_IND = 1 THEN 'CVP SKU' ELSE 'Non-CVP' END AS sku_type,
    CASE WHEN cvp_met_ind = 1 THEN 'CVP Met' 
         WHEN CV_Focus_SKU_IND = 1 THEN 'CVP Not Met' 
         ELSE 'Non-CVP' END AS cvp_status,
    SUM(viewed_impressions) AS impressions,
    SUM(clicks) AS clicks,
    SAFE_DIVIDE(SUM(clicks), SUM(viewed_impressions)) AS ctr,
    SUM(atc_clicks) AS atc,
    SUM(total_gmv) AS gmv
FROM `wmt-site-content-strategy.scs_production.CVPsummary`
WHERE event_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY 1, 2

-- ✅ CVP Pass Rate by Fiscal Week (WoW trend)
SELECT
    fiscal_week,
    SUM(CASE WHEN CV_Focus_SKU_IND = 1 THEN viewed_impressions ELSE 0 END) AS cvp_enrolled_impressions,
    SUM(CASE WHEN cvp_met_ind = 1 THEN viewed_impressions ELSE 0 END) AS cvp_met_impressions,
    SAFE_DIVIDE(
        SUM(CASE WHEN cvp_met_ind = 1 THEN viewed_impressions ELSE 0 END),
        SUM(CASE WHEN CV_Focus_SKU_IND = 1 THEN viewed_impressions ELSE 0 END)
    ) AS impression_weighted_pass_rate
FROM `wmt-site-content-strategy.scs_production.CVPsummary`
WHERE event_dt >= '2025-08-01'
GROUP BY 1
ORDER BY fiscal_week

-- ✅ Top CVP SKUs by GMV (last 7 days)
SELECT
    event_dt,
    itemid,
    prod_nm,
    rpt_lvl_1_nm AS category,
    cvp_met_ind,
    is_sponsored,
    `1p_3p_flag`,
    SUM(viewed_impressions) AS impressions,
    SUM(clicks) AS clicks,
    SUM(total_gmv) AS gmv
FROM `wmt-site-content-strategy.scs_production.CVPsummary`
WHERE event_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  AND CV_Focus_SKU_IND = 1
  AND cvp_met_ind = 1
GROUP BY 1, 2, 3, 4, 5, 6, 7
ORDER BY gmv DESC
LIMIT 100
```

---

## ⚠️ CRITICAL Cost & Query Rules

> **This table has 2.32 BILLION rows and ~812 GB per partial scan.**  
> A full table scan could cost **hundreds of dollars**. Non-negotiable: always filter `event_dt`.

```sql
-- ❌ NEVER do this
SELECT * FROM `wmt-site-content-strategy.scs_production.CVPsummary`

-- ✅ ALWAYS do this
WHERE event_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
-- OR for fiscal week:
WHERE fiscal_week = 'W-42'
```

---

## ⚠️ Data Quality Gotchas

| Issue | Impact |
|-------|--------|
| `event_dt` is **STRING** (not DATE) | Must cast: `CAST(event_dt AS DATE)` for date math |
| `itemid` can be **numeric string** OR **hex hash** | Hex hashes are non-product content. Filter: `WHERE LENGTH(itemid) < 15` for real SKUs |
| `rpt_lvl_*_nm` columns are **heavily null** | Many module rows have no taxonomy. Use IS NOT NULL when doing category analysis |
| `fiscal_week` format is **`W-NN`** | e.g. `W-31`, `W-42` — not a standard date format |
| `null` vs `0` in CVP columns | `null` = not evaluated/not a CVP SKU; `0` = evaluated but did not meet criteria |

---

## 🔗 Relationships to Other Tables

| Table | Join Keys | Purpose |
|-------|-----------|---------|
| **`item_hp_scs`** | `experience_lvl2`, `moduletype`, `modl_nm`, `modl_zone_nm`, `itemid`, `event_dt` | Near-identical schema. CVPsummary = item_hp_scs + 3 CVP columns + `fiscal_week` |
| **`hp_summary_asset`** | `experience_lvl2`, `moduletype`, `CAST(event_dt AS DATE)` = `session_start_dt` | Module-level rollup. Bridge via moduletype for asset-level context |
| **`sov_hp_carousel_content`** | `experience_lvl2`, `moduletype`, `1p_3p_flag`, `is_sponsored`, `CAST(event_dt AS DATE)` | Add SOV/slot context to CVP item analysis |
| **`hp_session`** | `experience_lvl2`, `CAST(event_dt AS DATE)` = `DATE(session_start_dt)` | Session normalization for CPTS |

---

## 💡 Business Use Cases

1. **CVP Program Health** — What % of CVP-enrolled SKUs are actually meeting the bar? (Pass rate = ~35%)
2. **Category CVP Performance** — Which product categories have the highest CVP pass rates?
3. **1P vs 3P CVP** — Do first-party SKUs meet CVP at a higher rate than third-party?
4. **Module-level CVP** — Which homepage modules (Hero Carousel vs SIG) deliver better CVP outcomes?
5. **Sponsored vs Organic CVP** — Does paid placement correlate with CVP success?
6. **Week-over-Week CVP Trend** — Is the program improving over time?

---

*Last updated by Keel Agent | Source: BigQuery schema exploration + row count analysis*
