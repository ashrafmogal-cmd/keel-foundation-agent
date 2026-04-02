# 📅 Reporting Conventions & Module Name Reference
## Keel Agent Knowledge Base | Fiscal Calendar, WBR Windows, hp_module_name & moduletype

*Maintained by: Keel Agent*

---

## 📆 Walmart Fiscal Week Definition

> **Walmart fiscal week runs SATURDAY through FRIDAY.**

| Day | Role |
|-----|------|
| **Saturday** | Week START |
| Friday | Week END |

**Never assume Monday–Sunday for a Walmart week.**

### Example
| Fiscal Week | Start | End |
|-------------|-------|-----|
| WK42 FY26 | Sat, Nov 15, 2025 | Fri, Nov 21, 2025 |
| WK43 FY26 | Sat, Nov 22, 2025 | Fri, Nov 28, 2025 |
| WK44 FY26 | Sat, Nov 29, 2025 | Fri, Dec 5, 2025 |
| WK1 FY27 | Sat, Jan 31, 2026 | Fri, Feb 6, 2026 |

---

## 📊 WBR Reporting Windows (Two Separate Cadences)

There are **two distinct WBR date windows** depending on the report type. **Always confirm which one applies before writing SQL.**

### 1. Standard WBR — Homepage Performance
| | |
|-|-|
| **Date range** | **Saturday through Tuesday** (4 days) |
| **Reported on** | Monday and Tuesday |
| **Used for** | General HP performance: CTR, GMV, ATC, Impressions |
| **Example** | If reporting on Mon Jan 13 → range = Sat Jan 10 – Tue Jan 13 |

### 2. Messaging Performance WBR
| | |
|-|-|
| **Date range** | **Monday through Sunday** (7 days — full week) |
| **Reported on** | Monday and Tuesday |
| **Used for** | Message-level performance, share-out context, message CTR/GMV trends |
| **Example** | If reporting on Mon Jan 13 → range = Mon Jan 6 – Sun Jan 12 |

> ⚠️ **Key rule**: When a user asks about "WBR" or "last week" performance without specifying, clarify which window they need.  
> If context makes it obvious (e.g., "messaging performance"), use the correct window automatically.

---

## 🔢 SQL Patterns by Reporting Window

### Standard WBR — Saturday to Tuesday
```sql
-- Find the most recent Saturday and the Tuesday 3 days later
WITH reporting_window AS (
  SELECT
    DATE_SUB(CURRENT_DATE(), INTERVAL MOD(DAYOFWEEK(CURRENT_DATE()) + 1, 7) DAY) AS wbr_start,  -- Last Saturday
    DATE_ADD(
      DATE_SUB(CURRENT_DATE(), INTERVAL MOD(DAYOFWEEK(CURRENT_DATE()) + 1, 7) DAY),
      INTERVAL 3 DAY
    ) AS wbr_end  -- Tuesday (3 days after Saturday)
)
SELECT *
FROM `wmt-site-content-strategy.scs_production.hp_summary_asset`, reporting_window
WHERE session_start_dt BETWEEN wbr_start AND wbr_end
```

### Messaging Performance WBR — Monday to Sunday
```sql
-- Full Mon–Sun week (most recently completed)
WITH reporting_window AS (
  SELECT
    DATE_SUB(CURRENT_DATE(), INTERVAL MOD(DAYOFWEEK(CURRENT_DATE()) + 6, 7) DAY) AS wbr_start,  -- Last Monday
    DATE_SUB(CURRENT_DATE(), INTERVAL MOD(DAYOFWEEK(CURRENT_DATE()) + 6, 7) - 6 DAY) AS wbr_end   -- Last Sunday
)
SELECT *
FROM `wmt-site-content-strategy.scs_production.hp_summary_asset`, reporting_window
WHERE session_start_dt BETWEEN wbr_start AND wbr_end
```

### WoW Comparison (prior week same window)
```sql
-- For messaging WBR WoW:
WHERE session_start_dt BETWEEN
  DATE_SUB(<wbr_start>, INTERVAL 7 DAY)
  AND DATE_SUB(<wbr_end>, INTERVAL 7 DAY)
```

---

## 🗺️ hp_module_name & moduletype Mappings in hp_summary_asset

These are the **exact column values** used in the `hp_summary_asset` table.  
Always use these exact strings — do not guess or abbreviate.

---

### HPOV — Hero POV (AutoScroll Cards)

> HPOV = the primary above-the-fold carousel on the Walmart homepage. 5 cards, 39M daily impressions.

| hp_module_name | moduletype | Card # | Daily Impressions | SOV | CTR Benchmark | Content |
|----------------|-----------|--------|-------------------|-----|--------------|---------|
| `AutoScroll Card 1` | `PrismAdjustableCardCarousel` | Card 1 | 13M | 35% | **.23%** | Tier 1 only |
| `AutoScroll Card 2` | `PrismAdjustableCardCarousel` | Card 2 | 9M | 23% | **.15%** | WMC Ads (~92% sold) |
| `AutoScroll Card 3` | `PrismAdjustableCardCarousel` | Card 3 | 8M | 19% | **.13%** | WMC Ads |
| `AutoScroll Card 4` | `PrismAdjustableCardCarousel` | Card 4 | 5M | 13% | **.17%** | Services ONLY (Pharmacy, Get It Fast, OnePay, W+ Assist) |
| `AutoScroll Card 5` | `PrismAdjustableCardCarousel` | Card 5 | 4M | 10% | **.25%** ⭐ highest | Tier 1 & 2 Merch |

---

### SIG — Scrollable Item Grid

> SIG = BTF (below-the-fold) item carousel module. Accounts for ~50% of total BTF engagement.

| hp_module_name | moduletype | Role |
|----------------|-----------|------|
| `SIG Card 1` | `PrismScrollableItemGrid` | Parent message — must be Tier 1, de-duped from HPOV |
| `SIG Card 2` | `PrismScrollableItemGrid` | Sub-message (direct M1 child) |
| `SIG Card 3` | `PrismScrollableItemGrid` | Sub-message |
| `SIG Card 4` | `PrismScrollableItemGrid` | Sub-message |
| `SIG Card 5` | `PrismScrollableItemGrid` | Sub-message |
| `SIG Card 6` | `PrismScrollableItemGrid` | Sub-message |

---

## 🔍 SQL Filter Patterns

### All HPOV Cards (use moduletype — cleaner)
```sql
WHERE moduletype = 'PrismAdjustableCardCarousel'
```

### All HPOV Cards (use hp_module_name — explicit)
```sql
WHERE hp_module_name IN (
  'AutoScroll Card 1',
  'AutoScroll Card 2',
  'AutoScroll Card 3',
  'AutoScroll Card 4',
  'AutoScroll Card 5'
)
```

### Specific HPOV Card
```sql
WHERE hp_module_name = 'AutoScroll Card 1'   -- or Card 2, 3, 4, 5
```

### All SIG Cards (use moduletype — cleaner)
```sql
WHERE moduletype = 'PrismScrollableItemGrid'
```

### All SIG Cards (use hp_module_name)
```sql
WHERE hp_module_name LIKE 'SIG Card%'
```

### Specific SIG Card
```sql
WHERE hp_module_name = 'SIG Card 1'   -- Parent message
```

### HPOV + SIG Combined (full homepage picture)
```sql
WHERE moduletype IN ('PrismAdjustableCardCarousel', 'PrismScrollableItemGrid')
```

### Exclude HPOV and SIG (all other modules)
```sql
WHERE moduletype NOT IN ('PrismAdjustableCardCarousel', 'PrismScrollableItemGrid')
```

---

## 🧩 How moduletype Links to hp_module_name

Think of it as:
- `moduletype` = **the container type** (what kind of module is it?)
- `hp_module_name` = **the specific slot** (which card within that module?)

```
moduletype = 'PrismAdjustableCardCarousel'
  └── hp_module_name IN ('AutoScroll Card 1' ... 'AutoScroll Card 5')

moduletype = 'PrismScrollableItemGrid'
  └── hp_module_name IN ('SIG Card 1' ... 'SIG Card 6')
```

**Use `moduletype` when:** You want all cards of a type in one filter  
**Use `hp_module_name` when:** You want a specific card (e.g., Card 1 only), or comparing cards to each other

---

## ⚡ Quick Reference Card

| I want to analyze... | Filter to use |
|---------------------|--------------|
| All HPOV | `moduletype = 'PrismAdjustableCardCarousel'` |
| Just Card 1 (Tier 1 dominant) | `hp_module_name = 'AutoScroll Card 1'` |
| Just Card 4 (Services) | `hp_module_name = 'AutoScroll Card 4'` |
| Card 5 (highest CTR) | `hp_module_name = 'AutoScroll Card 5'` |
| All SIG | `moduletype = 'PrismScrollableItemGrid'` |
| SIG parent only | `hp_module_name = 'SIG Card 1'` |
| HPOV + SIG together | `moduletype IN ('PrismAdjustableCardCarousel','PrismScrollableItemGrid')` |
| Standard WBR window | `session_start_dt BETWEEN [last Sat] AND [that Tue]` |
| Messaging WBR window | `session_start_dt BETWEEN [last Mon] AND [last Sun]` |

---

*Last updated by Keel Agent | Confirmed by: Ashraf (site content strategy team)*
