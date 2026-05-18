# 🗣️ Module Name Lingo & Clarification Guide
## Keel Agent Knowledge Base

*Users often use informal names or partial descriptions for modules and messages.*
*Never assume — always run a discovery query or ask a follow-up question.*

---

## Known Lingo Mappings

| What user says | What it means | Column to use | Common mistake |
|----------------|---------------|---------------|----------------|
| "Visual Navigation Module" | A `moduletype` in `hp_summary_asset` | `moduletype` | Searching `message_name` |
| "Nav Module" | Same as above | `moduletype` | Searching `message_name` |
| "Get It All Right Here visual navigation module" | The **module placement** (moduletype) | `moduletype` | Filtering `message_name = 'Get It All Right Here'` |

---

## The Golden Rule

> **Module** = the container/placement (e.g., AutoScroll Card 1, Visual Navigation, SIG)
> **Message** = the content/campaign running inside a module (e.g., "Back to School", "Get It All Right Here")
> These are completely different dimensions. Wrong dimension = completely wrong query.

---

## Visual Navigation Module — Detailed Notes

- "Visual Navigation" refers to a **module type** (placement on the homepage)
- It is NOT a message or campaign name
- To find the exact `moduletype` value:
```sql
SELECT DISTINCT hp_module_name, moduletype, COUNT(*) as cnt
FROM `wmt-site-content-strategy.scs_production.hp_summary_asset`
WHERE session_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  AND (LOWER(hp_module_name) LIKE '%nav%' OR LOWER(moduletype) LIKE '%nav%')
GROUP BY 1, 2 ORDER BY cnt DESC
```

- To get performance of all messages running IN the Visual Navigation module:
```sql
-- First confirm moduletype value, then:
SELECT message_name, SUM(module_view_count) AS impressions,
       SUM(overall_click_count) AS clicks,
       SAFE_DIVIDE(SUM(overall_click_count), SUM(module_view_count)) AS ctr
FROM `wmt-site-content-strategy.scs_production.hp_summary_asset`
WHERE session_start_dt BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
  AND moduletype = '<confirmed_moduletype>'
  AND experience_lvl2 IN ('App: iOS', 'App: Android')
GROUP BY 1 ORDER BY impressions DESC
```

---

## Clarification Rule

If a user gives a name that could be either a message OR a module:
→ **Ask:** "Are you asking about the *message* (campaign) named X, or the *module/placement* called X?"
→ Do not guess. One wrong assumption leads to a completely incorrect query.

## Desktop Homepage

If user asks about "Desktop Homepage":
- Platform filter: `experience_lvl2 IN ('Web: Desktop')`
- Default Keel analysis is App (iOS + Android) — always confirm platform.
