# 🏠 Homepage Buddy — Agent Knowledge Transfer
## Keel Agent Knowledge Base | Integrated Agent Intelligence

*Source: Homepage Buddy agent system prompt (marketplace: https://puppy.walmart.com/marketplace/homepage-buddy)*  
*Maintained by: Keel Agent*

---

## 🧭 What Homepage Buddy Does

Homepage Buddy is a specialized analytics agent originally built around the **`HPsummary` table** — however, **the team has since moved to `hp_summary_asset` as the primary dashboard table**. When delegating to Homepage Buddy, confirm which table it is querying and override to `hp_summary_asset` if needed.

> ⚠️ **Table Correction:** `hp_summary_asset` is now the live dashboard table. `HPsummary` is legacy. Keel should default all new analysis to `hp_summary_asset`.
- Answers HP performance questions in plain English
- Generates Excel tables saved to `~/Desktop/clickfather/`
- Creates PowerPoint charts with Walmart blue styling
- Handles fuzzy module/message name matching
- Supports WBR, daily trends, WoW, YoY, and module comparisons

Keel can **invoke Homepage Buddy** for output generation tasks (Excel, PPT) while handling the analytical reasoning layer itself.

---

## 📊 Applications Homepage Buddy Powers

| App | Description |
|-----|-------------|
| **WBR App** | Weekly Business Review — WoW metrics by platform, module, message |
| **HP Performance Charts** | Daily/weekly CTR, impressions, GMV, ATC trend charts |
| **Module Performance App** | Per-module CTR, GMV, activation benchmarks |
| **Bubble Charts** | Multi-metric scatter (e.g. CTR vs GMV by message) |
| **Bar Charts** | Module/message comparison charts |
| **Message Comparison** | Side-by-side performance across messages/creative assets |

---

## 🔑 Critical Knowledge from Homepage Buddy

### The Mandatory Filter — NEVER Forget This
```sql
WHERE Content_Type = 'Merch'
-- This filter is ALWAYS applied. Without it, data includes non-merch content and is incorrect.
```

### Platform Naming Gotcha
```sql
-- HPsummary uses NO SPACE after colon:
experience_lvl2 IN ('App:iOS', 'App:Android')

-- hp_summary_asset uses SPACE after colon:
experience_lvl2 IN ('App: iOS', 'App: Android')
```

### Click Column Disambiguation
| Table | Clicks Column | Notes |
|-------|--------------|-------|
| `HPsummary` | `overall_click_count` | Primary CTR numerator |
| `hp_summary_asset` | `overall_click_count` | Primary CTR numerator |
| Both tables | `all_clicks_count_flag` | Used for Asset Exit Rate only |

### Asset Exit Rate Formula
```sql
(1 - SAFE_DIVIDE(SUM(all_clicks_count_flag), SUM(asset_clicks_count))) * 100 AS asset_exit_rate
```
This measures: *% of HP sessions where the user left without any subsequent engagement*

### Services Activations — Use COALESCE
```sql
SUM(COALESCE(subs_activations, 0) + COALESCE(acc_activations, 0)) AS services_activations
```

---

## 📋 All Metrics Formulas (HPsummary-specific)

| Metric | SQL Formula |
|--------|-------------|
| Impressions | `SUM(viewed_impressions)` |
| Clicks | `SUM(overall_click_count)` |
| CTR | `SAFE_DIVIDE(SUM(overall_click_count), SUM(viewed_impressions)) * 100` |
| GMV | `SUM(total_gmv)` |
| GMV per 1M Impressions | `SAFE_DIVIDE(SUM(total_gmv), SUM(viewed_impressions)) * 1000000` |
| Add to Cart | `SUM(total_atc_count)` |
| ATC Rate | `SAFE_DIVIDE(SUM(total_atc_count), SUM(viewed_impressions)) * 100` |
| GMF Activations | `SUM(gmf_activations)` |
| Services Activations | `SUM(COALESCE(subs_activations,0) + COALESCE(acc_activations,0))` |
| Express Delivery Activations | `SUM(exp_del_activations)` |
| Rx Activations | `SUM(rx_activations)` |
| Asset Exit Rate | `(1 - SAFE_DIVIDE(SUM(all_clicks_count_flag), SUM(asset_clicks_count))) * 100` |

---

## 📐 All Dimensions Available in HPsummary

### Module Dimensions
| Column | Use Case |
|--------|---------|
| `hp_module_name` | **USE THIS FIRST** for module filtering |
| `hp_module_type` | Broad module type |
| `moduleType` | Technical module type |
| `modulename` | Full name with date/zone prefix |

### Message Dimensions
| Column | Use Case |
|--------|---------|
| `message_name` | Campaign/message name |
| `message_id` | Unique identifier — use for precise filtering |
| `message_owner` | Owner person/team |
| `message_sponsor` | Sponsoring SBU |
| `message_type` | SEASONAL, HOLIDAY, etc. |

### Other Key Dimensions
| Column | Use Case |
|--------|---------|
| `Carousel_Name` | Carousel-level grouping |
| `m0_Nm` → `m4_nm` | 5-level product category hierarchy |
| `asset_heading` | Asset creative text |
| `Content_Zone` | HP slot/zone |
| `Module_Group` | Content vs Commerce |
| `traffic_source_lvl2` | Traffic source |
| `SBU` | Strategic Business Unit |
| `content_zone` | ATF = contentZone1–6 (App), contentZone7–27 (Desktop). Use this for ATF/BTF filtering. |
| `atf_flag` | ⚠️ UNRELIABLE — atf_flag tags all Desktop rows as BTF. Never use for ATF filtering. |
| `atf_location` | ⚠️ Do NOT use for ATF filtering — use content_zone values instead. |
| `Prism_Module` | Prism design system |
| `default_shown` | Default vs personalized |
| `personalized_asset` | Personalization flag |
| `language_split` | English vs Spanish |

### Date Dimensions (all 12)
`session_start_dt`, `cal_month_name`, `cal_month_nbr`, `cal_week_nbr`, `cal_week_nbr_mon`, `cal_qtr_name`, `cal_qtr_nbr`, `cal_yr_nbr`, `fiscal_week_nbr`, `fiscal_month_nbr`, `fiscal_qtr_nbr`, `fiscal_yr_nbr`

---

## 🤖 Fuzzy Module Matching Pattern

When a user gives a partial module name, run this first:
```sql
SELECT DISTINCT hp_module_name
FROM `wmt-site-content-strategy.scs_production.HPsummary`
WHERE Content_Type = 'Merch'
  AND hp_module_name LIKE '%[USER_INPUT]%'
LIMIT 10
```
Then show options and confirm before running the main query.

---

## 📤 Output File Conventions

| Output Type | Path | Filename Format |
|------------|------|-----------------|
| Excel | `~/Desktop/clickfather/` | `hp_data_YYYYMMDD_HHMMSS.xlsx` |
| PowerPoint | `~/Desktop/clickfather/` | `hp_chart_YYYYMMDD_HHMMSS.pptx` |

### Walmart Brand Colors
| Color | Hex | Use |
|-------|-----|-----|
| Walmart Blue | `#0071CE` | Primary charts, lines |
| Walmart Yellow | `#FFC220` | Secondary, highlights |
| Walmart Green | `#76C043` | Positive trend |
| Walmart Red | `#E31837` | Negative trend, alerts |

---

## 🔄 How Keel Should Use Homepage Buddy

Keel can invoke Homepage Buddy for execution while retaining the analytical reasoning layer:

```
User Question (analytical/strategic)
        ↓
    KEEL (brain)
    - Understands the question
    - Applies business context
    - Identifies the right table, filters, metric
    - Adds HPOV card benchmarks, seasonal context
        ↓
    invoke_agent("homepage-buddy", specific_query_prompt)
    - Executes the SQL
    - Generates Excel/PPT output
        ↓
    KEEL returns insight with context
```

**When to delegate to Homepage Buddy:**
- User wants Excel/PowerPoint output files
- User wants styled charts (Walmart blue)
- HPsummary-specific queries with `Content_Type = 'Merch'`

**When Keel handles directly:**
- Complex multi-table analysis
- CVP program analysis (CVPsummary)
- Item-level deep dives (item_hp_scs)
- SOV analysis (sov_hp_carousel_content)
- Strategic/comparative reasoning

---

## 💡 Example Prompts for Keel → Homepage Buddy Delegation

```python
invoke_agent(
    agent_name="homepage-buddy",
    prompt="Generate an Excel file with CTR, impressions, and GMV for all modules in iOS+Android for the week of 2026-02-09 to 2026-02-15. Group by hp_module_name."
)

invoke_agent(
    agent_name="homepage-buddy",
    prompt="Create a PowerPoint line chart showing daily CTR trend for 'Scrollable Item Grid Card 1' from 2026-01-01 to 2026-03-31 on iOS+Android apps."
)
```

---

*Last updated by Keel Agent | Source: Homepage Buddy agent system prompt (marketplace agent)*
