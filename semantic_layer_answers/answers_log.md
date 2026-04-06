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
**ATF Definition:** content_zone IN ('contentZone1'–'contentZone6')
**Key Findings (CORRECTED — CZ1–CZ6 scope):**
- SIG Card 1: $8,862,573 GMV | GMV/click $1.25 — **#1 ATF driver**
- SIG Card 2: $1,109,948 GMV | GMV/click $1.00
- AutoScroll Card 1: $662,285 GMV | GMV/click $1.10
- P13N Item Carousel: $544,221 GMV | GMV/click null (clicks not captured in CZ1–6 scope)
- SIG Card 3: $502,998 GMV | GMV/click $0.95
- SIG Card 4: $238,520 GMV | GMV/click $1.02
- SIG Card 5: $107,247 GMV | GMV/click $0.89
- AutoScroll Card 2: $99,456 GMV | GMV/click $0.33
- AutoScroll Card 3: $76,470 GMV | GMV/click $0.32
- AutoScroll Card 5: $72,235 GMV | GMV/click $0.49
- AutoScroll Card 4: $69,946 GMV | GMV/click $0.61
- SIG Card 6: $56,082 GMV | GMV/click $0.67
- Merch Item Carousel: $42,235 GMV
**Key Insight:** P13N Item Carousel showed $18M GMV in first (wrong) query without CZ filter — dropped to
  $544K with correct ATF CZ1–6 scope. 97% of P13N GMV is actually BTF. SIG Card 1 alone ($8.86M)
  outperforms all 5 HPOV AutoScroll cards combined (~$980K).
**Data Quality Note:** atf_flag column is UNRELIABLE — tags ALL modules as 'BTF' including HPOV AutoScroll Cards.
  Use content_zone field (CZ1–CZ6 = ATF) for all ATF/BTF filtering.

**⚠️ CORRECTION (User Feedback):**
- ATF definition: Use content_zone field. contentZone1–contentZone6 = ATF. contentZone7+ = BTF.
- Do NOT use atf_flag column for ATF/BTF filtering — unreliable (tags all modules as BTF).
- Correct SQL filter: WHERE content_zone IN ('contentZone1','contentZone2','contentZone3','contentZone4','contentZone5','contentZone6')
- Excel: Keep formatting basic — no colors, simple table only.
- Metrics to report: GMV + GMV/click only (no CTR, impressions, clicks unless specifically asked).

---
