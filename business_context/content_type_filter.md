# Content_Type Filter — Merch vs WMC

## Overview
When calculating CTR (or any performance metric), always filter to Content_Type = 'Merch' only.
WMC (Walmart Media Connect) = paid ads. Merch = organic site merchandising content.
Mixing WMC and Merch in CTR calculations distorts performance benchmarks.

## Source Formula (Tableau)
```
IF LOWER(IFNULL([Content Served By], '')) = 'ads' THEN 'WMC'
ELSEIF CONTAINS(LOWER(IFNULL([Disable Content Personalization], '')), 'true') THEN 'Merch'
ELSEIF CONTAINS(LOWER(IFNULL([Disable Content Personalization], '')), 'false')
  AND LOWER(IFNULL([Personalized Asset], '')) = 'default'
  AND DATE([Session Start Dt]) <= DATE('2025-03-01')
  AND LOWER(IFNULL([Content Zone], '')) = 'contentzone3'
  AND LOWER(IFNULL([Hp Module Name], '')) IN ('autoscroll card 1','autoscroll card 2','autoscroll card 3')
  THEN 'WMC'
ELSEIF CONTAINS(LOWER(IFNULL([Disable Content Personalization], '')), 'false')
  AND LOWER(IFNULL([Personalized Asset], '')) = 'default'
  AND (
    (LOWER(IFNULL([Content Zone], '')) IN ('contentzone8','contentzone9') AND LOWER(IFNULL([Hp Module Name], '')) = 'adjustable banner small')
    OR
    (LOWER(IFNULL([Content Zone], '')) IN ('contentzone10','contentzone11') AND LOWER(IFNULL([Hp Module Name], '')) = 'triple pack small')
  )
  THEN 'WMC'
ELSE 'Merch'
END
```

## BigQuery SQL Translation

```sql
-- Content_Type CASE expression — use in every CTR/GMV query
-- Then filter: WHERE content_type = 'Merch'

CASE
  -- Rule 1: Explicitly served as ads = WMC
  WHEN LOWER(IFNULL(content_served_by, '')) = 'ads'
    THEN 'WMC'

  -- Rule 2: Personalization disabled = Merch
  WHEN LOWER(IFNULL(disable_content_personalization, '')) LIKE '%true%'
    THEN 'Merch'

  -- Rule 3: Historical WMC condition (pre-Mar 1 2025, contentzone3, AutoScroll Cards 1-3)
  WHEN LOWER(IFNULL(disable_content_personalization, '')) LIKE '%false%'
    AND LOWER(IFNULL(personalized_asset, '')) = 'default'
    AND session_start_dt <= DATE('2025-03-01')
    AND LOWER(IFNULL(content_zone, '')) = 'contentzone3'
    AND LOWER(IFNULL(hp_module_name, '')) IN ('autoscroll card 1', 'autoscroll card 2', 'autoscroll card 3')
    THEN 'WMC'

  -- Rule 4: WMC in specific banner/pack zones
  WHEN LOWER(IFNULL(disable_content_personalization, '')) LIKE '%false%'
    AND LOWER(IFNULL(personalized_asset, '')) = 'default'
    AND (
      (LOWER(IFNULL(content_zone, '')) IN ('contentzone8', 'contentzone9')
        AND LOWER(IFNULL(hp_module_name, '')) = 'adjustable banner small')
      OR
      (LOWER(IFNULL(content_zone, '')) IN ('contentzone10', 'contentzone11')
        AND LOWER(IFNULL(hp_module_name, '')) = 'triple pack small')
    )
    THEN 'WMC'

  -- Default: Everything else = Merch
  ELSE 'Merch'
END AS content_type
```

## Usage Pattern

```sql
-- ALWAYS wrap in a CTE and filter:
WITH base AS (
  SELECT
    *,
    CASE
      WHEN LOWER(IFNULL(content_served_by, '')) = 'ads' THEN 'WMC'
      WHEN LOWER(IFNULL(disable_content_personalization, '')) LIKE '%true%' THEN 'Merch'
      WHEN LOWER(IFNULL(disable_content_personalization, '')) LIKE '%false%'
        AND LOWER(IFNULL(personalized_asset, '')) = 'default'
        AND session_start_dt <= DATE('2025-03-01')
        AND LOWER(IFNULL(content_zone, '')) = 'contentzone3'
        AND LOWER(IFNULL(hp_module_name, '')) IN ('autoscroll card 1','autoscroll card 2','autoscroll card 3')
        THEN 'WMC'
      WHEN LOWER(IFNULL(disable_content_personalization, '')) LIKE '%false%'
        AND LOWER(IFNULL(personalized_asset, '')) = 'default'
        AND (
          (LOWER(IFNULL(content_zone, '')) IN ('contentzone8','contentzone9') AND LOWER(IFNULL(hp_module_name, '')) = 'adjustable banner small')
          OR
          (LOWER(IFNULL(content_zone, '')) IN ('contentzone10','contentzone11') AND LOWER(IFNULL(hp_module_name, '')) = 'triple pack small')
        )
        THEN 'WMC'
      ELSE 'Merch'
    END AS content_type
  FROM `wmt-site-content-strategy.scs_production.hp_summary_asset`
  WHERE session_start_dt BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
    AND experience_lvl2 IN ('App: iOS', 'App: Android')
)
SELECT ...
FROM base
WHERE content_type = 'Merch'
```

## Key Notes
- Rule 3 (historical WMC) only applies for dates <= 2025-03-01. For FY27 queries (2026+), this condition is never true — those rows fall to ELSE = Merch.
- Rule 4 covers WMC ads in adjustable banner small (CZ8/9) and triple pack small (CZ10/11) zones.
- content_served_by = 'ads' is the primary WMC identifier for Cards 2 and 3.
- ALWAYS apply this filter before reporting CTR, GMV, ATC, or any performance metric.
- Columns used: content_served_by, disable_content_personalization, personalized_asset, content_zone, hp_module_name, session_start_dt
