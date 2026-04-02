# 📊 Dataset: `HPsummary`

**Project:** `wmt-site-content-strategy`  
**Dataset:** `scs_production`  
**Full Reference:** `wmt-site-content-strategy.scs_production.HPsummary`  
**Keel Role:** The **primary reporting table** for homepage analytics. Richer than `hp_summary_asset` — includes extra date dimensions, activation metrics, and a critical `Content_Type` filter. Powering the Homepage Buddy agent and all HP performance dashboards.

> ⚠️ **CRITICAL MANDATORY FILTER**: Always apply `Content_Type = 'Merch'` — without this, data will be incorrect.

---

## 🧭 What It Represents

One row = one **homepage asset/module** sliced by date, platform, traffic source, and editorial metadata — with full performance metrics and rich date/fiscal dimensions.

This is the **upgraded version of `hp_summary_asset`** with:
- Mandatory `Content_Type` filter for Merch-only data
- More date dimensions (calendar + fiscal month/week/quarter/year)
- Activation columns renamed (e.g., `gmf_activations` instead of `gmf_activation_flag`)
- `language_split` and `Carousel_Name` dimensions

---

## 🚨 Mandatory Filter

```sql
-- ALWAYS include this filter — NEVER remove it
WHERE Content_Type = 'Merch'
```

---

## 📋 Key Columns

### Dimensions

| Column | Description | Sample Values |
|--------|-------------|---------------|
| `session_start_dt` | Primary date column — **use for all date filters** | `2025-01-31`, `2026-03-31` |
| `experience_lvl2` | Platform/device | `App:iOS`, `App:Android`, `Web: Desktop`, `Web: mWeb` |
| `traffic_source_lvl2` | Traffic acquisition channel | `Organic: Direct`, `Paid: SEM`, `Organic: SEO` |
| `hp_module_name` | **Primary module name — use this first for filtering** | `Scrollable Item Grid Card 1`, `AutoScroll Card 1` |
| `hp_module_type` | Module type classification | `Content`, `Commerce` |
| `moduleType` | Detailed technical module type | `PrismHeroCarousel`, `AdjustableBanner` |
| `modulename` | Full module name with dates/zones | `HP Redesign (CZ33): Adjustable Banner...` |
| `Content_Type` | **MANDATORY FILTER COLUMN** | `Merch` (always filter to this) |
| `message_name` | Campaign/message name | `"2025 Fall New And Trending"` |
| `message_id` | Unique message identifier | UUID |
| `message_owner` | Owner team/person | Owner name |
| `message_sponsor` | Sponsoring business unit | `CAMPAIGNS & EVENTS`, `HOME` |
| `message_type` | Message category | `SEASONAL`, `HOLIDAY` |
| `SBU` | Strategic Business Unit | `HOME`, `GROCERY`, `CROSS CATEGORY` |
| `Carousel_Name` | Carousel name if in carousel | `Not Carousel`, or carousel name |
| `Content_Zone` | Content zone on HP | `contentZone33`, `contentZone36` |
| `Module_Group` | High-level module grouping | `Content`, `Commerce` |
| `m0_Nm` → `m4_nm` | Product taxonomy hierarchy (5 levels) | Department → Leaf category |
| `asset_heading` | Display heading text of the asset | `"Luce tu estilo por menos"` |
| `atf_flag` | Above/Below the fold | `ATF`, `BTF` |
| `atf_location` | Specific fold position | `BTF`, `HeroAutoScroll` |
| `Prism_Module` | Prism design system flag | `Not Prism`, `Prism` |
| `default_shown` | Editorial vs personalized | `Default`, `Personalized` |
| `personalized_asset` | Was asset personalized? | `True`, `False` |
| `language_split` | Language of session | `English`, `Spanish` |

### Date Dimensions (Rich — Unique to HPsummary)

| Column | Description |
|--------|-------------|
| `session_start_dt` | Primary date (use for filtering) |
| `cal_month_name` | Calendar month name (e.g., `January`) |
| `cal_month_nbr` | Calendar month number (1–12) |
| `cal_week_nbr` | Calendar week number |
| `cal_week_nbr_mon` | Calendar week starting Monday |
| `cal_qtr_name` | Calendar quarter name (e.g., `Q1`) |
| `cal_qtr_nbr` | Calendar quarter number (1–4) |
| `cal_yr_nbr` | Calendar year |
| `fiscal_week_nbr` | Walmart fiscal week number |
| `fiscal_month_nbr` | Walmart fiscal month number |
| `fiscal_qtr_nbr` | Walmart fiscal quarter number |
| `fiscal_yr_nbr` | Walmart fiscal year number |

### Metrics

| Column | SQL Formula | Description |
|--------|-------------|-------------|
| `viewed_impressions` | `SUM(viewed_impressions)` | Viewable impressions |
| `overall_click_count` | `SUM(overall_click_count)` | **Primary clicks column** (use this for CTR, not `asset_clicks_count`) |
| **CTR** | `SAFE_DIVIDE(SUM(overall_click_count), SUM(viewed_impressions)) * 100` | Click-through rate as % |
| `total_gmv` | `SUM(total_gmv)` | Gross Merchandise Value |
| `total_atc_count` | `SUM(total_atc_count)` | Add to Cart count |
| `gmf_activations` | `SUM(gmf_activations)` | GMF category activations |
| `subs_activations` | `SUM(COALESCE(subs_activations, 0))` | Subscriptions activations |
| `acc_activations` | `SUM(COALESCE(acc_activations, 0))` | Walmart+ account activations |
| `exp_del_activations` | `SUM(exp_del_activations)` | Express delivery activations |
| `rx_activations` | `SUM(rx_activations)` | Pharmacy (Rx) activations |
| **Services Activations** | `SUM(COALESCE(subs_activations,0) + COALESCE(acc_activations,0))` | Combined services activation |
| `all_clicks_count_flag` | Used in Asset Exit Rate | Inclusive click flag |
| `asset_clicks_count` | Used in Asset Exit Rate | Asset-specific clicks |
| **Asset Exit Rate** | `(1 - SAFE_DIVIDE(SUM(all_clicks_count_flag), SUM(asset_clicks_count))) * 100` | % who left without engaging |

---

## 🖥️ Default Platform Filter

```sql
-- DEFAULT: iOS + Android apps only (inform user of this)
AND experience_lvl2 IN ('App:iOS', 'App:Android')

-- If user asks for Desktop: add this
AND experience_lvl2 IN ('App:iOS', 'App:Android', 'Web: Desktop')

-- If user asks for all platforms: remove the filter entirely
```

> ⚠️ Note: Platform values use `App:iOS` (no space) in this table vs `App: iOS` (with space) in other tables!

---

## 🔑 Query Templates

### Basic Metrics Query
```sql
SELECT
    SUM(viewed_impressions) AS impressions,
    SUM(overall_click_count) AS clicks,
    SAFE_DIVIDE(SUM(overall_click_count), SUM(viewed_impressions)) * 100 AS ctr,
    SUM(total_gmv) AS gmv,
    SUM(total_atc_count) AS total_atc
FROM `wmt-site-content-strategy.scs_production.HPsummary`
WHERE Content_Type = 'Merch'  -- MANDATORY
  AND experience_lvl2 IN ('App:iOS', 'App:Android')
  AND session_start_dt BETWEEN '2025-01-01' AND '2025-01-31'
  AND hp_module_name = 'Scrollable Item Grid Card 1'
```

### Daily Trend (for charts)
```sql
SELECT
    session_start_dt AS date,
    SUM(viewed_impressions) AS impressions,
    SUM(overall_click_count) AS clicks,
    SAFE_DIVIDE(SUM(overall_click_count), SUM(viewed_impressions)) * 100 AS ctr,
    SUM(total_gmv) AS gmv
FROM `wmt-site-content-strategy.scs_production.HPsummary`
WHERE Content_Type = 'Merch'
  AND experience_lvl2 IN ('App:iOS', 'App:Android')
  AND session_start_dt BETWEEN '2025-02-01' AND '2025-02-28'
  AND hp_module_name = 'Scrollable Item Grid Card 1'
GROUP BY session_start_dt
ORDER BY session_start_dt
```

### Module Comparison
```sql
SELECT
    hp_module_name,
    SUM(viewed_impressions) AS impressions,
    SUM(overall_click_count) AS clicks,
    SAFE_DIVIDE(SUM(overall_click_count), SUM(viewed_impressions)) * 100 AS ctr,
    SUM(total_gmv) AS gmv,
    SUM(total_atc_count) AS total_atc,
    (1 - SAFE_DIVIDE(SUM(all_clicks_count_flag), SUM(asset_clicks_count))) * 100 AS asset_exit_rate
FROM `wmt-site-content-strategy.scs_production.HPsummary`
WHERE Content_Type = 'Merch'
  AND experience_lvl2 IN ('App:iOS', 'App:Android')
  AND session_start_dt BETWEEN '2025-01-01' AND '2025-01-31'
GROUP BY hp_module_name
ORDER BY impressions DESC
```

### WBR (Weekly Business Review) — WoW Metrics
```sql
SELECT
    fiscal_week_nbr,
    SUM(viewed_impressions) AS impressions,
    SUM(overall_click_count) AS clicks,
    SAFE_DIVIDE(SUM(overall_click_count), SUM(viewed_impressions)) * 100 AS ctr,
    SUM(total_gmv) AS gmv,
    SUM(gmf_activations) AS gmf_activations,
    SUM(COALESCE(subs_activations, 0) + COALESCE(acc_activations, 0)) AS services_activations,
    SUM(exp_del_activations) AS express_delivery_activations
FROM `wmt-site-content-strategy.scs_production.HPsummary`
WHERE Content_Type = 'Merch'
  AND experience_lvl2 IN ('App:iOS', 'App:Android')
  AND session_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
GROUP BY fiscal_week_nbr
ORDER BY fiscal_week_nbr
```

### Fuzzy Module Name Search
```sql
-- Use this when you're not sure of the exact module name
SELECT DISTINCT hp_module_name
FROM `wmt-site-content-strategy.scs_production.HPsummary`
WHERE Content_Type = 'Merch'
  AND hp_module_name LIKE '%Card 1%'
LIMIT 20
```

### Message Performance (for share-out analysis)
```sql
SELECT
    message_name,
    message_sponsor,
    SBU,
    SUM(viewed_impressions) AS impressions,
    SUM(overall_click_count) AS clicks,
    SAFE_DIVIDE(SUM(overall_click_count), SUM(viewed_impressions)) * 100 AS ctr,
    SUM(total_gmv) AS gmv,
    SAFE_DIVIDE(SUM(total_gmv), SUM(viewed_impressions)) * 1000000 AS gmv_per_million_impressions
FROM `wmt-site-content-strategy.scs_production.HPsummary`
WHERE Content_Type = 'Merch'
  AND experience_lvl2 IN ('App:iOS', 'App:Android')
  AND session_start_dt BETWEEN '2026-02-09' AND '2026-02-23'
GROUP BY 1, 2, 3
ORDER BY impressions DESC
```

---

## 📤 Output Formats (Homepage Buddy Pattern)

When users ask for data exports, use these formats:

### Excel File
```python
import pandas as pd
from datetime import datetime
import os

df = pd.DataFrame(data)  # data = query results
os.makedirs(os.path.expanduser('~/Desktop/clickfather'), exist_ok=True)
filename = os.path.expanduser(f'~/Desktop/clickfather/hp_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')
df.to_excel(filename, index=False)
print(f'Saved to {filename}')
```

### PowerPoint Chart (Walmart Blue Styling)
```python
# Walmart Colors
WALMART_BLUE = '#0071CE'
WALMART_YELLOW = '#FFC220'
WALMART_GREEN = '#76C043'
WALMART_RED = '#E31837'

# Save to ~/Desktop/clickfather/hp_chart_YYYYMMDD_HHMMSS.pptx
```

---

## 🔗 Relationships to Other Tables

| Table | Relationship |
|-------|-------------|
| `hp_summary_asset` | Similar grain, older/simpler version. HPsummary is preferred for reporting. Key difference: `overall_click_count` (HPsummary) vs `asset_clicks_count` (hp_summary_asset) |
| `hp_session` | Join for CPTS: `session_start_dt + experience_lvl2 + traffic_source_lvl2` |
| `sov_hp_carousel_content` | Join for SOV context: `message_id + session_start_dt` |
| `item_hp_scs` / `CVPsummary` | Item-level drill-down from module-level HPsummary |

---

## ⚠️ Key Differences vs `hp_summary_asset`

| Feature | `HPsummary` | `hp_summary_asset` |
|---------|-------------|-------------------|
| Mandatory filter | `Content_Type = 'Merch'` | None |
| Primary clicks column | `overall_click_count` | `asset_clicks_count` |
| Activation columns | `gmf_activations`, `subs_activations`, etc. | `gmf_activation_flag`, etc. |
| Date dimensions | Rich (12 date columns) | Basic (4 date columns) |
| Platform values | `App:iOS` (no space) | `App: iOS` (with space) |
| Preferred for | **Reporting, dashboards, WBR** | Raw analysis, joins |

---

*Last updated by Keel Agent | Source: Homepage Buddy agent system prompt analysis*
