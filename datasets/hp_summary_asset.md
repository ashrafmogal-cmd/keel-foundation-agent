# 📊 Dataset: `hp_summary_asset` — PRIMARY DASHBOARD TABLE ✅

**Project:** `wmt-site-content-strategy`  
**Dataset:** `scs_production`  
**Full Reference:** `wmt-site-content-strategy.scs_production.hp_summary_asset`  
**Size:** ~53.4 GB ⚠️  
**Status:** ✅ **ACTIVE — This is the table powering the live HP dashboards (WBR, HP Performance, Module Performance, Bubble Charts, Bar Charts). Always prefer this over HPsummary.**  
**Keel Role:** Primary asset-level performance table — the main source for CTR, ATC, GMV, and activation metrics by homepage module.

---

## 🧭 What It Represents

One row = one **homepage asset/module** sliced by:
- Date (`session_start_dt`)
- Platform (`experience_lvl2`)
- Traffic source (`traffic_source_lvl2`)
- Editorial metadata (message, content zone, module type, etc.)
- Performance metrics (impressions, clicks, ATC, GMV, activations)

---

## 📋 Column Reference

| # | Column | Type | Description | Sample Values |
|---|--------|------|-------------|---------------|
| 1 | `wm_wk_of_year` | INT | Walmart fiscal week number | `9`, `14`, `52` |
| 2 | `cal_wk_of_year` | INT | Calendar week of year | `14`, `30` |
| 3 | `cal_mth_beg_dt` | STRING | Calendar month start date | `2026-03-01` |
| 4 | `session_start_dt` | DATE | Session date — **use this as your primary date filter** | `2026-03-31` |
| 5 | `experience_lvl2` | STRING | Platform/device experience | `App: iOS`, `App: Android`, `Web: Desktop`, `Web: Mobile` |
| 6 | `traffic_source_lvl2` | STRING | How the user arrived | `Organic: Direct`, `Paid: SEM`, `Organic: SEO` |
| 7 | `tenant_ste_cd` | STRING | Tenant/site identifier | `US_GLASS_IOS`, `US_GLASS_ANDROID`, `US_GLASS_CORESITE` |
| 8 | `lang_cd` | STRING | Language of the session | `English`, `Spanish` |
| 9 | `message_id` | STRING | Unique ID for the content message | UUID or `NA` |
| 10 | `modulename` | STRING | Full name/label of the HP module | `HP Redesign (CZ33): Adjustable Banner...` |
| 11 | `moduletype` | STRING | Technical type of the module | `AdjustableBanner`, `PrismHeroCarousel` |
| 12 | `content_zone` | STRING | Content zone on the homepage. **ATF = contentZone1 through contentZone6. BTF = contentZone7+.** Use this for ATF/BTF filtering — NOT atf_flag. | `contentZone1` through `contentZone80` |
| 13 | `container_id` | STRING | Container ID within content zone | `NA` or specific container ID |
| 14 | `content_served_by` | STRING | Serving engine | `cxtools` (editorial), `p13n` (personalization), `NA` |
| 15 | `asset_heading` | STRING | Display heading text of the asset | `"Luce tu estilo por menos"` |
| 16 | `asset_display_order` | INT | Position/order the asset appeared | `1`, `2`, `null` |
| 17 | `disable_content_personalization` | STRING | Was personalization disabled? | `NA`, `True`, `False` |
| 18 | `personalized_asset` | STRING | Was this asset personalized? | `Missing Info`, `True`, `False` |
| 19 | `message_name` | STRING | Human-readable name for the campaign/message | `"2025 Fall New And Trending"` |
| 20 | `message_type` | STRING | Category of message | `SEASONAL`, `HOLIDAY`, `null` |
| 21 | `message_sponsor` | STRING | Business unit sponsoring the message | `CAMPAIGNS & EVENTS`, `HOME` |
| 22 | `sbu` | STRING | Strategic Business Unit | `OTHER`, `HOME`, `GROCERY`, `CROSS CATEGORY` |
| 23 | `message_owner` | STRING | Owner team/person for the message | `null` or owner name |
| 24 | `m0_nm` | STRING | Product taxonomy level 0 (top) | Department name |
| 25 | `m1_nm` | STRING | Product taxonomy level 1 | Category name |
| 26 | `m2_nm` | STRING | Product taxonomy level 2 | Subcategory name |
| 27 | `m3_nm` | STRING | Product taxonomy level 3 | Segment name |
| 28 | `m4_nm` | STRING | Product taxonomy level 4 (most granular) | Item type |
| 29 | `atf_flag` | STRING | ⚠️ UNRELIABLE — do NOT use for ATF filtering. Found to tag all modules as 'BTF' even HPOV cards. Use `content_zone` instead. | `BTF`, `N/A` (ATF modules show as N/A, not 'ATF') |
| 30 | `atf_location` | STRING | Specific fold position label | `BTF`, `HeroAutoScroll`, `ATF` |
| 31 | `carousel_name` | STRING | Carousel name if in a carousel | `Not Carousel`, or carousel name |
| 32 | `module_group` | STRING | High-level grouping of module | `Content`, `Commerce` |
| 33 | `prism_module` | STRING | Is this a Prism design system module? | `Not Prism`, `Prism` |
| 34 | `hp_module_type` | STRING | HP-specific module type classification | `Content`, `Commerce` |
| 35 | `hp_module_name` | STRING | Friendly HP module name | `Adjustable Banner`, `Hero Carousel` |
| 36 | `module_view_count` | INT | How many times the module was viewed (impressions) | numeric or `null` |
| 37 | `overall_click_count` | INT | Total clicks across all asset elements | numeric or `null` |
| 38 | `asset_clicks_count` | INT | Clicks on the specific asset | numeric or `null` |
| 39 | `all_clicks_count_flag` | INT | Flag for counting all click types | `0`, `1`, or `null` |
| 40 | `total_atc_count` | INT | Add-to-cart count attributed to asset | numeric or `null` |
| 41 | `total_gmv` | FLOAT | Gross Merchandise Value attributed | dollar amount or `null` |
| 42 | `gmf_activation_flag` | INT | GMF category activation event | `0`, `1`, or `null` |
| 43 | `subs_activation_flag` | INT | Subscriptions activation event | `0`, `1`, or `null` |
| 44 | `acc_activation_flag` | INT | Walmart+ account activation event | `0`, `1`, or `null` |
| 45 | `exp_del_activation_flag` | INT | Express delivery activation event | `0`, `1`, or `null` |
| 46 | `rx_activation_flag` | INT | Pharmacy (Rx) activation event | `0`, `1`, or `null` |

---

## content_zone — Desktop ATF Definition
- Content zone format: camelCase string, e.g. `contentZone3`, `contentZone7`, `contentZone27`
- **Desktop ATF = contentZone7 through contentZone27** (business rule)
- atf_flag column is NOT reliable for Desktop (always = 'BTF') — use zone number instead
- SQL filter: `SAFE_CAST(REGEXP_EXTRACT(content_zone, r'\d+') AS INT64) BETWEEN 7 AND 27`
- HPOV primary zone on Desktop: contentZone3 (NOT ATF)
- SIG primary zones on Desktop: contentZone41, contentZone42 (NOT ATF)

---

## 🔑 Key Derived Metrics from this Table

```sql
-- CTR (Click Through Rate)
overall_click_count / NULLIF(module_view_count, 0) AS ctr  -- CORRECT. Do NOT use asset_clicks_count for CTR.
-- NOTE: asset_clicks_count is NOT the right column for CTR. Use overall_click_count.

-- CPTS (Clicks Per Thousand Sessions) — join with hp_session
(asset_clicks_count / NULLIF(hp_session_count, 0)) * 1000 AS cpts

-- ATC Rate
total_atc_count / NULLIF(module_view_count, 0) AS atc_rate

-- GMV Per Impression
total_gmv / NULLIF(module_view_count, 0) AS gmv_per_impression
```

---

## ⚠️ Cost & Query Best Practices

> This table is **~53.4 GB**. Always filter by date first!

```sql
-- ✅ ALWAYS filter by session_start_dt
WHERE session_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)

-- ✅ Typical weekly performance query
SELECT
    session_start_dt,
    experience_lvl2,
    hp_module_name,
    SUM(module_view_count) AS total_impressions,
    SUM(asset_clicks_count) AS total_clicks,
    SAFE_DIVIDE(SUM(asset_clicks_count), SUM(module_view_count)) AS ctr,
    SUM(total_atc_count) AS total_atc,
    SUM(total_gmv) AS total_gmv
FROM `wmt-site-content-strategy.scs_production.hp_summary_asset`
WHERE session_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY 1, 2, 3
ORDER BY session_start_dt DESC
```

---

## Module Grain Guide

Two levels of granularity exist for modules in this table:

- moduletype: Higher-level grouping. e.g. PrismAdjustableCardCarousel (= all HPOV cards), PrismScrollableItemGrid (= all SIG cards). DEFAULT grain for module breakdowns.
- hp_module_name: Lower-level, individual card. e.g. AutoScroll Card 1, SIG Card 2. Use only when card-level detail is requested.

Key moduletype values:
- PrismAdjustableCardCarousel = HPOV AutoScroll Cards 1-5
- PrismScrollableItemGrid = SIG Cards 1-6
- ItemCarousel = P13N or Merch item carousels
- PrismHeroCarousel = Hero Carousel
- OrderStatusTracker = OST
- AmendBanner = Amend Banner

RULE: Default to moduletype for breakdowns. Only use hp_module_name when card-level drill-down is asked for.

---

## WMC / Merch Content Type Classifier

This CASE statement is the source-of-truth classifier for separating WMC (Ads) from Merch impressions in hp_summary_asset.
Use this EVERY TIME you need to separate WMC from Merch. NEVER use HPsummary for this purpose.

```sql
CASE
  WHEN LOWER(IFNULL(content_served_by, '')) = 'ads'
    THEN 'WMC'
  WHEN LOWER(IFNULL(disable_content_personalization, '')) LIKE '%true%'
    THEN 'Merch'
  WHEN LOWER(IFNULL(disable_content_personalization, '')) LIKE '%false%'
    AND LOWER(IFNULL(personalized_asset, '')) = 'default'
    AND session_start_dt <= DATE('2025-03-01')
    AND LOWER(IFNULL(content_zone, '')) = 'contentzone3'
    AND LOWER(IFNULL(hp_module_name, '')) IN ('autoscroll card 1','autoscroll card 2','autoscroll card 3')
    THEN 'WMC'
  WHEN LOWER(IFNULL(disable_content_personalization, '')) LIKE '%false%'
    AND LOWER(IFNULL(personalized_asset, '')) = 'default'
    AND (
      (LOWER(IFNULL(content_zone, '')) IN ('contentzone8','contentzone9')
        AND LOWER(IFNULL(hp_module_name, '')) = 'adjustable banner small')
      OR
      (LOWER(IFNULL(content_zone, '')) IN ('contentzone10','contentzone11')
        AND LOWER(IFNULL(hp_module_name, '')) = 'triple pack small')
    )
    THEN 'WMC'
  ELSE 'Merch'
END AS content_type
```

### Logic Explained
| Condition | Result | Notes |
|-----------|--------|-------|
| content_served_by = 'ads' | WMC | Primary WMC signal — ad server placed this impression |
| disable_content_personalization CONTAINS 'true' | Merch | Content personalization disabled = site merch |
| disable_content_personalization CONTAINS 'false' + personalized_asset = 'default' + date <= 2025-03-01 + contentzone3 + AutoScroll Card 1/2/3 | WMC | Legacy WMC detection (pre-March 2025) |
| disable_content_personalization CONTAINS 'false' + personalized_asset = 'default' + (contentzone8/9 + Adjustable Banner Small) OR (contentzone10/11 + Triple Pack Small) | WMC | WMC banner/triple pack formats |
| Everything else | Merch | Default classification |

---

## 🔗 Relationships

- **Joins with** `hp_session` on `session_start_dt + experience_lvl2 + traffic_source_lvl2` for CPTS
- **Joins with** `sov_hp_carousel_content` on `message_id + content_zone + session_start_dt` for SOV
- **Rolls up from** `item_hp_scs` for item-level drill-downs

---

*Last updated by Keel Agent | Source: BigQuery schema exploration + Confluence HP Analytics 101*
