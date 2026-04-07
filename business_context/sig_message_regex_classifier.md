# SIG Message REGEX Classifier — Reusable Feature

## Purpose
Classify `message_name` values in `hp_summary_asset` into business content categories using REGEXP_CONTAINS.
Eliminates need for manual message tagging or SBU column (which is inaccurate for SIG analysis).

## When to Use
- Any SIG (PrismScrollableItemGrid) analysis on contentZone5
- Message-level SOV, CTR, ATC, GMV comparisons by content type
- Finding Tech (or any category) messages without knowing exact names

## Zone Context — ALWAYS Filter This Way for SIG
- contentZone5 = Site Merch Driven messages (primary analysis zone)
- contentZone4 = P13N/Unattributed only (Jump Right Back In, personalized carousels — no named site merch)
- SQL: `SAFE_CAST(REGEXP_EXTRACT(content_zone, r'\d+') AS INT64) IN (4, 5)`

## REGEX Classifier (CASE Statement — Copy/Paste Ready)

```sql
CASE
  WHEN REGEXP_CONTAINS(
         LOWER(IFNULL(message_name,'')),
         r'tech|electron|gaming and media|pc gaming|laptop|tablet|computer'
       ) THEN 'Tech / Electronics'
  WHEN REGEXP_CONTAINS(
         LOWER(IFNULL(message_name,'')),
         r'fashion|apparel|clothing|style|wear'
       ) THEN 'Fashion'
  WHEN REGEXP_CONTAINS(
         LOWER(IFNULL(message_name,'')),
         r'\bhome\b|furniture|decor|bedding|patio|garden|floor'
       ) THEN 'Home'
  WHEN REGEXP_CONTAINS(
         LOWER(IFNULL(message_name,'')),
         r'food|grocer|meal|snack|beverage|drink'
       ) THEN 'Food'
  WHEN REGEXP_CONTAINS(
         LOWER(IFNULL(message_name,'')),
         r'beauty|skin|hair|makeup|personal care'
       ) THEN 'Beauty / Personal Care'
  WHEN REGEXP_CONTAINS(
         LOWER(IFNULL(message_name,'')),
         r'toy|kids|baby|toddler|children|easter basket'
       ) THEN 'Toys / Kids / Baby'
  WHEN REGEXP_CONTAINS(
         LOWER(IFNULL(message_name,'')),
         r'consumable|household|essential|cleaning|laundry|paper|health|wellness|hsa|fsa'
       ) THEN 'Consumables / Health'
  WHEN REGEXP_CONTAINS(
         LOWER(IFNULL(message_name,'')),
         r'sport|outdoor|auto|pet|garden'
       ) THEN 'Sports / Auto / Pets'
  WHEN REGEXP_CONTAINS(
         LOWER(IFNULL(message_name,'')),
         r'rollbacks and more|savings event|clearance|top 100'
       ) THEN 'Cross Category / Savings'
  WHEN message_name IS NULL THEN 'P13N / Unattributed'
  ELSE 'Other'
END AS msg_category
```

## Critical Notes
- **Tech regex excludes "Game Time"** — Game Time is a sports/Super Bowl event. Only `gaming and media` and `pc gaming` qualify as Tech to avoid false positives.
- **`\bhome\b`** — word boundary prevents matching "home improvement" messages under wrong category
- **Order matters** — more specific patterns (Tech) before broader catch-alls (Cross Category)
- **NULL message_name** = P13N content in CZ4 (always) and rare CZ5 rows

## Known Tech Messages in contentZone5 (as of Mar-Apr 2026)
| Message Name | Impressions (28d) | CTR |
|---|---|---|
| Tech Rollbacks And More | 51,254,598 | 0.4243% |
| 2026 March Savings Event Tech | 1,187,889 | 0.3771% |
| Gaming And Media Rollbacks And More | ~8 | negligible |

## Performance Context (contentZone5, Last 28 Days)
- Tech/Electronics SOV: 3.88% (7th of 10 categories)
- Tech/Electronics CTR: 0.4232% (9th of 10 categories)
- Tech/Electronics ATC/1K: 0.362 — LOWEST of any category in CZ5
- Compare: Food ATC/1K = 2.406, Home CTR = 1.04%

## Extending the Classifier
To add a new category (e.g., Pharmacy/Healthcare):
```sql
WHEN REGEXP_CONTAINS(
       LOWER(IFNULL(message_name,'')),
       r'pharmacy|rx|prescription|medicare|insurance'
     ) THEN 'Pharmacy / Healthcare'
```
Add BEFORE the `ELSE 'Other'` line.
