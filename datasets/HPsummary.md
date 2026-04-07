# HPsummary — DEPRECATED / DO NOT USE

## ⛔ HARD RULE: NEVER USE HPsummary TABLE

The HPsummary table is permanently off-limits for ALL queries. This is a non-negotiable rule.
- Do NOT use HPsummary for Merch queries
- Do NOT use HPsummary for WMC/Ads queries
- Do NOT use HPsummary for any analysis
- Always use hp_summary_asset instead

Any documentation about HPsummary WMC Content_Type filters written previously is INVALID and superseded by this rule.

## Why It Was Deprecated
The team moved away from HPsummary. hp_summary_asset is the current source of truth for all homepage performance data.

## What to Use Instead
→ hp_summary_asset for ALL module/asset/message/WMC performance
→ hp_session for session denominator / CPTS
→ sov_hp_carousel_content for Share of Voice / carousel
→ item_hp_scs for item/product level (filter event_dt!)
→ CVPsummary for CVP program analysis (filter event_dt!)
