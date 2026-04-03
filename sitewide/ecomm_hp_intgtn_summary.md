# 🌐 ecomm_hp_intgtn_summary — Sitewide Context Table

> **Purpose:** Provides sitewide page view and session metrics for the Walmart homepage, sourced from the `ecomm_traffic` dataset.
> Use this table to **contextualize homepage performance against total site traffic** — a dimension NOT available in the core `scs_production` tables (hp_summary_asset, hp_session, etc.).

---

## 📌 Table Reference

| Field | Value |
|-------|-------|
| **Dataset** | `ecomm_traffic` |
| **Table** | `ecomm_hp_intgtn_summary` |
| **Grain** | Traffic Source × Date |
| **Date Filter Column** | `session_start_dt` |
| **Full Reference** | `ecomm_traffic.ecomm_hp_intgtn_summary` |

---

## 🔑 Known Columns

| Column | Type | Description |
|--------|------|-------------|
| `session_start_dt` | DATE | Session date — **always filter by this first** |
| `traffic_source_lvl2` | STRING | Traffic source (e.g., `'Organic: Direct'`) |
| `hp_session_flag` | STRING | Use `'HP-Session'` to filter to homepage sessions only. Omit for all sessions (sitewide). |
| `hp_session_count` | INTEGER | Number of homepage sessions |
| `homepage_pv_cnt` | INTEGER | Homepage page view count |

> ⚠️ **Note:** A `total_session_count` column (or equivalent) may exist for true sitewide session volume — confirm with `bigquery_get_table_schema` before using in a visitation rate calculation.

---

## 📐 Derived Metrics

| Metric | Formula | Notes |
|--------|---------|-------|
| **HP Page Views per Session** | `SAFE_DIVIDE(SUM(homepage_pv_cnt), SUM(hp_session_count))` | Engagement depth on HP |
| **HP Visitation Rate** | `SAFE_DIVIDE(SUM(hp_session_count), SUM(total_session_count))` | % of all sessions that hit HP — requires confirmed total session column |

---

## ⚠️ Key Filters — Apply These Always

| Filter | Default | When to Omit |
|--------|---------|-------------|
| `traffic_source_lvl2 = 'Organic: Direct'` | Standard reporting default | Omit when analyzing all traffic sources |
| `hp_session_flag = 'HP-Session'` | Homepage-only sessions | Omit when you want all/sitewide session volume |

---

## 🔍 Saved Query Patterns

---

### QUERY 1 — Homepage Page Views, Sessions & Pages-Per-Session (Specific Date Range)

**Use for:** Reporting on HP engagement volume for a defined date window.
**Metrics returned:** HP page views, HP sessions, pages per session.

```sql
SELECT
  session_start_dt,
  SUM(homepage_pv_cnt)                                          AS hp_page_views,
  SUM(hp_session_count)                                         AS hp_sessions,
  SAFE_DIVIDE(SUM(homepage_pv_cnt), SUM(hp_session_count))      AS pages_per_session
FROM `ecomm_traffic.ecomm_hp_intgtn_summary`
WHERE traffic_source_lvl2 = 'Organic: Direct'
  AND hp_session_flag     = 'HP-Session'
  AND session_start_dt BETWEEN '2026-03-14' AND '2026-03-17'
GROUP BY 1
ORDER BY session_start_dt ASC
```

> 📌 **Tip:** Swap out the `BETWEEN` dates as needed. For a rolling window, see Query 2.

---

### QUERY 2 — Homepage Sessions (Rolling Last N Days)

**Use for:** Quick recent view of HP sessions — no hardcoded dates needed.
**Default:** Last 5 days. Adjust `INTERVAL N DAY` as needed.

```sql
SELECT
  DATE(session_start_dt)                                        AS session_start_dt,
  SUM(hp_session_count)                                         AS hp_sessions
FROM `ecomm_traffic.ecomm_hp_intgtn_summary`
WHERE DATE(session_start_dt) >= DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY)
  AND traffic_source_lvl2   = 'Organic: Direct'
  AND hp_session_flag        = 'HP-Session'
GROUP BY 1
ORDER BY session_start_dt DESC
```

> 📌 **Note:** Remove `AND hp_session_flag = 'HP-Session'` to pull ALL sessions in the table (sitewide scope, if the table includes non-HP rows).

---

### QUERY 3 — HP Page Views + Sessions + Pages-Per-Session (Rolling, Full Metrics)

**Use for:** The complete HP engagement picture over a rolling window — most useful for WoW or trend comparisons.

```sql
SELECT
  DATE(session_start_dt)                                        AS session_start_dt,
  SUM(homepage_pv_cnt)                                          AS hp_page_views,
  SUM(hp_session_count)                                         AS hp_sessions,
  SAFE_DIVIDE(SUM(homepage_pv_cnt), SUM(hp_session_count))      AS pages_per_session
FROM `ecomm_traffic.ecomm_hp_intgtn_summary`
WHERE DATE(session_start_dt) >= DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY)
  AND traffic_source_lvl2   = 'Organic: Direct'
  AND hp_session_flag        = 'HP-Session'
GROUP BY 1
ORDER BY session_start_dt DESC
```

---

### QUERY 4 — WoW Comparison: This Week vs Last Week (HP Sessions & Page Views)

**Use for:** Standard week-over-week comparison, aligned to Walmart fiscal week (Saturday–Friday).

```sql
WITH weekly AS (
  SELECT
    DATE(session_start_dt)                                      AS dt,
    SUM(homepage_pv_cnt)                                        AS hp_page_views,
    SUM(hp_session_count)                                       AS hp_sessions,
    SAFE_DIVIDE(SUM(homepage_pv_cnt), SUM(hp_session_count))    AS pages_per_session
  FROM `ecomm_traffic.ecomm_hp_intgtn_summary`
  WHERE DATE(session_start_dt) >= DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY)
    AND traffic_source_lvl2   = 'Organic: Direct'
    AND hp_session_flag        = 'HP-Session'
  GROUP BY 1
)
SELECT
  dt,
  hp_page_views,
  hp_sessions,
  pages_per_session,
  LAG(hp_sessions) OVER (ORDER BY dt)                           AS hp_sessions_prior_day,
  SAFE_DIVIDE(hp_sessions - LAG(hp_sessions) OVER (ORDER BY dt),
              LAG(hp_sessions) OVER (ORDER BY dt))              AS sessions_dow
FROM weekly
ORDER BY dt DESC
```

---

### QUERY 5 — Schema Discovery (Run First If Unsure of Columns)

**Use for:** Confirming available column names in this table before writing other queries.

```sql
SELECT column_name, data_type
FROM `ecomm_traffic.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'ecomm_hp_intgtn_summary'
ORDER BY ordinal_position
```

---

## 🔗 Cross-Table Alignment: ecomm_traffic vs scs_production

When a user asks to **compare homepage vs sitewide**, use this table alongside `hp_summary_asset` or `hp_session`.

| Dimension | ecomm_hp_intgtn_summary | hp_session (scs_production) |
|-----------|------------------------|---------------------------|
| Sessions metric | `hp_session_count` | `hp_session_count` |
| Page views | `homepage_pv_cnt` | Not available |
| Traffic source | `traffic_source_lvl2` | `traffic_source_lvl2` |
| Date column | `session_start_dt` (DATE) | `session_start_dt` (TIMESTAMP → cast to DATE) |
| Sitewide sessions | Possibly `total_session_count` (confirm) | Not in this table |

> ⚠️ **When joining these tables:** Cast `hp_session.session_start_dt` to DATE. Confirm `traffic_source_lvl2` values match between tables.

---

## 💡 When Keel Should Use This Table

Use `ecomm_hp_intgtn_summary` when the user asks:

- *"How many people visited the homepage this week?"*
- *"What is the homepage visitation rate vs total site traffic?"*
- *"How many page views did the homepage get?"*
- *"What is pages per session for homepage?"*
- *"How do homepage sessions compare to sitewide sessions?"*
- *"Is HP traffic up or down vs last week?"*

**Do NOT use this table for:**
- CTR, ATC, GMV, Impressions → use `hp_summary_asset`
- Share of Voice / carousel → use `sov_hp_carousel_content`
- Item/SKU level → use `item_hp_scs`
- CPTS (sessions denominator) → use `hp_session`
