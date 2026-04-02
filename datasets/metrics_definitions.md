# 📐 Metrics Definitions & Glossary
## Keel Agent Knowledge Base — Homepage Analytics 101

*Source: [Confluence HP Analytics 101](https://confluence.walmart.com/pages/viewpage.action?spaceKey=RETAIL&title=Homepage+Analytics+101)*  
*Maintained by: Keel Agent*

---

## 🧮 Core Engagement Metrics

| Metric | Definition | Formula | Primary Table |
|--------|-----------|---------|---------------|
| **Impressions (Viewed)** | Number of times an asset/module was **loaded AND viewed** by a customer | — | `hp_summary_asset.module_view_count` |
| **Clicks** | Number of clicks (including Add to Cart) on an asset that navigate to a subsequent page | — | `hp_summary_asset.asset_clicks_count` |
| **CTR (Click Through Rate)** | Overall click-through rate on the homepage, impression-normalized | `Total Clicks ÷ Viewed Impressions` | `hp_summary_asset` |
| **CPTS (Clicks Per Thousand Sessions)** | A normalized engagement rate per 1,000 sessions — session-normalized alternative to CTR | `(Total Clicks ÷ Total HP Sessions) × 1,000` | `hp_summary_asset` + `hp_session` |
| **Asset Exit Rate** | % of homepage journeys where a user **left without engaging** on any subsequent page | `Exit Sessions ÷ HP Sessions` | — |
| **Sessions** | A unique customer visit. Resets after **30 min of inactivity** OR **12 hours** (hard reset) | — | `hp_session` |
| **HP Visitation Rate** | % of all sessions that visited the homepage | `hp_session_count ÷ total_session_count` | `hp_session` |

---

## 🛒 Commerce / Conversion Metrics

| Metric | Definition | Formula | Notes |
|--------|-----------|---------|-------|
| **ATC (Add to Cart)** | ATCs originating **directly from Homepage**, OR where HP was the **last touch** before cart — **excluding** breaks via search bar, global nav (Cart, My Items, Departments, Services, etc.) | Strict last-touch attribution | `hp_summary_asset.total_atc_count` |
| **ATC Rate** | Add-to-cart rate, impression-normalized | `Add-to-Cart Clicks ÷ Viewed Impressions` | `hp_summary_asset` |
| **Total GMV (Gross Merchandise Value)** | GMV from items ATC'd (per HP last-touch logic) **AND converted to a purchase in the same session** | — | `hp_summary_asset.total_gmv` |
| **GMV Per Impression** | Revenue efficiency of an asset | `GMV ÷ Viewed Impressions` | `hp_summary_asset` |

### ⚠️ ATC Attribution Logic (Critical)

HP gets ATC/GMV credit ONLY when:
1. The ATC originated **directly from the homepage**, OR
2. HP was the **last touchpoint** before cart — with **no intervening breaks** via:
   - Search bar
   - Global nav (Cart, My Items, Departments, Services)
   - Any other HP click that redirects off-page

This is **strict last-touch attribution** — do not confuse with first-touch or linear.

---

## 🚀 Activation Metrics

Activations track **first-time category buyers** after a **12-month purchase gap**. These are NOT just "new users" — they are users re-entering a category after being lapsed for 12+ months.

| Metric | Definition | Flag Column |
|--------|-----------|-------------|
| **GMF Activation** | User makes their **first GMF purchase** (Electronics, Toys & Seasonal, Hardlines, Fashion, Home) having made **zero GMF purchases in prior 12 months** | `hp_summary_asset.gmf_activation_flag` |
| **Food Activation** | User makes their **first Food purchase** having made zero Food purchases in prior 12 months | — |
| **Consumables Activation** | User makes their **first Consumables purchase** having made zero Consumables purchases in prior 12 months | — |
| **Subs Activation** | Subscriptions-related activation | `hp_summary_asset.subs_activation_flag` |
| **Acc Activation** | Walmart+ account activation | `hp_summary_asset.acc_activation_flag` |
| **Exp Del Activation** | Express delivery activation | `hp_summary_asset.exp_del_activation_flag` |
| **Rx Activation** | Pharmacy (Rx) activation | `hp_summary_asset.rx_activation_flag` |

> **Key concept:** The 12-month lookback window makes these a **lapsed/new buyer re-engagement KPI**, not just first-ever buyers.

---

## 📊 Share of Voice (SOV)

| Metric | Definition | Table |
|--------|-----------|-------|
| **SOV (Share of Voice)** | % of total homepage impressions captured by a given message/module/SBU | `sov_hp_carousel_content` |
| **Message SOV** | Impression share of a specific campaign message | `sov_hp_carousel_content.message_name` |
| **SBU SOV** | Impression share by Strategic Business Unit | `sov_hp_carousel_content.sbu` |

```sql
-- SOV Calculation Pattern
SAFE_DIVIDE(
    SUM(viewed_impressions),
    SUM(SUM(viewed_impressions)) OVER (PARTITION BY session_start_dt)
) AS share_of_voice
```

---

## 📍 Business Terminology Glossary

| Term | Definition |
|------|-----------|
| **HP / Homepage** | The Walmart.com homepage (walmart.com landing page) |
| **Asset** | A piece of content placed on the homepage (banner, carousel, tile, etc.) |
| **Module** | The container/widget that displays content on the homepage |
| **Message** | A campaign or editorial unit of content identified by `message_id` and `message_name` |
| **Content Zone (CZ)** | A specific slot/position on the homepage layout (e.g., `contentZone33`, `CZ3`) |
| **ATF (Above the Fold)** | Content visible without scrolling |
| **BTF (Below the Fold)** | Content requiring scrolling to see |
| **HPOV (Homepage Overview)** | The primary HP content overview — Cards 1–5 |
| **SIG** | Secondary image gallery or similar content — Cards 1–6 |
| **SBU (Strategic Business Unit)** | Business unit owning or sponsoring content (e.g., HOME, GROCERY, FASHION) |
| **1P** | First-party seller (Walmart sells directly) |
| **3P** | Third-party marketplace seller |
| **cxtools** | Editorial content management/serving system (default/non-personalized content) |
| **p13n** | Personalization engine serving algorithmically personalized content |
| **Prism** | Walmart's design system — modules built on Prism have `prism_module = 'Prism'` |
| **Hero Carousel** | The primary rotating banner carousel at the top of the homepage |
| **Organic Traffic** | Users who arrived without paid acquisition (Direct, SEO, Social) |
| **WoW** | Week-over-Week comparison |
| **WTD** | Week-to-Date |
| **YoY** | Year-over-Year comparison |
| **WM Wk** | Walmart fiscal week (different from calendar week — starts on different day) |

---

## 📋 Dashboard Reference

| Dashboard Name | Purpose |
|----------------|---------|
| **D-1 Reports** | Day-minus-one daily reporting |
| **Home Page Performance** | Overall HP performance tracking (primary dashboard) |
| **Message Comparison** | Compare performance across messages/creative assets |
| **Message Personalization Tracking** | Track personalized vs default message performance |
| **Historical Asset Performance** | Historical view of asset-level metrics over time |
| **Share of Voice** | How much visibility different assets/partners/SBUs get |
| **Carousel Item Level** | Item-level performance inside carousels (powered by `item_hp_scs`) |
| **Weekly HP Eligible Report** | Weekly eligibility-based HP reporting |

---

## 🔢 Sample Queries (Reference Patterns)

### CTR by Module (Last 7 Days)
```sql
SELECT
    hp_module_name,
    experience_lvl2,
    SUM(module_view_count) AS impressions,
    SUM(asset_clicks_count) AS clicks,
    SAFE_DIVIDE(SUM(asset_clicks_count), SUM(module_view_count)) AS ctr
FROM `wmt-site-content-strategy.scs_production.hp_summary_asset`
WHERE session_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY 1, 2
ORDER BY ctr DESC
```

### ATC Drop Analysis (Why did ATC drop?)
```sql
SELECT
    session_start_dt,
    hp_module_name,
    experience_lvl2,
    SUM(module_view_count) AS impressions,
    SUM(total_atc_count) AS total_atc,
    SAFE_DIVIDE(SUM(total_atc_count), SUM(module_view_count)) AS atc_rate,
    SUM(total_gmv) AS gmv
FROM `wmt-site-content-strategy.scs_production.hp_summary_asset`
WHERE session_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY)
GROUP BY 1, 2, 3
ORDER BY session_start_dt DESC, total_atc DESC
```

### CPTS Calculation
```sql
WITH sessions AS (
    SELECT
        DATE(session_start_dt) AS session_date,
        experience_lvl2,
        SUM(hp_session_count) AS hp_sessions
    FROM `wmt-site-content-strategy.scs_production.hp_session`
    WHERE DATE(session_start_dt) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
    GROUP BY 1, 2
),
asset_clicks AS (
    SELECT
        session_start_dt AS session_date,
        experience_lvl2,
        hp_module_name,
        SUM(asset_clicks_count) AS clicks
    FROM `wmt-site-content-strategy.scs_production.hp_summary_asset`
    WHERE session_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
    GROUP BY 1, 2, 3
)
SELECT
    a.session_date,
    a.experience_lvl2,
    a.hp_module_name,
    a.clicks,
    s.hp_sessions,
    SAFE_DIVIDE(a.clicks, s.hp_sessions) * 1000 AS cpts
FROM asset_clicks a
JOIN sessions s USING (session_date, experience_lvl2)
ORDER BY cpts DESC
```

### GMF Activations Week-over-Week
```sql
SELECT
    wm_wk_of_year,
    experience_lvl2,
    SUM(gmf_activation_flag) AS gmf_activations,
    LAG(SUM(gmf_activation_flag)) OVER (PARTITION BY experience_lvl2 ORDER BY wm_wk_of_year) AS prev_week_activations,
    SAFE_DIVIDE(
        SUM(gmf_activation_flag) - LAG(SUM(gmf_activation_flag)) OVER (PARTITION BY experience_lvl2 ORDER BY wm_wk_of_year),
        LAG(SUM(gmf_activation_flag)) OVER (PARTITION BY experience_lvl2 ORDER BY wm_wk_of_year)
    ) AS wow_change
FROM `wmt-site-content-strategy.scs_production.hp_summary_asset`
WHERE session_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
GROUP BY 1, 2
ORDER BY wm_wk_of_year DESC
```

---

*Last updated by Keel Agent | Source: Confluence HP Analytics 101 + Keel Agent Workflows doc*
