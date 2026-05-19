-- WBR Query — All Modules
-- Table  : wmt-site-content-strategy.scs_production.hp_summary_asset  (new authoritative source)
-- Filter : lang_cd = 'English' | excludes moduletype = 'VideoCarousel'
-- Dates  : swap the date literals below or pass dynamically
--
-- Column mapping vs old HPsummary:
--   viewed_impressions  → module_view_count
--   language_split      → lang_cd  ('English')
--   Content_Type        → REMOVED (not in hp_summary_asset)
--   Content_Zone        → content_zone
--   moduleType          → moduletype
--   Carousel_Name       → carousel_name
--
-- Module definitions:
--   HPOV                 : AutoScroll Card 1–5
--   ATF Carousels (SIG)  : SIG Card 1–6, contentzone4–6
--   ATF Carousels        : contentzone3–6, hp_module_type=Carousel (excl. HPOV & SIG)
--   Walmart+ Banner      : hp_module_name='Walmart+ Banner', hp_module_type != 'Utility'
--   Utility              : hp_module_type='Utility'
--   BTF Navigation       : hp_module_type='Navigation', NOT in ATF zones
--   BTF Content          : hp_module_type='Content',    NOT in ATF zones
--   BTF Carousels        : hp_module_type='Carousel',   NOT in ATF zones

WITH current_week AS (
  SELECT
    CASE
      WHEN hp_module_name IN (
        'AutoScroll Card 1','AutoScroll Card 2','AutoScroll Card 3',
        'AutoScroll Card 4','AutoScroll Card 5'
      ) THEN 'HPOV'
      WHEN hp_module_name IN (
        'SIG Card 1','SIG Card 2','SIG Card 3',
        'SIG Card 4','SIG Card 5','SIG Card 6'
      ) AND LOWER(content_zone) IN ('contentzone4','contentzone5','contentzone6')
      THEN 'ATF Carousels (SIG)'
      WHEN LOWER(content_zone) IN ('contentzone3','contentzone4','contentzone5','contentzone6')
        AND hp_module_type = 'Carousel'
      THEN 'ATF Carousels'
      WHEN hp_module_name = 'Walmart+ Banner'
        AND hp_module_type != 'Utility'
      THEN 'Walmart+ Banner'
      WHEN hp_module_type = 'Utility'
      THEN 'Utility'
      WHEN hp_module_type = 'Navigation'
        AND LOWER(content_zone) NOT IN (
          'contentzone1','contentzone2','contentzone3',
          'contentzone4','contentzone5','contentzone6',
          'topcontentzone1','topcontentzone2','topcontentzone3',
          'topcontentzone4','topcontentzone5','topcontentzone6'
        )
      THEN 'BTF Navigation'
      WHEN hp_module_type = 'Content'
        AND LOWER(content_zone) NOT IN (
          'contentzone1','contentzone2','contentzone3',
          'contentzone4','contentzone5','contentzone6',
          'topcontentzone1','topcontentzone2','topcontentzone3',
          'topcontentzone4','topcontentzone5','topcontentzone6'
        )
      THEN 'BTF Content'
      WHEN hp_module_type = 'Carousel'
        AND LOWER(content_zone) NOT IN (
          'contentzone1','contentzone2','contentzone3',
          'contentzone4','contentzone5','contentzone6',
          'topcontentzone1','topcontentzone2','topcontentzone3',
          'topcontentzone4','topcontentzone5','topcontentzone6'
        )
      THEN 'BTF Carousels'
    END AS Module,
    SUM(overall_click_count) AS current_clicks,
    SUM(module_view_count)   AS current_impressions,
    SUM(total_atc_count)     AS current_atc,
    SAFE_DIVIDE(SUM(overall_click_count), SUM(module_view_count)) AS current_ctr
  FROM `wmt-site-content-strategy.scs_production.hp_summary_asset`
  WHERE session_start_dt BETWEEN '2026-04-04' AND '2026-04-07'  -- ← current week
    AND lang_cd = 'English'
    AND COALESCE(moduletype, '') != 'VideoCarousel'
    -- AND experience_lvl2 = 'App: iOS'      -- uncomment for iOS-only
    -- AND experience_lvl2 = 'App: Android'  -- uncomment for Android-only
  GROUP BY Module
  HAVING Module IS NOT NULL
),
previous_week AS (
  SELECT
    CASE
      WHEN hp_module_name IN (
        'AutoScroll Card 1','AutoScroll Card 2','AutoScroll Card 3',
        'AutoScroll Card 4','AutoScroll Card 5'
      ) THEN 'HPOV'
      WHEN hp_module_name IN (
        'SIG Card 1','SIG Card 2','SIG Card 3',
        'SIG Card 4','SIG Card 5','SIG Card 6'
      ) AND LOWER(content_zone) IN ('contentzone4','contentzone5','contentzone6')
      THEN 'ATF Carousels (SIG)'
      WHEN LOWER(content_zone) IN ('contentzone3','contentzone4','contentzone5','contentzone6')
        AND hp_module_type = 'Carousel'
      THEN 'ATF Carousels'
      WHEN hp_module_name = 'Walmart+ Banner'
        AND hp_module_type != 'Utility'
      THEN 'Walmart+ Banner'
      WHEN hp_module_type = 'Utility'
      THEN 'Utility'
      WHEN hp_module_type = 'Navigation'
        AND LOWER(content_zone) NOT IN (
          'contentzone1','contentzone2','contentzone3',
          'contentzone4','contentzone5','contentzone6',
          'topcontentzone1','topcontentzone2','topcontentzone3',
          'topcontentzone4','topcontentzone5','topcontentzone6'
        )
      THEN 'BTF Navigation'
      WHEN hp_module_type = 'Content'
        AND LOWER(content_zone) NOT IN (
          'contentzone1','contentzone2','contentzone3',
          'contentzone4','contentzone5','contentzone6',
          'topcontentzone1','topcontentzone2','topcontentzone3',
          'topcontentzone4','topcontentzone5','topcontentzone6'
        )
      THEN 'BTF Content'
      WHEN hp_module_type = 'Carousel'
        AND LOWER(content_zone) NOT IN (
          'contentzone1','contentzone2','contentzone3',
          'contentzone4','contentzone5','contentzone6',
          'topcontentzone1','topcontentzone2','topcontentzone3',
          'topcontentzone4','topcontentzone5','topcontentzone6'
        )
      THEN 'BTF Carousels'
    END AS Module,
    SUM(overall_click_count) AS prev_clicks,
    SUM(module_view_count)   AS prev_impressions,
    SAFE_DIVIDE(SUM(overall_click_count), SUM(module_view_count)) AS prev_ctr,
    SUM(total_atc_count)     AS prev_atc
  FROM `wmt-site-content-strategy.scs_production.hp_summary_asset`
  WHERE session_start_dt BETWEEN '2026-03-28' AND '2026-03-31'  -- ← prior week
    AND lang_cd = 'English'
    AND COALESCE(moduletype, '') != 'VideoCarousel'
    -- AND experience_lvl2 = 'App: iOS'
    -- AND experience_lvl2 = 'App: Android'
  GROUP BY Module
  HAVING Module IS NOT NULL
),
totals_current AS (
  SELECT
    SUM(current_clicks) AS total_clicks,
    SUM(current_atc)    AS total_atc
  FROM current_week
)
SELECT
  c.Module,
  ROUND(c.current_ctr * 100, 2)                                          AS ctr_pct,
  ROUND((SAFE_DIVIDE(c.current_ctr, p.prev_ctr) - 1) * 100, 1)           AS ctr_wow_pct,
  ROUND(SAFE_DIVIDE(c.current_clicks, t.total_clicks) * 100, 1)           AS clicks_pct,
  ROUND((SAFE_DIVIDE(c.current_clicks, p.prev_clicks) - 1) * 100, 1)      AS clicks_wow_pct,
  ROUND(SAFE_DIVIDE(c.current_atc, t.total_atc) * 100, 1)                 AS atc_pct,
  -- ATC WoW: rate-based (ATCs per impression) — avoids volume bias from partial weeks
  ROUND((SAFE_DIVIDE(
    SAFE_DIVIDE(c.current_atc, c.current_impressions),
    SAFE_DIVIDE(p.prev_atc,   p.prev_impressions)
  ) - 1) * 100, 1)                                                        AS atc_wow_pct
FROM current_week   c
LEFT JOIN previous_week   p ON c.Module = p.Module
CROSS JOIN totals_current t
ORDER BY
  CASE c.Module
    WHEN 'HPOV'                THEN 1
    WHEN 'ATF Carousels (SIG)' THEN 2
    WHEN 'ATF Carousels'       THEN 3
    WHEN 'Walmart+ Banner'     THEN 4
    WHEN 'Utility'             THEN 5
    WHEN 'BTF Navigation'      THEN 6
    WHEN 'BTF Content'         THEN 7
    WHEN 'BTF Carousels'       THEN 8
  END
