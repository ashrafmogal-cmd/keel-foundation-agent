# 📊 Dataset: `item_hp_scs`

**Project:** `wmt-site-content-strategy`  
**Dataset:** `scs_production`  
**Full Reference:** `wmt-site-content-strategy.scs_production.item_hp_scs`  
**Size:** ~685 GB 🔴 **CRITICAL: ALWAYS filter by `event_dt` or query costs will be extreme**  
**Keel Role:** Most granular table — item/product-level engagement data for products shown on the homepage. Used for carousel item-level analysis and product-level GMV attribution.

---

## 🧭 What It Represents

One row = one **individual product (item)** shown in a specific HP module on a specific date and platform.

Used to answer questions like:
- *"Which specific products drove the most clicks in the hero carousel last week?"*
- *"What is the GMV attribution at the product level by category?"*
- *"How do sponsored vs non-sponsored items compare in CTR?"*

---

## 📋 Column Reference

| # | Column | Type | Description | Sample Values |
|---|--------|------|-------------|---------------|
| 1 | `experience_lvl2` | STRING | Platform/device | `App: Android`, `App: iOS`, `Web: Desktop`, `Web: Mobile` |
| 2 | `moduletype` | STRING | Module type containing the item | `PrismHeroCarousel`, `AdjustableBanner` |
| 3 | `modl_nm` | STRING | Full module name | `04/28 (CZ 39) Hero Carousel IOS CC-App` |
| 4 | `modl_zone_nm` | STRING | Content zone for the module | `contentZone34`, `contentZone42` |
| 5 | `prod_nm` | STRING | Product name | Product name or `null` |
| 6 | `rpt_lvl_0_nm` | STRING | Taxonomy level 0 — top-level department | Department name or `null` |
| 7 | `rpt_lvl_1_nm` | STRING | Taxonomy level 1 — category | Category name or `null` |
| 8 | `rpt_lvl_2_nm` | STRING | Taxonomy level 2 — subcategory | Subcategory or `null` |
| 9 | `rpt_lvl_3_nm` | STRING | Taxonomy level 3 — segment | Segment or `null` |
| 10 | `rpt_lvl_4_nm` | STRING | Taxonomy level 4 — most granular item type | Item type or `null` |
| 11 | `prod_class_type_nm` | STRING | Product class type | `null` or class type name |
| 12 | `prod_type_nm` | STRING | Product type name | `null` or type name |
| 13 | `itemid` | STRING | Unique item/product identifier (hashed) | `1A49167C80824E9FAA909D9A11A04986` |
| 14 | `is_sponsored` | STRING | Whether the item placement is sponsored | `0` (not sponsored), `1` (sponsored) |
| 15 | `1p_3p_flag` | STRING | First-party vs third-party seller | `1P`, `3P` |
| 16 | `event_dt` | STRING | Date of the event — **PRIMARY DATE FILTER** | `2025-08-11`, `2026-03-31` |
| 17 | `atc_clicks` | INT | Add-to-cart clicks for this item | numeric or `null` |
| 18 | `clicks` | INT | Total clicks on this item | numeric or `null` |
| 19 | `viewed_impressions` | INT | Times item was viewed | `5`, `16`, `48` |
| 20 | `load_impressions` | INT | Times item was loaded/rendered (incl. not viewed) | `5`, `16`, `48` |
| 21 | `total_gmv` | FLOAT | Revenue attributed to this item | dollar amount or `null` |
| 22 | `all_clicks_count_flag` | INT | All-inclusive click flag | `0`, `1`, `null` |
| 23 | `asset_clicks_count` | INT | Clicks on the asset containing this item | numeric or `null` |

---

## 🔑 Key Derived Metrics

```sql
-- Item-Level CTR
SAFE_DIVIDE(clicks, viewed_impressions) AS item_ctr

-- Item-Level ATC Rate
SAFE_DIVIDE(atc_clicks, viewed_impressions) AS item_atc_rate

-- GMV Per Impression
SAFE_DIVIDE(total_gmv, viewed_impressions) AS gmv_per_impression

-- Viewability Rate (what % of loaded items were actually viewed)
SAFE_DIVIDE(viewed_impressions, load_impressions) AS viewability_rate
```

---

## ⚠️ CRITICAL Cost Warning

> **This table is 685 GB.** A full table scan will cost hundreds of dollars.
> **ALWAYS filter by `event_dt` — no exceptions.**

```sql
-- ✅ SAFE — always use event_dt filter
SELECT
    event_dt,
    experience_lvl2,
    modl_nm,
    rpt_lvl_1_nm AS category,
    SUM(viewed_impressions) AS impressions,
    SUM(clicks) AS clicks,
    SAFE_DIVIDE(SUM(clicks), SUM(viewed_impressions)) AS ctr,
    SUM(atc_clicks) AS total_atc,
    SUM(total_gmv) AS total_gmv
FROM `wmt-site-content-strategy.scs_production.item_hp_scs`
WHERE event_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)  -- ← MANDATORY
GROUP BY 1, 2, 3, 4
ORDER BY total_gmv DESC

-- ✅ Top items by GMV (last 7 days)
SELECT
    event_dt,
    itemid,
    prod_nm,
    rpt_lvl_1_nm AS category,
    is_sponsored,
    `1p_3p_flag`,
    SUM(viewed_impressions) AS impressions,
    SUM(clicks) AS clicks,
    SUM(total_gmv) AS total_gmv
FROM `wmt-site-content-strategy.scs_production.item_hp_scs`
WHERE event_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY 1, 2, 3, 4, 5, 6
ORDER BY total_gmv DESC
LIMIT 100
```

---

## 🔗 Relationships

- **Child of** `sov_hp_carousel_content` and `hp_summary_asset` — rolls up to module-level metrics
- Join with `hp_summary_asset` on `modl_nm + experience_lvl2 + event_dt` for cross-table analysis
- Use `itemid` to join with product catalog tables for enriched product metadata
- `rpt_lvl_*_nm` columns mirror standard Walmart product taxonomy hierarchy

---

## 📦 Common Use Cases

1. **Carousel item-level performance dashboard** — which products in carousels drive most GMV?
2. **1P vs 3P analysis** — how do first-party vs third-party products compare?
3. **Sponsored vs organic item performance** — `is_sponsored = '1'` vs `'0'`
4. **Category-level homepage attribution** — aggregate by `rpt_lvl_1_nm` for department view

---

*Last updated by Keel Agent | Source: BigQuery schema exploration + Confluence HP Analytics 101*
