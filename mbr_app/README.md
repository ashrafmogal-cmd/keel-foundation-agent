# mbr_app — Monthly Business Review (MBR) Assets

This folder holds everything the **Keel** agent needs to generate Monthly Business
Review reports. MBR generation is a **built-in capability of Keel** (not a separate
agent) — a user simply asks Keel: *"run the MBR report for <Month> <Year>"*.

## Contents
| File | Purpose |
|------|---------|
| `mbr_agent_guide.md` | Workflow, architecture, methodology, and report-engine guide |
| `mbr_handoff_v5_may2026.md` | Canonical knowledge digest from the May 2026 MBR close (cohort split, two-engine framework, June prep, open items, cohort SQL) |
| `handoffs/` | Source handoff HTML files (one per cycle; add v6, v7… here over time) |
| `may_mbr_v5_reference.py` | Proven HTML report generator — reuse its helpers/structure for any month |
| `april2026_nav_mbr_baseline.html` | CSS/style baseline inherited by the generator |

## How Keel Uses This
1. At MBR session start, Keel reads `mbr_agent_guide.md` + the latest `mbr_handoff_*.md`.
2. It queries BigQuery live for the requested month (MoM/YoY), drafts insights,
   and asks the user for non-BQ inputs.
3. It generalizes `may_mbr_v5_reference.py` to build the branded HTML report.

## Adding a New Cycle
- Drop the new handoff HTML into `handoffs/`.
- Add a `mbr_handoff_vN_<month><year>.md` digest alongside it.
- Update Keel's pointers if the canonical handoff version changes.
