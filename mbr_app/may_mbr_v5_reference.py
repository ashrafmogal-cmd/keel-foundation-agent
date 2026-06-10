#!/usr/bin/env python3
"""May 2026 Nav MBR — v5 final clean rebuild."""
import os
from datetime import datetime

# ═══ DATA ═══════════════════════════════════════════════════
dept_may={"Clicks":13144242,"ATC":11164740,"Units":3302984,"GMV":19945500,"ER":0.153}
dept_apr={"Clicks":13144242/1.0202,"ATC":11164740/0.973,"Units":3302984/0.8731,"GMV":19945500/0.8955,"ER":0.165}
# Sub Nav — updated with user's April and May numbers + diffs
sub_may={"Clicks":6200562,"ATC":1521309,"Units":363147,"GMV":3338358,"ER":0.259}
sub_apr={"Clicks":5924271,"ATC":1521309/1.0345,"Units":363147/(1-0.0805),"GMV":3338358/1.0066,"ER":0.254}

def pch(c,p): return (c-p)/p*100 if p else 0
def fnum(n):
    if abs(n)>=1e6: return f"{n/1e6:.2f}M"
    if abs(n)>=1e3: return f"{n/1e3:.0f}K"
    return f"{n:,.0f}"
def fdol(n):
    if abs(n)>=1e6: return f"${n/1e6:.2f}M"
    if abs(n)>=1e3: return f"${n/1e3:.0f}K"
    return f"${n:,.0f}"
def fbadge(pct, suffix="%"):
    color="#76C043" if pct>0.5 else ("#E31837" if pct<-0.5 else "#888")
    bg="#e8f8e0" if pct>0.5 else ("#fde8ec" if pct<-0.5 else "#f0f0f0")
    sign="+" if pct>0 else ""
    if suffix=="bps": return f'<span class="badge" style="background:{bg};color:{color};border:1px solid {color}33">{sign}{pct:.0f} bps</span>'
    return f'<span class="badge" style="background:{bg};color:{color};border:1px solid {color}33">{sign}{pct:.1f}%</span>'

# Dept Nav L0s (no Gaming/Books/Collectibles/FathersDay/Resold — those go in New table)
app_l0=[("Mother S Day",104102,-11740),("Pharmacy Health",806361,-8152),("Rollbacks More",491090,-8941),("Toys Outdoor Play",154884,-8111),("Home Garden Tools",670078,-6981),("Household Essentials",157909,-5163),("Beauty",161632,-3686),("Baby Kids",260290,-17851),("Pets",103059,-756),("Auto Tires",282602,-828),("Personal Care",233949,1574),("Party Supplies",48596,3469),("Sports Outdoors",108671,3291),("School Office",98366,4491),("Electronics",285413,4512),("Clothing Shoes",1492561,53484),("Grocery",4491140,99060)]
rweb_l0=[("Home Garden Tools",282551,-11152),("Baby Kids",57874,-5710),("Rollbacks More",144381,-5354),("Grocery",1023922,-5497),("Auto Tires",131784,-4476),("Toys Outdoor Play",37027,-2344),("Pharmacy Health",250978,-2149),("Personal Care",52500,-1554),("Beauty",40174,-1097),("Household Essentials",44854,-948),("School Office",27848,-873),("Party Supplies",11985,-550),("Pets",38147,-303),("Sports Outdoors",51207,142),("Electronics",171245,2495),("Clothing Shoes",430435,5855),("Mother S Day",25066,-12689)]
app_gmv={"Grocery":-1644721,"Clothing Shoes":65473,"Electronics":-5269,"Rollbacks More":-40862,"Baby Kids":-48335,"Home Garden Tools":-35469,"Pharmacy Health":-39335,"Beauty":-17517,"Personal Care":-36574,"Household Essentials":-45265,"Auto Tires":-10528,"Pets":-41547,"Toys Outdoor Play":-23851,"Party Supplies":-163,"Sports Outdoors":8819,"School Office":-4544,"Mother S Day":27622}
rweb_gmv={"Grocery":-174189,"Clothing Shoes":26999,"Electronics":-253127,"Rollbacks More":-12330,"Baby Kids":-19666,"Home Garden Tools":-6361,"Pharmacy Health":-19432,"Beauty":-5635,"Personal Care":-15120,"Household Essentials":-16785,"Auto Tires":19133,"Pets":-9108,"Toys Outdoor Play":-11499,"Party Supplies":-121,"Sports Outdoors":-10404,"School Office":-4214,"Mother S Day":2740}

# New/Restructured L0s
app_new_l0=[("Gaming & Movies",66851,62525,0.271),("Collectibles, Books & Music",33415,10481,0.257),("Father's Day",22500,9152,0.418),("Resold",38840,4727,0.450)]
rweb_new_l0=[("Gaming & Movies",23311,42625,0.215),("Collectibles, Books & Music",12081,11639,0.162),("Father's Day",8243,9348,0.302),("Resold",5987,2249,0.281)]

def calc_sorted(items):
    r=[]
    for n,c,d in items:
        prev=c-d; mom=(d/prev*100) if prev else 0; r.append((n,c,mom,d))
    return sorted(r, key=lambda x: x[2])

def bar_chart(sd, gd, title, icon, bc):
    mx=max(abs(x[2]) for x in sd) or 1; rows=""
    for n,c,mom,d in sd:
        w=min(abs(mom)/mx*100,100); g=gd.get(n,0); tip=f"Clicks {'+' if d>=0 else ''}{fnum(d)} · GMV {'+' if g>=0 else ''}{fdol(g)}"
        if mom<-0.5: rows+=f'<div class="br"><div class="bpct" style="color:#E31837">{mom:.1f}%</div><div class="tipwrap neg"><div class="bar bar-red" style="width:{w}%"></div><div class="tip">{tip}</div></div><div class="bl">{n}</div><div class="tipwrap" style="flex:1"></div><div class="bpct-left"></div></div>\n'
        elif mom>0.5: rows+=f'<div class="br"><div class="bpct"></div><div class="tipwrap neg" style="flex:1"></div><div class="bl">{n}</div><div class="tipwrap"><div class="bar bar-grn" style="width:{w}%"></div><div class="tip">{tip}</div></div><div class="bpct-left" style="color:#76C043">+{mom:.1f}%</div></div>\n'
        else: rows+=f'<div class="br"><div class="bpct" style="color:#888">~0%</div><div class="tipwrap neg" style="flex:0.5"></div><div class="bl">{n}</div><div class="tipwrap" style="flex:0.5"></div><div class="bpct-left"></div></div>\n'
    return f'<div class="card" style="border-left:4px solid {bc}"><div class="ctitle">{icon} {title}</div><div class="csub">Sorted worst → best · Hover for detail · ◀ Red = decline · Green = growth ▶</div><div class="barchart">{rows}</div></div>'

# Sub Nav pills
app_sub_leg=[("Get It Fast",115952,-43180),("My Items",289957,-24017),("Credit Card",45539,-19970),("Only at Walmart",74528,-16209),("Walmart+",290320,-4134),("New Arrivals",161742,60),("Pharmacy",443231,15474),("Meals Made Easy",143648,17396),("Rollbacks More",1256836,97732)]
rweb_sub_leg=[("Only at Walmart",59392,-15037),("My Items",203626,-16367),("Credit Card",28268,-22176),("Walmart+",286291,6687),("New Arrivals",229923,1799),("Get It Fast",231344,4046),("Pharmacy",225357,9464),("Rollbacks More",551470,15011),("Meals Made Easy",141664,17723)]
app_sub_seas=[("Memorial Day",315598,113694,0.241),("Mothers Day",238975,132178,0.288),("Fathers Day",67554,18912,0.308),("Walmart Business",30367,1216,0.480),("Soccer HQ",18561,996,0.194),("Graduation",12234,2535,0.158),("Americas Birthday",11568,3246,0.146),("Swim Shop",11134,3457,0.246),("The Pet Event",5215,2179,0.134),("Subway",1359,0,0.346)]
rweb_sub_seas=[("Memorial Day",260109,205371,0.315),("Mothers Day",189152,235001,0.278),("Fathers Day",111054,98308,0.341),("Walmart Business",34035,32800,0.501),("Americas Birthday",30589,19830,0.324),("Swim Shop",27985,24545,0.254),("Graduation",27705,20660,0.289),("The Pet Event",15285,15709,0.227),("Soccer HQ",10827,6001,0.344),("Subway",545,60,0.309)]

def subnav_bar(items, title, icon, color):
    si=sorted([(n,c,d,pch(c,c-d) if(c-d) else 0) for n,c,d in items], key=lambda x:x[3])
    mx=max(abs(x[3]) for x in si) or 1; rows=""
    for n,c,d,mom in si:
        w=min(abs(mom)/mx*100,100); tip=f"{d:+,.0f} clicks"
        if mom<-0.5: rows+=f'<div class="br"><div class="bpct" style="color:#E31837">{mom:.1f}%</div><div class="tipwrap neg"><div class="bar bar-red" style="width:{w}%"></div><div class="tip">{tip}</div></div><div class="bl">{n}</div><div class="tipwrap" style="flex:1"></div><div class="bpct-left"></div></div>\n'
        else: rows+=f'<div class="br"><div class="bpct"></div><div class="tipwrap neg" style="flex:1"></div><div class="bl">{n}</div><div class="tipwrap"><div class="bar bar-grn" style="width:{w}%"></div><div class="tip">{tip}</div></div><div class="bpct-left" style="color:#76C043">+{mom:.1f}%</div></div>\n'
    return f'<div class="card" style="border-left:4px solid {color}"><div class="ctitle">{icon} {title}</div><div class="csub">Excludes seasonal / new pills · Sorted worst → best</div><div class="barchart">{rows}</div></div>'

# Resold
resold_l1=[("All Resold",6875,0.092,774),("Electronics",5058,0.522,947),("Computers Tablets",4512,0.503,663),("Rollbacks More",4299,0.578,7),("Cell Phones",3462,0.502,432),("Home Kitchen",4258,0.508,409),("Pre Loved Fashion",2696,0.073,490),("Garden Tools",1435,0.570,229),("Beauty Tools",1268,0.629,85),("Vacuums",1078,0.570,68),("Baby Gear",954,0.555,145),("Video Games Consoles",2945,0.631,478)]
resold_total_clicks=38840+5987; resold_total_atc=1916+458; resold_total_units=58+59; resold_total_gmv=4727+2249
resold_total_gmv_app=4727

# Pre-build new L0 rows
def build_new_l0_rows(items):
    return "".join(f'<tr style="border-bottom:1px solid #f0f2f5"><td style="padding:6px 8px;font-weight:600">{n}</td><td style="padding:6px 8px;text-align:right">{fnum(c)}</td><td style="padding:6px 8px;text-align:right">{fdol(g)}</td><td style="padding:6px 8px;text-align:right">{er*100:.1f}%</td></tr>' for n,c,g,er in items)
new_l0_app_rows = build_new_l0_rows(app_new_l0)
new_l0_rweb_rows = build_new_l0_rows(rweb_new_l0)

# Nav GMV decline calc
total_gmv_may = dept_may["GMV"] + sub_may["GMV"]
total_gmv_apr = dept_apr["GMV"] + sub_apr["GMV"]
nav_gmv_decline = pch(total_gmv_may, total_gmv_apr)

css = open('/Users/a0m1sr5/Library/CloudStorage/OneDrive-WalmartInc/Desktop/clickfather/april2026_nav_mbr_20260505.html').read().split('<style>')[1].split('</style>')[0]

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>May 2026 — Nav Deep Dive</title>
<style>{css}</style>
</head>
<body>
<div class="hdr">
  <div class="hdr-top">
    <div>
      <div class="h1">&#128202; May 2026 &#8212; Navigation Deep Dive</div>
      <div class="hsub">Dept Nav + Sub Nav &middot; App vs rWeb &middot; MoM vs April 2026</div>
    </div>
    <div class="hbadge">Site Content Strategy &amp; BAI</div>
  </div>
  <div class="ybar"></div>
</div>
<div class="page">

<!-- AGENDA -->
<div style="margin-bottom:20px">
  <div style="font-weight:800;font-size:.95rem;color:#1a1a1a;margin-bottom:8px">📑 Agenda</div>
  <ol style="margin:0;padding-left:22px;font-size:.85rem;line-height:2;color:#333">
    <li>Overall Navigation Metrics</li>
    <li>Key Insights</li>
    <li>Department Nav</li>
    <li>Sub Nav</li>
  </ol>
</div>

<!-- ═══ OVERALL NAVIGATION METRICS ═══ -->
<div class="stitle" style="color:#1a1a1a">📋 Overall Navigation Metrics</div>
<div class="ssub">May vs April 2026</div>
<div class="krow">
  <div class="kpanel">
    <div class="khdr" style="border-left:4px solid #0071CE"><div>
      <div style="font-weight:700;font-size:.95rem">Dept Nav</div>
      <div style="font-size:.76rem;color:#666">May clicks: <strong>{fnum(dept_may["Clicks"])}</strong> (<span style="color:#76C043">+{pch(dept_may["Clicks"],dept_apr["Clicks"]):.1f}%</span> MoM) · Exit Rate: {dept_may["ER"]*100:.1f}% ({(dept_may["ER"]-dept_apr["ER"])*100:+.1f}pp)</div>
    </div></div>
    <div class="kgrid">
      <div class="kc"><div class="kl">Clicks</div><div class="kv">{fnum(dept_may["Clicks"])}</div>{fbadge(pch(dept_may["Clicks"],dept_apr["Clicks"]))}</div>
      <div class="kc"><div class="kl">Attr. ATC</div><div class="kv">{fnum(dept_may["ATC"])}</div>{fbadge(pch(dept_may["ATC"],dept_apr["ATC"]))}</div>
      <div class="kc"><div class="kl">Units Ordered</div><div class="kv">{fnum(dept_may["Units"])}</div>{fbadge(pch(dept_may["Units"],dept_apr["Units"]))}</div>
      <div class="kc"><div class="kl">Attr. GMV</div><div class="kv">{fdol(dept_may["GMV"])}</div>{fbadge(pch(dept_may["GMV"],dept_apr["GMV"]))}</div>
    </div>
  </div>
  <div class="kpanel">
    <div class="khdr" style="border-left:4px solid #FFC220"><div>
      <div style="font-weight:700;font-size:.95rem">Sub Nav</div>
      <div style="font-size:.76rem;color:#666">May clicks: <strong>{fnum(sub_may["Clicks"])}</strong> (<span style="color:#76C043">+{pch(sub_may["Clicks"],sub_apr["Clicks"]):.1f}%</span> MoM) · Exit Rate: {sub_may["ER"]*100:.1f}% ({(sub_may["ER"]-sub_apr["ER"])*100:+.1f}pp)</div>
    </div></div>
    <div class="kgrid">
      <div class="kc"><div class="kl">Clicks</div><div class="kv">{fnum(sub_may["Clicks"])}</div>{fbadge(pch(sub_may["Clicks"],sub_apr["Clicks"]))}</div>
      <div class="kc"><div class="kl">Attr. ATC</div><div class="kv">{fnum(sub_may["ATC"])}</div>{fbadge(pch(sub_may["ATC"],sub_apr["ATC"]))}</div>
      <div class="kc"><div class="kl">Units Ordered</div><div class="kv">{fnum(sub_may["Units"])}</div>{fbadge(pch(sub_may["Units"],sub_apr["Units"]))}</div>
      <div class="kc"><div class="kl">Attr. GMV</div><div class="kv">{fdol(sub_may["GMV"])}</div>{fbadge(pch(sub_may["GMV"],sub_apr["GMV"]))}</div>
    </div>
  </div>
</div>

<!-- ═══ KEY INSIGHTS ═══ -->
<div class="stitle" style="color:#1a1a1a;margin-top:24px">🔍 Key Insights</div>
<div class="ssub">May 2026 · Combined App + rWeb</div>
<div style="background:#fff;border-radius:12px;padding:20px 24px;box-shadow:0 2px 8px rgba(0,0,0,0.06);border:1px solid #e8eaed">
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px">
  <div class="icard" style="border-top:3px solid #E31837"><div style="font-size:.73rem;color:#888;margin-bottom:4px">Sitewide Sessions</div><div style="font-size:.8rem;color:#E31837;font-weight:700">▼ -1.5% MoM</div></div>
  <div class="icard" style="border-top:3px solid #76C043"><div style="font-size:.73rem;color:#888;margin-bottom:4px">Sitewide ATC</div><div style="font-size:.8rem;color:#76C043;font-weight:700">▲ +4.9% MoM</div></div>
  <div class="icard" style="border-top:3px solid #76C043"><div style="font-size:.73rem;color:#888;margin-bottom:4px">Sitewide GMV</div><div style="font-size:.8rem;color:#76C043;font-weight:700">▲ +0.9% MoM</div></div>
</div>
<ul style="padding:0;margin:0;list-style:none">
<li style="font-size:.88rem;line-height:1.7;color:#333;padding:10px 0;border-bottom:1px solid #f0f2f5"><strong>Clicks are holding but the GMV gap is widening.</strong> Sitewide GMV grew slightly, but Nav-attributed GMV declined <strong>{nav_gmv_decline:.1f}%</strong> MoM. Dept Nav GMV fell -10.5% while Sub Nav GMV grew modestly. Customers are clicking through Nav at steady rates but completing purchases through other paths — search, homepage modules, and direct links appear to be winning the conversion battle.</li>
<li style="font-size:.88rem;line-height:1.7;color:#333;padding:10px 0;border-bottom:1px solid #f0f2f5"><strong>Summer is reshaping what customers want.</strong> The L0s that grew all tell the same story — customers are dressing for warm weather (<strong>Clothing</strong>, driven by Women's and Swim Shop), planning outdoor events (<strong>Party Supplies</strong>, <strong>Sports &amp; Outdoors</strong>), and shopping for <strong>Father's Day</strong> gifts.</li>
<li style="font-size:.88rem;line-height:1.7;color:#333;padding:10px 0;border-bottom:1px solid #f0f2f5"><strong>Grocery clicks grew but GMV eroded broadly across nearly every L1.</strong> This suggests a shift in basket composition or promotional cadence rather than a category-specific problem. Frozen, Meat Seafood, and Beverages led the losses.</li>
<li style="font-size:.88rem;line-height:1.7;color:#333;padding:10px 0"><strong>Rollbacks &amp; More continues to be the anchor pill in Sub Nav</strong> — it's the highest-volume pill on both platforms and the most consistent grower month over month. Pharmacy is also quietly climbing on App, reflecting a steady customer shift toward health &amp; wellness navigation.</li>
</ul>
</div>

<!-- ═══ DEPT NAV ═══ -->
<div class="divider"></div>
<div style="background:linear-gradient(135deg,#0071CE15,#0071CE08);border-radius:12px;padding:20px 24px;margin-bottom:16px;border-left:5px solid #0071CE">
  <div style="font-size:1.4rem;font-weight:800;color:#0071CE;margin-bottom:4px">📂 Dept Nav</div>
  <div style="font-size:.85rem;color:#555">Clicks grew despite traffic headwinds — summer categories drove the gains while GMV erosion was broad-based</div>
</div>

<div class="crow">
{bar_chart(calc_sorted(app_l0), app_gmv, "App — Dept Nav L0 Click MoM %", "📱", "#0071CE")}
{bar_chart(calc_sorted(rweb_l0), rweb_gmv, "rWeb — Dept Nav L0 Click MoM %", "🌐", "#0071CE")}
</div>

<!-- NEW L0 CALLOUT -->
<div style="background:#fff;border-radius:12px;padding:16px 22px;box-shadow:0 1px 6px rgba(0,0,0,.07);margin-bottom:16px;border-left:4px solid #0071CE">
  <div style="font-weight:800;font-size:.9rem;color:#0071CE;margin-bottom:10px">🆕 New &amp; Restructured L0s — No April Baseline</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
    <div>
      <div style="font-weight:700;font-size:.82rem;color:#333;margin-bottom:8px">📱 App</div>
      <table style="width:100%;border-collapse:collapse;font-size:.82rem">
        <thead><tr style="background:#f8f9fa;border-bottom:2px solid #e8eaed"><th style="text-align:left;padding:6px 8px">L0</th><th style="text-align:right;padding:6px 8px">Clicks</th><th style="text-align:right;padding:6px 8px">GMV</th><th style="text-align:right;padding:6px 8px">Exit Rate</th></tr></thead>
        <tbody>{new_l0_app_rows}</tbody></table>
    </div>
    <div>
      <div style="font-weight:700;font-size:.82rem;color:#333;margin-bottom:8px">🌐 rWeb</div>
      <table style="width:100%;border-collapse:collapse;font-size:.82rem">
        <thead><tr style="background:#f8f9fa;border-bottom:2px solid #e8eaed"><th style="text-align:left;padding:6px 8px">L0</th><th style="text-align:right;padding:6px 8px">Clicks</th><th style="text-align:right;padding:6px 8px">GMV</th><th style="text-align:right;padding:6px 8px">Exit Rate</th></tr></thead>
        <tbody>{new_l0_rweb_rows}</tbody></table>
    </div>
  </div>
  <div style="font-size:.78rem;color:#888;margin-top:10px;line-height:1.6">
    <strong>Movies Migration:</strong> Movies moved from Books to Gaming on 5/19, creating Gaming &amp; Movies. · <strong>Collectibles:</strong> Tested for 1 month as standalone entry (launched 4/15). Taken down 5/15 and merged with Books &amp; Music on 5/19. · <strong>Father's Day &amp; Resold:</strong> New Dept L0s launched mid-May with partial month data.
  </div>
</div>

<!-- 2 bullet insights -->
<div style="background:#fff;border-radius:12px;padding:16px 22px;box-shadow:0 1px 6px rgba(0,0,0,.07);margin-bottom:16px;border-left:4px solid #0071CE">
  <ul style="padding:0;margin:0;list-style:none">
    <li style="font-size:.86rem;line-height:1.7;color:#333;padding:8px 0;border-bottom:1px solid #f0f2f5"><div style="font-weight:800;font-size:.9rem;color:#0071CE;margin-bottom:4px">☀️ Summer Is Driving the Growers</div> <strong>Clothing</strong> (+3.7% App) led by Women's (+30K clicks, +$68K GMV) as summer wardrobe shopping kicks in — Swim Shop exploded +164%, Premium Fashion +11%. <strong>Party Supplies</strong> (+7.7%), <strong>Sports Outdoors</strong> (+3.1%), and the new <strong>Father's Day</strong> L0 all point to customers planning outdoor events and gifting. Grocery clicks grew +2.3% but GMV dropped -$1.6M across nearly every L1 — a basket composition shift, not a category-specific issue.</li>
    <li style="font-size:.86rem;line-height:1.7;color:#333;padding:8px 0"><div style="font-weight:800;font-size:.9rem;color:#0071CE;margin-bottom:4px">✏️ Customers Are Getting Ahead of School</div> School Office grew +4.8% — but it's not traditional back-to-school yet. The top L1 growers are <strong>Crafting</strong> (+1,273 clicks — parents finding summer activities for kids) and <strong>Teacher's Classroom Shop</strong> (+716) / <strong>Classroom Registry</strong> (+678) — educators stocking up as school budgets get confirmed in May/June. <strong>All School Supplies</strong> clicks grew but GMV declined — customers are browsing and wish-listing, not buying yet.</li>
  </ul>
</div>

<!-- GROCERY KPI -->
<div class="krow">
  <div class="kpanel" style="border-left:4px solid #0071CE">
    <div class="khdr"><div><div style="font-weight:700;font-size:.95rem">App — Grocery (Top L0 by Volume)</div><div style="font-size:.76rem;color:#666">44.4% of all App Dept Nav clicks · GMV/Click: $1.80</div></div></div>
    <div class="kgrid">
      <div class="kc"><div class="kl">Clicks</div><div class="kv">4.49M</div>{fbadge(pch(4491140,4491140-99060))}</div>
      <div class="kc"><div class="kl">Attr. ATC</div><div class="kv">6.69M</div>{fbadge(pch(6685617,6685617+431889))}</div>
      <div class="kc"><div class="kl">Attr. GMV</div><div class="kv">$8.08M</div>{fbadge(pch(8081461,8081461+1644721))}</div>
      <div class="kc"><div class="kl">Exit Rate</div><div class="kv">11.7%</div><span class="badge" style="background:#e8f8e0;color:#76C043;border:1px solid #76C04333">-160 bps</span></div>
    </div>
  </div>
  <div class="kpanel" style="border-left:4px solid #0071CE">
    <div class="khdr"><div><div style="font-weight:700;font-size:.95rem">rWeb — Grocery (Top L0 by Volume)</div><div style="font-size:.76rem;color:#666">35.6% of all rWeb Dept Nav clicks · GMV/Click: $2.84</div></div></div>
    <div class="kgrid">
      <div class="kc"><div class="kl">Clicks</div><div class="kv">1.02M</div>{fbadge(pch(1023922,1023922+5497))}</div>
      <div class="kc"><div class="kl">Attr. ATC</div><div class="kv">1.77M</div>{fbadge(pch(1771772,1771772-20258))}</div>
      <div class="kc"><div class="kl">Attr. GMV</div><div class="kv">$2.91M</div>{fbadge(pch(2910588,2910588+174189))}</div>
      <div class="kc"><div class="kl">Exit Rate</div><div class="kv">11.2%</div><span class="badge" style="background:#e8f8e0;color:#76C043;border:1px solid #76C04333">-10 bps</span></div>
    </div>
  </div>
</div>

<!-- GROCERY GMV EROSION -->
<div class="card" style="margin-bottom:14px;border-left:4px solid #0071CE">
  <div class="ctitle">🛒 Grocery — Clicks Growing, GMV Eroding</div>
  <div class="csub">The disconnect: customers are browsing more but spending less per visit. The decline spans nearly every L1.</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px">
    <div style="background:#fff5f5;border-radius:8px;padding:14px 18px;border:1px solid #E3183722">
      <div style="font-weight:700;color:#E31837;font-size:.85rem;margin-bottom:8px">📉 Biggest GMV Losses (App + rWeb)</div>
      <table style="width:100%;border-collapse:collapse;font-size:.82rem">
        <thead><tr style="border-bottom:2px solid #e8eaed"><th style="text-align:left;padding:6px 8px">L1</th><th style="text-align:right;padding:6px 8px">GMV Δ</th></tr></thead>
        <tbody>
        <tr style="border-bottom:1px solid #f0f2f5"><td style="padding:6px 8px">All Grocery</td><td style="padding:6px 8px;text-align:right;color:#E31837;font-weight:600">-$405K</td></tr>
        <tr style="border-bottom:1px solid #f0f2f5"><td style="padding:6px 8px">Frozen</td><td style="padding:6px 8px;text-align:right;color:#E31837;font-weight:600">-$313K</td></tr>
        <tr style="border-bottom:1px solid #f0f2f5"><td style="padding:6px 8px">Meat Seafood</td><td style="padding:6px 8px;text-align:right;color:#E31837;font-weight:600">-$280K</td></tr>
        <tr style="border-bottom:1px solid #f0f2f5"><td style="padding:6px 8px">Beverages</td><td style="padding:6px 8px;text-align:right;color:#E31837;font-weight:600">-$152K</td></tr>
        <tr style="border-bottom:1px solid #f0f2f5"><td style="padding:6px 8px">Snacks</td><td style="padding:6px 8px;text-align:right;color:#E31837;font-weight:600">-$130K</td></tr>
        <tr><td style="padding:6px 8px">Dairy Eggs</td><td style="padding:6px 8px;text-align:right;color:#E31837;font-weight:600">-$119K</td></tr>
        </tbody>
      </table>
    </div>
    <div style="background:#EEF6FF;border-radius:8px;padding:14px 18px;border:1px solid #0071CE22">
      <div style="font-weight:700;color:#0071CE;font-size:.85rem;margin-bottom:8px">💡 What's Likely Happening</div>
      <div style="font-size:.83rem;color:#333;line-height:1.8">The GMV erosion is broad-based — not a single category issue. This points toward a shift in basket composition or promotional cadence across Grocery.<br><br><strong>Meals Made Easy</strong> is the sole bright spot — the pill swap from Dinner Made Easy is paying off with broader meal-occasion positioning.<br><br><strong>Father's Day Food</strong> launched mid-month and is already driving strong volume.</div>
    </div>
  </div>
</div>

<!-- ═══ FOCUS: NEW L0 RESOLD ═══ -->
<div style="background:linear-gradient(135deg,#0071CE10,#0071CE05);border-radius:12px;padding:20px 24px;margin-bottom:16px;margin-top:24px;border-left:5px solid #0071CE">
  <div style="font-size:1.2rem;font-weight:800;color:#0071CE;margin-bottom:4px">♻️ Focus: New L0 Resold</div>
  <div style="font-size:.85rem;color:#555">Launched ~May 11 · Strong discovery, weak conversion</div>
</div>

<!-- Resold KPIs — only Exit Rate + ATC→Order -->
<div class="card" style="border-left:4px solid #0071CE;margin-bottom:14px">
  <div class="ctitle">♻️ Resold — Combined App + rWeb</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:8px;max-width:500px">
    <div class="kc"><div class="kl">Exit Rate</div><div class="kv" style="font-size:1.1rem;color:#E31837">42.7%</div><div style="font-size:.72rem;color:#888">vs 15.3% Nav avg</div></div>
    <div class="kc"><div class="kl">ATC → Order</div><div class="kv" style="font-size:1.1rem;color:#E31837">{resold_total_units/resold_total_atc*100:.1f}%</div><div style="font-size:.72rem;color:#888">vs ~30% dept avg</div></div>
  </div>
</div>

<!-- Exit rate story BEFORE table -->
<div style="background:#EEF6FF;border-radius:8px;padding:14px 18px;border:1px solid #0071CE22;margin-bottom:14px;border-left:4px solid #0071CE">
  <div style="font-weight:700;color:#0071CE;font-size:.85rem;margin-bottom:6px">💡 The Exit Rate Story</div>
  <ul style="font-size:.83rem;color:#333;line-height:1.8;padding-left:16px;margin:0">
    <li><strong>"All Resold" (9.2%) and "Pre-Loved Fashion" (7.3%) work because they land on Category pages</strong> — customers are forced to browse and click deeper, creating engagement momentum. These two entries prove the model: when customers land somewhere they <em>have</em> to interact with, they stay.</li>
    <li><strong>Everything else (50%+ exit rates) lands on PDP or browse pages</strong> — if that single product doesn't match intent, customers leave immediately. Routing high-exit entries like Beauty Tools (63%), Video Games (63%), and Rollbacks (58%) through a Category page first would match the pattern that's already working.</li>
  </ul>
</div>

<!-- Resold L1 table -->
<div class="card" style="border-left:4px solid #0071CE;margin-bottom:14px">
  <div class="ctitle">📊 Resold — App L1 Flyout Performance</div>
  <table style="width:100%;border-collapse:collapse;font-size:.82rem;margin-top:12px">
    <thead><tr style="background:#f8f9fa;border-bottom:2px solid #e8eaed">
      <th style="text-align:left;padding:8px 12px;font-weight:700">L1 Entry</th>
      <th style="text-align:right;padding:8px 12px;font-weight:700">Clicks</th>
      <th style="text-align:right;padding:8px 12px;font-weight:700">Exit Rate</th>
      <th style="text-align:right;padding:8px 12px;font-weight:700">GMV</th>
      <th style="text-align:right;padding:8px 12px;font-weight:700">Click Share</th>
      <th style="text-align:right;padding:8px 12px;font-weight:700">GMV Share</th>
    </tr></thead><tbody>
    {"".join(f'<tr style="border-bottom:1px solid #f0f2f5;{"background:#fafafa" if i%2 else ""}"><td style="padding:8px 12px;font-weight:600">{n}</td><td style="padding:8px 12px;text-align:right">{fnum(c)}</td><td style="padding:8px 12px;text-align:right;{"color:#76C043;font-weight:700" if er<0.15 else ""}">{er*100:.1f}%{"" if er<0.15 else ""}</td><td style="padding:8px 12px;text-align:right">{fdol(g)}</td><td style="padding:8px 12px;text-align:right">{c/38840*100:.1f}%</td><td style="padding:8px 12px;text-align:right;{"color:#76C043;font-weight:700" if (g/resold_total_gmv_app*100 > c/38840*100) else ""}">{g/resold_total_gmv_app*100:.1f}%</td></tr>' for i,(n,c,er,g) in enumerate(resold_l1))}
    </tbody></table>
  <div style="margin-top:10px;font-size:.78rem;color:#888;display:flex;gap:12px;align-items:center">
    <span style="display:inline-block;width:10px;height:10px;background:#fde8ec;border:1px solid #E31837;border-radius:2px"></span> <span>Exit rate &gt;50% — landing on PDP/browse pages</span>
    <span style="display:inline-block;width:10px;height:10px;background:#e8f8e0;border:1px solid #76C043;border-radius:2px"></span> <span>Exit rate &lt;15% — landing on category pages</span>
    <span style="display:inline-block;width:10px;height:10px;background:#e8f8e0;border:1px solid #76C043;border-radius:2px"></span> <span style="color:#76C043;font-weight:600">Green GMV Share</span> <span>= outperforming click share</span>
  </div>
</div>

<!-- ═══ SUB NAV ═══ -->
<div class="divider"></div>
<div style="background:linear-gradient(135deg,#FFC22018,#FFC22008);border-radius:12px;padding:24px 28px;margin-bottom:16px;border-left:5px solid #FFC220">
  <div style="font-size:1.4rem;font-weight:800;color:#b8860b;margin-bottom:12px">🗒️ Sub Nav</div>
  <div style="font-size:.88rem;line-height:1.7;color:#444">Sub Nav clicks grew MoM driven by new seasonal pills. <strong>Rollbacks &amp; More</strong> continues to dominate as the #1 pill. <strong>Pharmacy</strong> grew on App, reflecting a steady customer shift toward health &amp; wellness.</div>
</div>

<div style="font-weight:700;font-size:.92rem;color:#333;margin-bottom:10px">📦 Legacy Sub Nav Pills — MoM % Change</div>
<div class="crow">
{subnav_bar(app_sub_leg, "App — Legacy Pills Click MoM %", "📱", "#FFC220")}
{subnav_bar(rweb_sub_leg, "rWeb — Legacy Pills Click MoM %", "🌐", "#FFC220")}
</div>

<div style="font-weight:700;font-size:.92rem;color:#333;margin-bottom:10px;margin-top:24px">🌸 Seasonal &amp; New Sub Nav Pills</div>
<div class="crow">
<div class="card" style="border-left:4px solid #FFC220">
<div class="ctitle">📱 App — Seasonal &amp; New Pills</div><div class="csub">May 2026</div>
<table style="width:100%;border-collapse:collapse;font-size:.82rem;margin-top:12px">
  <thead><tr style="background:#f8f9fa;border-bottom:2px solid #e8eaed"><th style="text-align:left;padding:10px 12px;font-weight:700">Category</th><th style="text-align:right;padding:10px 12px;font-weight:700">Clicks</th><th style="text-align:right;padding:10px 12px;font-weight:700">GMV</th><th style="text-align:right;padding:10px 12px;font-weight:700">Exit Rate</th></tr></thead><tbody>
  {"".join(f'<tr style="border-bottom:1px solid #f0f2f5;{"background:#fafafa" if i%2 else ""}"><td style="padding:10px 12px;font-weight:600">{n}</td><td style="padding:10px 12px;text-align:right">{fnum(c)}</td><td style="padding:10px 12px;text-align:right">{fdol(g)}</td><td style="padding:10px 12px;text-align:right">{er*100:.1f}%</td></tr>' for i,(n,c,g,er) in enumerate(app_sub_seas))}
  </tbody></table></div>
<div class="card" style="border-left:4px solid #FFC220">
<div class="ctitle">🌐 rWeb — Seasonal &amp; New Pills</div><div class="csub">May 2026</div>
<table style="width:100%;border-collapse:collapse;font-size:.82rem;margin-top:12px">
  <thead><tr style="background:#f8f9fa;border-bottom:2px solid #e8eaed"><th style="text-align:left;padding:10px 12px;font-weight:700">Category</th><th style="text-align:right;padding:10px 12px;font-weight:700">Clicks</th><th style="text-align:right;padding:10px 12px;font-weight:700">GMV</th><th style="text-align:right;padding:10px 12px;font-weight:700">Exit Rate</th></tr></thead><tbody>
  {"".join(f'<tr style="border-bottom:1px solid #f0f2f5;{"background:#fafafa" if i%2 else ""}"><td style="padding:10px 12px;font-weight:600">{n}</td><td style="padding:10px 12px;text-align:right">{fnum(c)}</td><td style="padding:10px 12px;text-align:right">{fdol(g)}</td><td style="padding:10px 12px;text-align:right">{er*100:.1f}%</td></tr>' for i,(n,c,g,er) in enumerate(rweb_sub_seas))}
  </tbody></table></div>
</div>

<!-- Sub Nav notes -->
<div style="background:#fffbe6;border-radius:8px;padding:12px 16px;margin-bottom:14px;border:1px solid #FFC22044;font-size:.78rem;color:#888;line-height:1.6">
  <strong>Memorial Day</strong> — New seasonal pill launched mid-May. Already the largest Sub Nav pill by volume on App (316K clicks). · <strong>Walmart Business</strong> — New temporary entry for Small Business Month.
</div>

<div style="text-align:center;margin-top:28px;padding:14px;font-size:.72rem;color:#aaa">May 2026 Navigation Deep Dive · Source: May_Nav_MBR.xlsx · Generated {datetime.now().strftime('%B %d, %Y')}</div>
</div>
</body>
</html>"""

out_dir = os.path.expanduser("~/Desktop/clickfather")
os.makedirs(out_dir, exist_ok=True)
ts = datetime.now().strftime('%Y%m%d_%H%M%S')
out_path = os.path.join(out_dir, f"may2026_nav_mbr_v5_{ts}.html")
with open(out_path, "w") as f:
    f.write(html)
print(f"✅ Saved to: {out_path}")
print(f"   Size: {os.path.getsize(out_path):,} bytes")
