# 📊 Dataset: `hp_session`

**Project:** `wmt-site-content-strategy`  
**Dataset:** `scs_production`  
**Full Reference:** `wmt-site-content-strategy.scs_production.hp_session`  
**Size:** ~10 MB ✅ (Safe to query without heavy filters)  
**Keel Role:** Session-level denominator — used for computing HP visitation rate and normalizing CPTS across all other tables.

---

## 🧭 What It Represents

One row = one **session segment** sliced by:
- Date (`session_start_dt`)
- Experience/platform (`experience_lvl1`, `experience_lvl2`)
- Traffic source (`traffic_source_lvl2`)
- Walmart fiscal week (`wm_wk_of_year`)

It answers the question: **"Of all sessions in a given segment, how many visited the homepage?"**

---

## 📋 Column Reference

| # | Column | Type | Description | Sample Values |
|---|--------|------|-------------|---------------|
| 1 | `session_start_dt` | TIMESTAMP | When the session started | `2026-03-31T00:00:00+00:00` |
| 2 | `experience_lvl1` | STRING | Broad experience bucket | `App`, `Web` |
| 3 | `experience_lvl2` | STRING | Specific platform | `App: Android`, `App: iOS`, `Web: Desktop`, `Web: Mobile` |
| 4 | `traffic_source_lvl2` | STRING | Traffic source detail | `Organic: Direct`, `Paid: SEM`, `Organic: SEO`, `Organic: Social` |
| 5 | `wm_wk_of_year` | INT | Walmart fiscal week number | `9`, `14`, `52` |
| 6 | `hp_session_count` | INT | Sessions that **visited the homepage** | `256,745`, `604,685` |
| 7 | `total_session_count` | INT | **All sessions** in that segment (denominator) | `473,291`, `886,573` |

---

## 🔑 Key Derived Metrics

```sql
-- HP Visitation Rate
hp_session_count / NULLIF(total_session_count, 0) AS hp_visitation_rate
-- Example: Paid SEM Android = 604,685 / 886,573 = 68.2%

-- CPTS (requires joining with hp_summary_asset)
-- Step 1: Get total HP sessions by segment
-- Step 2: Join on session_start_dt + experience_lvl2 + traffic_source_lvl2
-- Step 3: (overall_click_count / hp_session_count) * 1000

-- Weekly HP Sessions by Platform
SELECT
    wm_wk_of_year,
    experience_lvl2,
    SUM(hp_session_count) AS total_hp_sessions,
    SUM(total_session_count) AS total_sessions,
    SAFE_DIVIDE(SUM(hp_session_count), SUM(total_session_count)) AS hp_visitation_rate
FROM `wmt-site-content-strategy.scs_production.hp_session`
GROUP BY 1, 2
ORDER BY 1, 2
```

---

## 📅 Session Definition

> A **session** resets after:
> - **30 minutes of inactivity**, OR
> - **12 hours** (hard reset regardless of activity)

This is critical for interpreting session counts — one user can generate multiple sessions in a day.

---

## ⚠️ Query Best Practices

> This table is only **~10 MB** — safe to query without strict date filters, but still good practice.

```sql
-- ✅ Standard session denominator pull (for CPTS calculation)
SELECT
    DATE(session_start_dt) AS session_date,
    experience_lvl2,
    traffic_source_lvl2,
    SUM(hp_session_count) AS hp_sessions,
    SUM(total_session_count) AS total_sessions
FROM `wmt-site-content-strategy.scs_production.hp_session`
WHERE DATE(session_start_dt) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY 1, 2, 3
```

---

## 🔗 Relationships

- **Primary join key** for `hp_summary_asset` CPTS calculations: `session_start_dt + experience_lvl2 + traffic_source_lvl2`
- Acts as the **denominator** for any session-normalized metric across all Keel tables

---

*Last updated by Keel Agent | Source: BigQuery schema exploration + Confluence HP Analytics 101*
