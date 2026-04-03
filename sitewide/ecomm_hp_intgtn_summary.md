# 🌐 ecomm_hp_intgtn_summary — Sitewide Context Queries

> **Table:** `ecomm_traffic.ecomm_hp_intgtn_summary`
> **Purpose:** Sitewide homepage traffic data — page views, sessions. Use to compare homepage performance against sitewide context.
> **Note:** `pages_per_session` is a derived metric you can calculate from Query 1 results: `hp_page_views / hp_sessions`

---

## QUERY 1 — HP Page Views & Sessions (Date Range)

```sql
SELECT session_start_dt, sum(homepage_pv_cnt) as hp_page_views, sum(hp_session_count) as hp_sessions
FROM ecomm_traffic.ecomm_hp_intgtn_summary
WHERE traffic_source_lvl2 = 'Organic: Direct'
  AND hp_session_flag = 'HP-Session'
  AND session_start_dt BETWEEN '2026-03-14' AND '2026-03-17'
GROUP BY 1
ORDER BY session_start_dt ASC
```

---

## QUERY 2 — HP Sessions (Rolling Last 5 Days)

```sql
SELECT CAST(session_start_dt AS DATE) AS session_start_dt, sum(hp_session_count) as hp_sessions
FROM ecomm_traffic.ecomm_hp_intgtn_summary
WHERE DATE(session_start_dt) >= DATE_TRUNC(day, NOW() - INTERVAL 5 DAY)
  AND traffic_source_lvl2 = 'Organic: Direct'
GROUP BY CAST(session_start_dt AS DATE)
ORDER BY session_start_dt DESC
```
