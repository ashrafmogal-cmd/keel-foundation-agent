# 📊 Dataset: `sov_hp_carousel_content`

**Project:** `wmt-site-content-strategy`  
**Dataset:** `scs_production`  
**Full Reference:** `wmt-site-content-strategy.scs_production.sov_hp_carousel_content`  
**Size:** ~13.6 GB 🟡  
**Keel Role:** Share-of-Voice (SOV) analysis for homepage carousel content — tracks how much impressions, clicks, and GMV each editorial message/module captures.

---

## 🧭 What It Represents

One row = one **carousel content piece** (a message or module within a carousel) sliced by:
- Date (`session_start_dt`)
- Platform (`experience_lvl2`)
- Traffic source (`traffic_source_lvl2`)
- Content metadata (message, carousel, module, personalization flags)
- Performance metrics (impressions, clicks, ATC, GMV)

Used to answer: **"Which messages/content are winning impressions on the homepage carousel, and how does that share correlate with performance?"**

---

## 📋 Column Reference

| # | Column | Type | Description | Sample Values |
|---|--------|------|-------------|---------------|
| 1 | `experience_lvl2` | STRING | Platform/device | `App: Android`, `Web: Mobile`, `Web: Desktop`, `App: iOS` |
| 2 | `traffic_source_lvl2` | STRING | Traffic acquisition channel | `Organic: Direct`, `Paid: SEM`, `Organic: SEO` |
| 3 | `atf_flag` | STRING | Above/Below the fold indicator | `ATF`, `BTF` |
| 4 | `carousel_name` | STRING | Name of the carousel | `Not Carousel`, or specific carousel name |
| 5 | `module_group` | STRING | High-level module grouping | `Content`, `Commerce` |
| 6 | `atf_location` | STRING | Specific fold position | `BTF`, `HeroAutoScroll`, `ATF` |
| 7 | `prism_module` | STRING | Prism design system flag | `Not Prism`, `Prism` |
| 8 | `sbu` | STRING | Strategic Business Unit | `OTHER`, `CROSS CATEGORY`, `HOME`, `GROCERY` |
| 9 | `default_shown` | STRING | Was default or personalized content shown | `Default`, `Personalized`, `Not Prism` |
| 10 | `message_id` | STRING | UUID of the content message | UUID or `null` |
| 11 | `message_name` | STRING | Campaign/message name | `"2025 Fall New And Trending"` |
| 12 | `message_sponsor` | STRING | Sponsoring business unit | `CAMPAIGNS & EVENTS`, `HOME`, `GROCERY` |
| 13 | `message_type` | STRING | Message category | `SEASONAL`, `HOLIDAY`, `null` |
| 14 | `modulename` | STRING | Module display name | `10/20 Full Width HeroPOV` |
| 15 | `moduletype` | STRING | Technical module type | `WriteAReviewBanner`, `PrismAdjustableCardCarousel` |
| 16 | `contentzone` | STRING | Content zone on HP | `contentZone15`, `contentZone3` |
| 17 | `container_id` | STRING | Container within zone | `gridHeroFullWidth5CardContainer1` |
| 18 | `contentservedby` | STRING | Serving engine | `cxtools` (editorial), `p13n` (personalization) |
| 19 | `disable_content_personalization` | STRING | Personalization disabled flag | `False`, `True` |
| 20 | `personalized_asset` | STRING | Whether the asset was personalized | `False`, `True` |
| 21 | `is_sponsored` | STRING | Sponsored content flag | `null`, `1`, `0` |
| 22 | `1p_3p_flag` | STRING | First-party vs third-party seller | `null`, `1P`, `3P` |
| 23 | `viewed_impressions` | INT | **Number of times content was viewed** | `48`, `4`, `1` |
| 24 | `overall_click_count` | INT | Total click interactions | `1`, `null` |
| 25 | `total_atc_count` | INT | Add-to-cart events | numeric or `null` |
| 26 | `all_clicks_count_flag` | INT | Inclusive click count flag | `0`, `1`, `null` |
| 27 | `asset_clicks_count` | INT | Clicks on the specific asset | numeric or `null` |
| 28 | `total_gmv` | FLOAT | Revenue attributed to this module/message | dollar amount or `null` |
| 29 | `session_start_dt` | STRING | Session date | `2024-04-18`, `2025-10-20` |
| 30 | `tenant_ste_cd` | STRING | Site/tenant identifier | `US_GLASS_ANDROID`, `US_GLASS_CORESITE` |

---

## 🔑 Key Derived Metrics & SOV Calculations

```sql
-- Share of Voice (SOV) by Message
SELECT
    session_start_dt,
    message_name,
    sbu,
    SUM(viewed_impressions) AS message_impressions,
    SUM(SUM(viewed_impressions)) OVER (PARTITION BY session_start_dt) AS total_impressions,
    SAFE_DIVIDE(
        SUM(viewed_impressions),
        SUM(SUM(viewed_impressions)) OVER (PARTITION BY session_start_dt)
    ) AS share_of_voice
FROM `wmt-site-content-strategy.scs_production.sov_hp_carousel_content`
WHERE session_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY 1, 2, 3
ORDER BY session_start_dt DESC, share_of_voice DESC

-- CTR on Carousel Content
SAFE_DIVIDE(asset_clicks_count, viewed_impressions) AS ctr

-- Personalized vs Default Performance Comparison
SELECT
    default_shown,
    SUM(viewed_impressions) AS impressions,
    SUM(asset_clicks_count) AS clicks,
    SAFE_DIVIDE(SUM(asset_clicks_count), SUM(viewed_impressions)) AS ctr,
    SUM(total_gmv) AS gmv
FROM `wmt-site-content-strategy.scs_production.sov_hp_carousel_content`
WHERE session_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY 1
```

---

## ⚠️ Cost & Query Best Practices

> This table is **~13.6 GB**. Filter by `session_start_dt` to control costs.

```sql
-- ✅ Always filter by date
WHERE session_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)

-- ✅ When comparing messages, GROUP BY message_name + session_start_dt
```

---

## 🔗 Relationships

- **Joins with** `hp_summary_asset` on `message_id + contentzone + session_start_dt` for cross-metric analysis
- **Part of SOV pipeline** — compute impression share across all carousel content on a given date
- Content served by `cxtools` = **editorial/default**, by `p13n` = **personalized**

---

*Last updated by Keel Agent | Source: BigQuery schema exploration + Confluence HP Analytics 101*
