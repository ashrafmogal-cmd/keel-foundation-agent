# 🎨 Dataset: `ecomm_message_asset`

**Project:** `wmt-ecomm-analytics`
**Dataset:** `ecomm_traffic`
**Full Reference:** `wmt-ecomm-analytics.ecomm_traffic.ecomm_message_asset`
**Keel Role:** Creative metadata layer — asset image URLs, headings, and message ownership.
            Joins to `hp_summary_asset` to power visual/creative performance reports.

---

## 🧭 What It Represents

This is the **MMUI message + asset metadata table** — it contains everything about the creative
side of a homepage message: image URLs, headings, CTA text, colors, ownership, status, and dates.

> Think of it as the **creative brief in database form** — one row per asset per day (`event_dt`).

**114 columns total.** Key columns for Keel use:

---

## 📋 Key Columns

| Column | Type | Description |
|--------|------|-------------|
| `event_dt` | STRING | Date the asset was active. **Must `CAST(event_dt AS DATE)` for joins.** |
| `asset_heading` | STRING | Asset headline — **primary JOIN key** to `hp_summary_asset.asset_heading` |
| `asset_image_source` | STRING | **Walmart CDN image URL** (walmartimages.com) — what customers see |
| `figma_asset_image_url` | STRING | Figma S3 rendering URL — design preview |
| `asset_name` | STRING | Structured: `[id]-[SBU]-[campaign]-[platform]-[format]-[timestamp]` |
| `asset_id` | STRING | Unique asset identifier |
| `message_name` | STRING | Parent message name — links to `hp_summary_asset.message_name` |
| `message_id` | STRING | Unique message identifier |
| `message_owner` | STRING | Message owner name |
| `message_sponsor` | STRING | Sponsoring team/brand |
| `asset_subheading` | STRING | Secondary headline text |
| `asset_cta` | STRING | Call-to-action button text |
| `asset_background_color` | STRING | Background color hex |
| `asset_status` | STRING | Active / Inactive / Draft |
| `planned_start_date` | DATE | Planned campaign start |
| `planned_end_date` | DATE | Planned campaign end |

---

## 🔗 How to Join with `hp_summary_asset`

```sql
-- Standard join to get image URLs alongside performance data
WITH imgs AS (
  SELECT
    CAST(event_dt AS DATE) AS event_date,
    asset_heading,
    asset_image_source,
    figma_asset_image_url,
    asset_name,
    message_name,
    -- Deduplicate: one image per asset_heading per day
    -- Prefer mobile small banner format for App analysis
    ROW_NUMBER() OVER (
      PARTITION BY LOWER(asset_heading), event_dt
      ORDER BY
        CASE WHEN asset_name LIKE '%-M-AdjBn-Sm-%' THEN 1 ELSE 2 END,
        asset_name
    ) AS rn
  FROM `wmt-ecomm-analytics.ecomm_traffic.ecomm_message_asset`
  WHERE event_dt BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
    AND asset_image_source IS NOT NULL
)
SELECT
  p.session_start_dt,
  p.message_name,
  p.asset_heading,
  p.hp_module_name,
  SUM(p.module_view_count)  AS impressions,
  SUM(p.overall_click_count) AS clicks,
  SAFE_DIVIDE(SUM(p.overall_click_count), SUM(p.module_view_count)) AS ctr,
  MAX(i.asset_image_source)   AS image_url,
  MAX(i.figma_asset_image_url) AS figma_url
FROM `wmt-site-content-strategy.scs_production.hp_summary_asset` p
LEFT JOIN imgs i
  ON LOWER(p.asset_heading) = LOWER(i.asset_heading)
  AND p.session_start_dt   = i.event_date
  AND i.rn = 1
WHERE p.session_start_dt BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
  AND p.experience_lvl2 IN ('App: iOS', 'App: Android')
GROUP BY 1, 2, 3, 4
ORDER BY impressions DESC
```

---

## ⚠️ Gotchas

| Issue | Detail |
|-------|--------|
| `event_dt` is STRING | Always `CAST(event_dt AS DATE)` before joining to DATE columns |
| Fan-out on join | Multiple assets share same `asset_heading` per day — always deduplicate with `ROW_NUMBER()` |
| Some rows have null images | Filter `WHERE asset_image_source IS NOT NULL` in the CTE |
| Generic headings | Headings like "Mother's Day gifts" are shared across multiple messages — tighter join using `message_name + asset_heading` improves precision |

---

## 💡 Use Cases

1. **Visual performance reports** — HTML reports with asset images + CTR/GMV side by side
2. **Creative analysis** — Which asset design drove the best CTR?
3. **Asset metadata lookup** — Who owns this message? What is the CTA text? What's the planned run date?
4. **Figma design review** — Link directly to Figma renders from performance data

---

*Added by Keel Agent — sourced from BigQuery schema exploration*
