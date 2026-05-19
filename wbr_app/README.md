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
| HPOV (Cards 1–5) | CTR%, CTR WoW%, Clicks%, Clicks WoW%, ATC%, ATC WoW% |
| ATF Carousels (SIG) | Same |
| ATF Carousels | Same |
| Walmart+ Banner | Same |
| Utility | Same |
| BTF Navigation | Same |
| BTF Content | Same |
| BTF Carousels | Same |

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
