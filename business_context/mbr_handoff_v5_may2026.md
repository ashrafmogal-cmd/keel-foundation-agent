# MBR Knowledge Handoff — v5 (May 2026 Close)

> **Canonical reference for the June 2026 MBR session.** Source: `mbr_handoffs/mbr-knowledge-handoff-v5-may-2026-close.html`
> Author: Fola 📝 · Generated 2026-06-10 · Supersedes handoff v4. Update to v6 at June MBR close.

This digest is consumed by the **keel-mbr** agent. The full styled HTML lives in `mbr_handoffs/`.

---

## 1. Session Context
The May 2026 MBR was the **first MBR with the new Customer Cohort split** (live mid-May 2026, owned by Customer Strategy team). Captures ratified knowledge from the v11 → v16 iteration cycle; establishes the framework recurring from June 2026 MBR onward.

**Final artifact:** v16 at https://puppy.walmart.com/sharing/a0d0rlq/may-2026-mbr-homepage · 7 sections · director-approved · 5 version bumps post-initial.

---

## 2. The Big Story — Customer Cohort Split
Cohorts owned by Customer Strategy, based on **online purchase frequency (trailing year)**:

| Cohort | Definition | May SOV | Strategic Role |
|--------|-----------|---------|----------------|
| Weekly / Bi-Weekly | ≥24 unique purchase weeks/yr | 45.2% | 💎 Volume Driver (GOATs) |
| Casual | 2–11 unique purchase weeks/yr | 23.3% | Services over-indexer |
| Monthly | 12–23 unique purchase weeks/yr | 16.7% | 📈 Efficiency Driver |
| New To Walmart | 0 or 1 purchases | 14.8% | Acquisition funnel |

**May 2026 cohort snapshot:**

| Cohort | CTR | ATC/1K | GMV ($M) | ExpDel | GMF | OG |
|--------|-----|--------|----------|--------|-----|-----|
| Casual | 2.45% | 7.29 | $18.2 | 16,043 | 2,449 | 6,725 |
| Monthly | 3.34% | 10.34 | $17.9 | 4,831 | 173 | 54 |
| New To Walmart | 1.29% | 1.83 | $3.4 | 8,800 | 14,115 | 21,265 |
| Weekly/Bi-Weekly | 2.87% | 8.90 | $58.4 | 2,874 | 36 | 2 |
| **Blended** | 2.61% | 7.57 | $77.8 | 32,548 | 16,773 | 28,046 |

**Headline:** Monthly converts ~30%+ more efficiently per impression than blended but gets only 16.7% SOV — cleanest efficiency arbitrage on the page. Counterfactual: upweighting Monthly to 25% SOV → est. **+2–4M incremental ATC/month**.

---

## 3. Two Growth Engines Framework — LOCKED
- **📈 Monthly = Efficiency Driver** (16.7% SOV · 3.34% CTR · 10.34 ATC/1K) → *Reinforce the Value Proposition* (speed, pricing, W+ visibility, item-dense composition). Owner: **Home Page Features & Site Optimization**.
- **💎 Weekly/Bi-Weekly = Volume Driver / GOATs** (45.2% SOV · 2.87% CTR · $58.4M GMV) → *Maximize Engagement & Conversion on the Edges* (active content, dial up services, convert ATF tail + BTF). Owner: **Site Content Team**.
- **Casual** = Services over-indexer (49% of ExpDel on 23% SOV ≈ 2× over-index) → test services-creative concentration.
- **New To Walmart** = Acquisition funnel (84% GMF + 76% OG) → measure on GMF/OG rate, **never** CTR/ATC.

---

## 4. New MBR Structure — 7 Sections (Locked)
1. Executive Summary
2. Executive Roadmap Review
3. Business Performance — Headlines
4. **Customer Cohorts Strategy** (NEW: §4a snapshot table + §4b two-engine visual)
5. HPOV Deep Dive
6. SIG ATF Deep Dive
7. Appendix — Definitions

**Layout rule:** Cohorts always sit between Business Performance and HPOV. Definitions live in Appendix only — never duplicated in §4 footnote.

---

## 5. Methodology Locks Ratified
- **Cohort defs** (above). Casual floor = **2 weeks, not 1** (1-week would overlap NTW's "0 or 1").
- **Cohort snapshot column set (locked):** Cohort | SOV | Impressions | CPTS | CTR | ATC/1K | GMV ($M) | ExpDel | GMF | OG. `.kpi` table class, `.up` green-bold winners, `.grand-total` Blended row. Always include Casual + NTW even when narrative focuses on Monthly + W/BW.
- **Two-engine visual:** CSS Grid `1fr 1fr`, `align-items:stretch`; cards flex-column `border:2px`; stat row 3-col grid tabular-nums; persona `min-height:4.5em`; owner pill `margin-top:auto`. Themes: Monthly `#0053e2`/`#eff6ff`, W/BW `#b8860b`/`#fffbeb`.
- **Insight labels:** `Callout:` (inline) / `Takeaway:` (section-opener). AVOID `Read:` (deprecated).
- **Owner-team pills** on all strategic recs. Recurring owners: Home Page Features, Site Optimization, Site Content, Customer Strategy, WMC, W+ Team, Hero Carousel Product, Merch Ops, Marketing/SEO, Instrumentation Eng.

---

## 6. Director Feedback Patterns — May 2026
1. **"Move section before X"** → renumber downstream h2+h3 (4a/4b→5a/5b) + cross-refs; grep-verify.
2. **"Just create a good visual"** → one strong side-by-side visual over multi-table/list combos.
3. **"Align the table"** → CSS Grid `align-items:stretch` + `margin-top:auto` + `min-height`.
4. **"Combine cohorts/segments"** → update live tables AND Appendix defs same cycle.
5. **"Change the label"** → standalone version bump; replacement count == occurrence count.

---

## 7. Process Lessons
- Plan **5–7 director-edit cycles** per MBR.
- **File-based publish** for share-puppy (write→grep-verify→upload); paste-through introduces typos.
- One strong visual > three smaller assets for strategic dichotomies.
- Owner pills turn analysis into action.
- Cohort definitions belong in Appendix, not section narrative.
- CSS Grid + flex stretch = the alignment answer.
- Cross-check cohort boundaries for non-overlapping coverage.

---

## 8. Open Items / Pending Escalations
| # | Item | Owner | Status |
|---|------|-------|--------|
| 1 | Message × Cohort cross-tab | Fola / BA&I | Pending |
| 2 | Monthly upweight A/B test (+8.3 pts SOV) | Site Optimization | Pending |
| 3 | NTW attribution window validation | Instrumentation | Pending |
| 4 | Cohort migration tracking (Casual→Monthly) | Customer Strategy | Pending |
| 5 | Services-creative concentration test (Casual) | Site Content + WMC | Pending |
| 6 | June MBR baseline (first full-month cohort) | Fola | Planned |

---

## 9. June MBR Prep
- **Window:** June 1–30, 2026 (first full-month cohort baseline). Target publish early July.
- **Re-baseline:** cohort SOV trajectory, Monthly CTR/ATC, Casual ExpDel share, NTW GMF/OG rate, W/BW GMV share (~75%?).
- **Ask user at session start:** sitewide traffic May→June, WMC ad revenue $, W+ sign-up rate June (HPOV/Banner/Combined), SOV bps, eng ticket status, cohort methodology adjustments.
- **Pre-flight:** reconcile May anchors (impressions, CPTS, ATC, GMV); verify cohort field availability in `hp_summary_asset` (or cohort-mapping join).
- **§4 standing template:** 4a snapshot (10-col) + 4b two-engine (Monthly + W/BW headline, Casual + NTW footnoted); optional 4c diagnostic.

---

## 10. SQL Patterns Added (cohort)
**Q-COHORT-SNAPSHOT** — Customer Cohort Performance:
```sql
SELECT
  customer_cohort,
  SUM(module_view_count) AS impressions,
  SAFE_DIVIDE(SUM(overall_click_count), SUM(hp_session_count)) * 1000 AS cpts,
  SAFE_DIVIDE(SUM(overall_click_count), SUM(module_view_count)) * 100 AS ctr_pct,
  SAFE_DIVIDE(SUM(total_atc_count), SUM(module_view_count)) * 1000 AS atc_per_1k,
  SUM(total_gmv) AS gmv,
  SUM(exp_del_activation_flag) AS exp_del,
  SUM(gmf_activation_flag) AS gmf,
  SUM(og_activation_flag) AS og
FROM `wmt-site-content-strategy.scs_production.hp_summary_asset`
WHERE session_start_dt BETWEEN '<start>' AND '<end>'
  AND experience_lvl2 IN ('App: iOS','App: Android','Web: Desktop','Web: Mobile')
  AND IFNULL(moduletype,'') NOT IN ('InteractiveImageCarousel','socialCarouselV2')
GROUP BY customer_cohort;
```
- **Q-COHORT-MESSAGE** — group by (customer_cohort, message_name), top 20 by blended impressions → which messages over-index per cohort.
- **Q-COHORT-MOM** — same as snapshot with month-bucket CASE → May vs June drift.

> ⚠️ **Verify** `customer_cohort` column exists in `hp_summary_asset` (else join to a cohort-mapping table) as a pre-flight step.

---

## 11. Cross-Reference (MBR ↔ WBR)
- WBR→MBR: Card1 W+/Non-W+ decomp, Web Desktop YoY bot-cleanup framing, ItemCarousel concentration, Merch-only HPOV exclusion set.
- MBR→WBR: Cohort framework mini-table in WBR §2 (June 2026+), two-engine owner accountability, cohort SOV drift watch item.
- Both: asymmetric IIC (clicks ex-IIC / activations with-IIC); driver attribution column; 5–7 edit cycles.

---

## 12. Reference URLs
- Final MBR v16: https://puppy.walmart.com/sharing/a0d0rlq/may-2026-mbr-homepage
- Prior handoff v4: https://puppy.walmart.com/sharing/a0d0rlq/mbr-knowledge-handoff-v4
- WBR handoff v11 (WK18): https://puppy.walmart.com/sharing/a0d0rlq/handoff-v11-wk18-2026-wbr-close
- FY27 Homepage Goals.xlsx (GUID `3cab877d-78d0-4680-a6f1-264036b2cfb3`)
