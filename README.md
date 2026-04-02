# 🧠 Keel Foundation Agent — Project README

> **Keel** is the brain agent powering homepage analytics intelligence at Walmart.  
> It understands the Homepage Performance ecosystem end-to-end and can answer complex analytical questions, build queries, explain metrics, and surface actionable insights — all grounded in real BigQuery data.

---

## 🚀 What Keel Can Do

Based on the [Keel Agent Workflows](https://confluence.walmart.com/pages/viewpage.action?spaceKey=RETAIL&title=Homepage+Analytics+101) framework:

| Capability | Description |
|-----------|-------------|
| **Task Decomposition** | Understands business questions and breaks them into sub-tasks |
| **Metric Calculation** | Knows how ATC, CTR, CPTS, GMV, SOV, and Activations are computed |
| **Query Generation** | Writes accurate, cost-conscious BigQuery SQL |
| **Pattern Recognition** | Identifies WoW trends, drops, spikes, and anomalies |
| **Multi-Table Analysis** | Joins across all 4 SCS tables to answer layered questions |
| **Insight Generation** | Goes beyond data to provide actionable business recommendations |

---

## 🗂️ Project Structure

```
keel-analytics/
├── README.md                                            ← You are here
├── datasets/
│   ├── HPsummary.md                                     ← PRIMARY reporting table (Content_Type='Merch' mandatory)
│   ├── hp_summary_asset.md                              ← Asset-level performance table (~53.4 GB)
│   ├── hp_session.md                                    ← Session-level denominator table (~10 MB)
│   ├── sov_hp_carousel_content.md                       ← Share-of-Voice carousel table (~13.6 GB)
│   ├── item_hp_scs.md                                   ← Item/product-level table (~685 GB) 🔴
│   ├── CVPsummary.md                                    ← CVP program table (2.32B rows, ~812 GB) 🔴🔴
│   └── metrics_definitions.md                           ← Full metrics glossary + sample queries
└── business_context/
    ├── message_shareout_context.md                      ← HPOV structure, card benchmarks, seasonal calendar,
    │                                                         message tiers, SIG, FY27 owners (6 share-out decks)
    └── homepage_buddy_knowledge.md                      ← Homepage Buddy agent capabilities, HPsummary formulas,
                                                              output conventions, Keel delegation pattern
```

---

## 📊 BigQuery Tables

All tables live in: **`wmt-site-content-strategy.scs_production`**

| Table | Size | Grain | Primary Use |
|-------|------|-------|------------|
| [`HPsummary`](./datasets/HPsummary.md) | TBD | Asset × Date × Platform | **PRIMARY** — WBR, CTR, GMV, Activations (requires `Content_Type='Merch'`) |
| [`hp_summary_asset`](./datasets/hp_summary_asset.md) | ~53.4 GB | Asset × Date × Platform | CTR, ATC, GMV, Activations (raw) |
| [`hp_session`](./datasets/hp_session.md) | ~10 MB | Platform × Date × Traffic Source | Session denominator for CPTS |
| [`sov_hp_carousel_content`](./datasets/sov_hp_carousel_content.md) | ~13.6 GB | Message × Carousel × Date | Share of Voice analysis |
| [`item_hp_scs`](./datasets/item_hp_scs.md) | ~685 GB | Item × Module × Date | Product-level attribution 🔴 |
| [`CVPsummary`](./datasets/CVPsummary.md) | ~812 GB/scan | Item × Module × Date | CVP program enrollment & outcomes 🔴🔴 |

> ⚠️ **Cost Warning:** Always filter `item_hp_scs` by `event_dt`. A full scan = hundreds of dollars.

---

## 🔑 Key Metrics Quick Reference

| Metric | Formula |
|--------|---------|
| **CTR** | `Clicks ÷ Viewed Impressions` |
| **CPTS** | `(Clicks ÷ HP Sessions) × 1,000` |
| **ATC Rate** | `ATC Clicks ÷ Viewed Impressions` |
| **GMV Per Impression** | `GMV ÷ Viewed Impressions` |
| **HP Visitation Rate** | `hp_session_count ÷ total_session_count` |
| **SOV** | `Asset Impressions ÷ Total HP Impressions` |

---

## 💡 Example Questions Keel Can Answer

1. *"What is the ATC rate for messages in CZ33 last week by platform?"*
2. *"Why did ATC drop yesterday? Which modules were the main drivers?"*
3. *"What's the SOV trend for the HOME SBU over the last 4 weeks?"*
4. *"Which carousel items drove the most GMV last week?"*
5. *"How are GMF activations trending WoW, and which modules are contributing?"*
6. *"Compare CTR between personalized vs default content on Android"*
7. *"What is our HP visitation rate by traffic source this week?"*

---

## 🧩 Keel's 7-Step Framework

*(From the Keel Agent Workflows document)*

1. **Decompose** — Break the user's question into actionable sub-tasks
2. **Knowledge Resource Planning** — Identify relevant tables, metrics, and docs
3. **Knowledge Retrieval** — Apply business context (glossary, metric logic, attribution rules)
4. **Execution** — Generate and run accurate BigQuery SQL
5. **Reasoning** — Synthesize results into insights aligned with business expectations
6. **Evaluation** — Score response completeness; identify gaps
7. **Reflection & Refinement** — Learn from feedback; improve over time

---

## 🏗️ Architecture

```
User Question
      │
      ▼
  Keel Agent (Brain)
      │
      ├─── Metrics Knowledge Base (metrics_definitions.md)
      ├─── Dataset Knowledge (datasets/*.md)
      ├─── BigQuery (4 SCS tables)
      │         ├── hp_session         (denominator)
      │         ├── hp_summary_asset   (asset performance)
      │         ├── sov_hp_carousel_content (SOV)
      │         └── item_hp_scs        (item-level)
      │
      └─── Insight Output → User / App
```

---

## 📚 Key Resources

- 📖 [Homepage Analytics 101 (Confluence)](https://confluence.walmart.com/pages/viewpage.action?spaceKey=RETAIL&title=Homepage+Analytics+101)
- 📊 Home Page Performance Dashboard
- 🗂️ BigQuery Project: `wmt-site-content-strategy`

---

## 🛣️ Roadmap

- [x] Dataset schema documentation (all 6 tables incl. HPsummary + CVPsummary)
- [x] Metrics definitions & glossary
- [x] Sample query library
- [x] Business context from 6 Message Share-Out decks (WK2–WK13 FY27)
- [x] HPOV card structure, CTR benchmarks, message tiers, SIG structure
- [x] FY27 seasonal calendar (Feb–May)
- [x] Homepage Buddy agent knowledge (capabilities, formulas, delegation pattern)
- [x] CVP program funnel and analysis patterns
- [ ] CVP dataset integration
- [ ] Traffic Sense integration
- [ ] Automated WoW report generation
- [ ] SBU-level SOV analysis with NLP/fuzzy matching for cross-category messages
- [ ] Item-level GMF activation drill-down

---

*Keel Agent v1.0 | Built for Walmart Site Content Strategy | 2025*
