# Keel Semantic Layer — Q&A Answer Log

This file logs questions asked to Keel and the key findings from each answer.
Used for learning, pattern recognition, and stakeholder reference.

---

## Q1 — Daily HP Sessions (Mar 1–7, 2026)
**Asked:** What are the daily sessions on homepage from 3/1 to 3/7?
**Table:** wmt-site-content-strategy.scs_production.hp_session
**Platforms:** App: iOS + App: Android
**Key Findings:**
- Sunday 3/1 peaked at 26,715,070 sessions (weekend surge, +16% vs weekday avg)
- Weekday average: ~23,207,000 sessions/day
- Saturday 3/7: 25,526,037 sessions
- HP Visitation Rate: stable at 80.53%–80.94% across all 7 days
- iOS = ~73% of HP sessions, Android = ~27%
- Week aligns with March Savings Event (WK8 FY27, 95% Card 1 SOV)
- Total weekly sessions: 168,474,712
**Data Quality Note:** None. hp_session is a clean, small table (~10MB).

---

## Q2 — ATF Module GMV (Feb 1–14, 2026)
**Asked:** Which modules in ATF are driving the most GMV for 2/1 to 2/14?
**Table:** wmt-site-content-strategy.scs_production.hp_summary_asset
**Platforms:** App: iOS + App: Android
**Key Findings:**
- P13N Item Carousel = #1 ATF GMV driver by a massive margin: $18,073,685 (95% of all ATF GMV)
  - CTR: 6.64% | GMV/impression: $0.2358 | GMV/click: $3.55
- AutoScroll Card 1 = #2 at $662,285 GMV | CTR: 0.18% (below 0.23% benchmark)
- AutoScroll Card 2 = $99,456 | CTR: 0.11% (below 0.15% benchmark)
- AutoScroll Card 3 = $76,470 | CTR: 0.10% (below 0.13% benchmark)
- AutoScroll Card 5 = $72,235 | CTR: 0.22% (below 0.25% benchmark)
- AutoScroll Card 4 = $69,946 | CTR: 0.14% (below 0.17% benchmark)
- Amend Banner + OST = 0 GMV (operational modules — no purchase attribution expected)
- All HPOV cards below benchmark during Valentine's Day period (Feb 1-14)
**Data Quality Note:** atf_flag column is UNRELIABLE — tags ALL modules as 'BTF' including HPOV AutoScroll Cards.
  Use known module names/moduletype values for ATF filtering instead.
  AutoScroll Cards 6–10 exist in data (anomaly — should only be Cards 1-5).

**⚠️ CORRECTION (User Feedback):**
- ATF definition: Use content_zone field. contentZone1–contentZone6 = ATF. contentZone7+ = BTF.
- Do NOT use atf_flag column for ATF/BTF filtering — unreliable (tags all modules as BTF).
- Correct SQL filter: WHERE content_zone IN ('contentZone1','contentZone2','contentZone3','contentZone4','contentZone5','contentZone6')
- Excel: Keep formatting basic — no colors, simple table only.
- Metrics to report: GMV + GMV/click only (no CTR, impressions, clicks unless specifically asked).

---
