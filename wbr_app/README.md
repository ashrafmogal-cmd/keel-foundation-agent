# 📊 WBR App — Weekly Business Review Dashboard

> **Included with the Keel Agent.** Just ask Keel: *"Open the WBR app for May 12"* and it handles everything automatically.

---

## 🚀 How to Launch (via Keel — Recommended)

Open Code Puppy, switch to the Keel agent, and say:

```
Open the WBR app for this week
```
or
```
Launch the WBR dashboard for May 12, 2026
```

Keel will:
1. Check if the server is already running
2. Set up the Python environment if needed (first time only)
3. Install dependencies automatically
4. Start the server and open Chrome to the right URL

---

## 🖥️ Manual Launch (if needed)

```bash
cd ~/keel-analytics/wbr_app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Then open: **http://127.0.0.1:8001**

---

## 🗓️ Date Selection

The app takes a `selected_date` URL parameter (any day of the fiscal week):

```
http://127.0.0.1:8001/?selected_date=2026-05-12
```

- The app automatically calculates the **Walmart fiscal week** (Saturday → selected day)
- Previous week is auto-calculated for WoW comparisons
- You can also select the date from the date picker inside the app

---

## 📋 What It Shows

| Module | Metrics |
|--------|---------|
| HPOV (Cards 1–5) | CTR Baseline, CTR%, CTR WoW%, ATC Rate Baseline, ATC Rate, ATC Rate WoW%, Engagement Performance |
| SIG | Same |
| Item Carousel | Same |
| Navigation | Same |
| Content | Same |
| Carousels | Same |
| Utility | Same |

### Metric Definitions

| Metric | Formula | Display |
|--------|---------|----------|
| **CTR Baseline** | FYTD CTR (Jan 31 → latest date) | `0.21%` |
| **CTR%** | Current week CTR | `0.19%` |
| **CTR WoW%** | vs previous fiscal week | `+5%` / `-3%` |
| **ATC Rate Baseline** | FYTD ATCs per 1,000 impressions | `12.3` (no %) |
| **ATC Rate** | Current week ATCs per 1,000 impressions | `11.8` (no %) |
| **ATC Rate WoW%** | vs previous fiscal week | `+2%` / `-4%` |
| **Engagement Performance** | (CTR% / CTR Baseline) × 100 | `92%` |

### Engagement Performance Color Coding

| Color | Range | Meaning |
|-------|-------|---------|
| 🟢 Green | ≥ 100% | At or above FYTD baseline |
| 🟡 Yellow | 90–99% | Approaching baseline, watch closely |
| 🔴 Red | < 90% | Significantly below baseline |

---

## ⚙️ Prerequisites

- ✅ BigQuery auth set up (`/bigquery_auth` in Code Puppy)
- ✅ Access to `wmt-site-content-strategy` project
- ✅ Python 3.9+ installed

---

## 🔧 Stop the Server

```bash
lsof -ti:8001 | xargs kill -9
```

---

## 📦 Dependencies

```
fastapi, uvicorn, google-cloud-bigquery, pandas, jinja2, matplotlib, python-pptx, openpyxl
```

*Internal Walmart use only — Keel Agent v1.0 | Site Content Strategy*
