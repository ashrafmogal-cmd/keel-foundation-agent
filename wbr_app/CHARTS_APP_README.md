# 📊 HP Charts App — Homepage Performance Visualizations

> **Port 8002** | Included with Keel. Just ask: *"Open the charts app for May 12"*

---

## 🚀 How to Launch (via Keel — Recommended)

```
Open the HP charts app for this week
Show me the bar charts for May 12
Launch the bubble chart dashboard
```

Keel calls `system.launch_charts_app` automatically — sets up the environment, starts the server, opens Chrome.

---

## 🖥️ Manual Launch

```bash
cd ~/keel-analytics/wbr_app
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python message_performance.py
```

Then open: **http://127.0.0.1:8002**

---

## 📈 What the App Shows

### 1. HPOV Bar Chart (AutoScroll Cards 1–5)
| Element | Description |
|---------|-------------|
| Bars | Impressions per message (in millions) |
| CTR Line | Click-through rate % overlay per message |
| SOV Badges | Colored horizontal line spanning each M0 group + SOV% + Projection% |
| Benchmark | Yellow dashed line (Feb 1–Mar 3 baseline CTR) |
| Groups | Color-coded by M0 campaign (Rollbacks, Easter, Services, etc.) |
| Includes | Sponsored Ads (WMC) as its own group |

### 2. SIG Bar Chart (SIG Cards 1–6)
Same format — groups: Top Picks, Rollbacks & More, CYS, Price Drop

### 3. HPOV Bubble Chart
| Axis | Metric | Direction |
|------|--------|-----------|
| X | ATC Rate (per 1K impressions) | Higher → better |
| Y | Exit Rate % (inverted) | Lower ↑ better |
| Size | Total impressions | Larger = more reach |

**Quadrants:** 🟢 Top Performer (high ATC, low exit) · 🔴 Low Performer · ⚫ Neutral

### 4. SIG Bubble Chart
Same format but X-axis = CTR %

---

## 🗓️ Fiscal Week Logic
- Walmart week: **Saturday → selected day**
- Select any day of the week — app auto-calculates the full week range + prior week for WoW

---

## 📐 Metrics
| Metric | Formula |
|--------|---------|
| CTR | `clicks / impressions × 100` |
| SOV | `message_impressions / total_module_impressions × 100` |
| ATC Rate | `total_atc_count / (impressions / 1000)` |
| Exit Rate | `1 − (all_clicks_count_flag / asset_clicks_count)` |
| Benchmark | CTR from Feb 1–Mar 3 baseline period |

---

## ↔️ Difference vs WBR App (port 8001)

| | WBR App (8001) | Charts App (8002) |
|--|----------------|-------------------|
| View | Module-level metrics table | Visual bar + bubble charts |
| Grain | Module buckets (HPOV, SIG, BTF…) | Message-level breakdown |
| WoW | ✅ Yes | Date-selectable |
| Best for | Quick exec WBR table | Deep creative performance analysis |

Use **both** for a complete WBR prep session.

---

## 🔧 Stop the Server
```bash
lsof -ti:8002 | xargs kill -9
```

*Internal Walmart use only — Keel Agent | Site Content Strategy*
