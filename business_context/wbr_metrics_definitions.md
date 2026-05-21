# WBR App — Metrics Definitions & Calculation Logic
> Source of truth for WBR App (port 8001) and Charts App (port 8002)
> File: ~/keel-analytics/business_context/wbr_metrics_definitions.md

---

## CTR Baseline (FYTD)
- **Definition:** FYTD (Fiscal Year to Date) CTR, Jan 31 2026 → max available date in dataset
- **Formula:** `SUM(overall_click_count) / SUM(module_view_count) * 100`
- **Table:** `hp_summary_asset` | Filter: Merch only (canonical CASE expression)
- **Constant:** `FYTD_START = "2026-01-31"` (hardcoded in both apps)
- **FYTD end:** `SELECT MAX(session_start_dt) FROM hp_summary_asset WHERE session_start_dt >= FYTD_START`
- **HPOV benchmark value:** ~0.21% (blended, spans pre+post MM SIG launch May 14 2026)

## WoW CTR
- **Formula:** `(current_ctr / fytd_ctr - 1) * 100`
- Compares current partial-week CTR to the FULL FYTD average (NOT prior week)
- Green if > 0, Red if < 0

## ATC Rate Baseline (FYTD)
- **Definition:** FYTD ATC Rate — ATCs per 1000 impressions
- **Formula:** `SUM(total_atc_count) / SUM(module_view_count) * 1000`
- **Display:** One decimal, NO % sign (e.g., `12.3` not `12.3%`)
- This is a RATE metric, not a share/contribution %

## WoW ATC Rate
- **Formula:** `(current_atc_rate / prev_week_atc_rate - 1) * 100`
- Compares current week's ATC Rate vs previous fiscal week's ATC Rate
- Green if > 0, Red if < 0

## Engagement Performance
- **Definition:** How current CTR compares to FYTD baseline
- **Formula:** `CTR% / CTR Baseline * 100` = `(curr_ctr / fytd_ctr) * 100`
- **Display:** Whole number with % sign (e.g., `92%`)
- **Color coding:**
  - 🟢 **Green:** >= 100% (at or above FYTD baseline)
  - 🟡 **Yellow/Amber:** 90-99% (approaching baseline, watch closely)
  - 🔴 **Red:** < 90% (significantly below baseline)

## Module Bucketing (WBR App port 8001)
Uses `hp_module_name` as PRIMARY key (unchanged by MM SIG launch):
- `HPOV`: AutoScroll Card 1-5, contentzone1-6
- `SIG`: SIG Card 1-6, contentzone1-6
- `Item Carousel`: moduletype = ItemCarousel, contentzone1-6
- `Navigation`: hp_module_type = Navigation, BTF zones
- `Content`: hp_module_type = Content, BTF zones
- `Carousels`: hp_module_type = Carousel, BTF zones
- `Utility`: hp_module_type = Utility, any zone
- **Excluded always:** VideoCarousel, InteractiveImageCarousel

## MM SIG Launch Impact on Baselines
- MM SIG launched May 14 2026 (Thursday night)
- HPOV moved: contentzone3 → contentzone2
- SIG Top Picks moved: contentzone4/5/6 → contentzone3
- FYTD baselines span PRE+POST MM SIG → blended averages
- Any spike/drop after May 15 2026 → attribute to MM SIG first

## SOV (Share of Voice) — Messaging Table (Charts App port 8002)
- **HPOV SOV:** `message_impressions / total_hpov_impressions * 100`
- **SIG SOV:** built at `carousel_name` level: `carousel_imps / total_sig_imps * 100`
- **SOV Projected:** user-entered in the table. Used to compute variance.
- **SOV Variance:** `SOV Actual - SOV Projected` (green if positive, red if negative)

## SIG Table — carousel_name Logic (Charts App)
- If `carousel_name LIKE '%Top Pick%'` OR `LIKE '%Jump Right Back%'`:
  → show `asset_heading` as the row label (P13N personalized content)
- Otherwise:
  → show `message_name` as row label (site merch editorial content)
- **P13N Grand Total row**: aggregates ALL Top Picks impressions/clicks/CTR into one summary
- SOV is built at carousel_name level, not individual message level
- User can add projected SOV to the P13N grand total row independently

## CTR Green/Red Coloring (Messaging Table)
- CTR cell is GREEN if `message_ctr >= fytd_baseline_ctr`
- CTR cell is RED if `message_ctr < fytd_baseline_ctr`
- FYTD baseline shown in its own column for reference

## Language Filter
- **UI label:** Language
- **HPsummary column:** `language_split` (values: 'English', 'Spanish')
- **hp_summary_asset column:** `lang_cd` (values: 'English', 'Spanish')
- **Default:** English
- **Options in UI:** English | Spanish | All

## Platform Default
- CTR / ATC / GMV default: App iOS + App Android
- HPsummary: 'App:iOS', 'App:Android' (NO space after colon)
- hp_summary_asset: 'App: iOS', 'App: Android' (WITH space after colon)

---
*Last updated: 2026-05-19 | Keel Analytics | ATC Rate + Engagement Performance updates*
