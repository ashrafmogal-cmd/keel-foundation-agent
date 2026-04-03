# 🧠 Keel Foundation Agent — Project README

> **Keel** is the brain agent powering homepage analytics intelligence at Walmart.  
> Defined in the FY27 Analytics Roadmap as: *"A site merchandising analytics expert that uses agentic workflows to deliver trusted, on-demand insights grounded in data and business context."*  
> Keel is a **Q1 FY27 initiative** — the foundation layer for all self-service analytics agents to follow.

---

## 🚀 What Keel Can Do

Based on the [Keel Agent Workflows](https://confluence.walmart.com/pages/viewpage.action?spaceKey=RETAIL&title=Homepage+Analytics+101) framework:

| Capability | Description |
|-----------|-------------|
| **Task Decomposition** | Understands business questions and breaks them into sub-tasks |
| **Metric Calculation** | Knows how ATC, CTR, CPTS, GMV, SOV, and Activations are computed |
| **Query Generation** | Writes accurate, cost-conscious BigQuery SQL |
| **Pattern Recognition** | Identifies WoW trends, drops, spikes, and anomalies |
| **Multi-Table Analysis** | Joins across all 6 SCS tables to answer layered questions |
| **Insight Generation** | Goes beyond data to provide actionable business recommendations |

---

## 🗂️ Project Structure

```
keel-analytics/
├── README.md                                            ← You are here
├── datasets/
│   ├── hp_summary_asset.md                              ← ✅ PRIMARY dashboard table (~53.4 GB)
│   ├── HPsummary.md                                     ← ⚠️ LEGACY table (moved away from)
│   ├── hp_session.md                                    ← Session-level denominator table (~10 MB)
│   ├── sov_hp_carousel_content.md                       ← Share-of-Voice carousel table (~13.6 GB)
│   ├── item_hp_scs.md                                   ← Item/product-level table (~685 GB) 🔴
│   ├── CVPsummary.md                                    ← CVP program table (2.32B rows) 🔴🔴
│   └── metrics_definitions.md                           ← Full metrics glossary + sample queries
└── business_context/
    ├── message_shareout_context.md                      ← HPOV structure, card benchmarks, seasonal calendar,
    │                                                         message tiers, SIG, FY27 owners (6 share-out decks)
    ├── homepage_buddy_knowledge.md                      ← Homepage Buddy capabilities, formulas, delegation pattern
    ├── agentic_workflow.md                              ← 8-step protocol, self-check lists, FY27 roadmap
    ├── message_tiering.md                               ← Full tiering framework: 4 factors, decision trees,
    │                                                         card SOV, all 100+ named messages + tier outcomes
    ├── msp_training.md                                  ← MSP process: message types, M0–M4 hierarchy,
    │                                                         MMUI flow, ATF eligibility, personas, timeline
    ├── hpov_shareout_nov_dec_jan_2026.md                ← 6 weekly share-out decks (WK42 Nov 2025 – WK01 FY27):
    │                                                         card rotations, AE2/Cyber Monday, holiday takedown,
    │                                                         NYNY, Valentine’s Day, Super Bowl, brand launches
    ├── sig_playbook.md                                  ← SIG Message Playbook: eligibility, asset requirements,
    │                                                         ATF/BTF strategy, P13N, 10-step process, active themes
    ├── reporting_conventions.md                         ← ⚠️ CRITICAL: Fiscal week (Sat–Fri), WBR windows
    │                                                         (Std: Sat–Tue | Msg: Mon–Sun), hp_module_name +
    │                                                         moduletype mappings for HPOV & SIG, SQL filters
    └── wmc_wplus_ost_amend.md                           ← WMC ads (Cards 2&3, ~92% sold), merch vs ads P&L,
                                                              W+ member states & targeting (soft/hard/override),
                                                              OST CTR=3.41-4.6%, Amend CTR=7.73% (highest ATF),
                                                              Timers, ATF CTR hierarchy, module discovery query
```

---

## 📊 BigQuery Tables

All tables live in: **`wmt-site-content-strategy.scs_production`**

| Table | Size | Grain | Primary Use |
|-------|------|-------|------------|
| [`hp_summary_asset`](./datasets/hp_summary_asset.md) | ~53.4 GB | Asset × Date × Platform | ✅ **PRIMARY DASHBOARD TABLE** — WBR, CTR, GMV, Activations |
| [`HPsummary`](./datasets/HPsummary.md) | TBD | Asset × Date × Platform | ⚠️ LEGACY — team has moved away from this, use hp_summary_asset |
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
| **ATC Rate** | `(ATC Clicks ÷ Viewed Impressions) × 1,000` |
| **GMV Per Impression** | `GMV ÷ Viewed Impressions` |
| **GMV Per Click** | `GMV ÷ Clicks` |

---

## 💡 Example Questions Keel Can Answer

1. *"What is the ATC rate for messages in CZ3 last week by platform?"*
2. *"Why did ATC drop yesterday? Which modules were the main drivers?"*
3. *"What's the SOV trend for the HOME SBU over the last 4 weeks?"*
4. *"Which carousel items drove the most GMV last week?"*
5. *"How are GMF activations trending WoW, and which modules are contributing?"*
6. *"Compare CTR between personalized vs default content on Android"*
7. *"What tier is Valentine's Day and what placement does it get?"*
8. *"What is the holiday gifting takedown time on Dec 24?"*
9. *"What are the SIG eligibility requirements and what assets does the parent message need?"*
10. *"What messages were live in WK50 (Jan 10-16) and what was the approved rotation?"*
11. *"What CTR benchmark should I use for Card 5, and does it exclude deals events?"*
12. *"What's the GMV per click for the Game Time module last Super Bowl week?"*

---

## 🔄 Keel's 8-Step Agentic Workflow

*(From FY27 Analytics Roadmap, Slide 2)*

Every query flows through all 8 steps — non-negotiable:

| Step | Name | What It Does |
|------|------|--------------|
| 1 | **Decompose Tasks** | Break question into metric, table, date, platform, grain, comparison |
| 2 | **Plan Knowledge Sources** | Map to the right table(s) before touching data |
| 3 | **Retrieve Knowledge** | Pull schema, benchmarks, seasonal context, attribution rules |
| 4 | **Execute** | Write + run cost-conscious BigQuery SQL with all mandatory filters |
| 5 | **Reasoning** | Interpret results in business terms with benchmark context |
| 6 | **Evaluate** | Self-check — numbers plausible? filters applied? senior analyst would trust this? |
| 7 | **Reflect** | Did I answer the RIGHT question? What's missing? Anticipate follow-up. |
| 8 | **Refine** | Fix, improve, add caveats — never output what you wouldn't stake credibility on |

**→ Output: Trusted. On-demand. Grounded in data and business context.**

Full detail: [`business_context/agentic_workflow.md`](./business_context/agentic_workflow.md)

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

## 🚀 FY27 Roadmap — Keel's Place

| Quarter | Agent/Initiative | Status |
|---------|-----------------|--------|
| **Q1** | **Homepage Keel Agent** — Foundation agent for homepage domain with semantic data layer | ✅ **IN PROGRESS** |
| **Q2** | Homepage Buddy Chatbot — Self-service chatbot powered by Keel | 🔜 |
| **Q2** | Msg Performance Keel Agent — Foundation agent for message domain | 🔜 |
| **Q3** | C&E Keel Agent, Message Performance Chatbot, Event Recap Agent | 🔜 |
| **Q3** | CVP Brand Audit Agent, Data Anomaly Detection Agent, C&E Dashboard | 🔜 |
| **Q4** | TrafficSense Chatbot, P13N Explainability, Feature Launch Decision Framework | 🔜 |

**Business Outcome:** Eliminate ad-hoc analytics requests → free up analytics resources for strategic work.

**Next Major Milestone:** Evaluation phase — Keel answers a test set of questions, analyst evaluates accuracy of answers + SQL + reasoning, feedback loop improves trust until answers can be shared directly with stakeholders without human QA.

---

*Keel Agent v1.0 | Built for Walmart Site Content Strategy | 2025*
