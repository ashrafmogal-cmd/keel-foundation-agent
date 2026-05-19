from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, StreamingResponse
from google.cloud import bigquery
from datetime import datetime, timedelta
from io import BytesIO

app = FastAPI(title="WBR Report App")
client = bigquery.Client()
JOB_CONFIG = bigquery.QueryJobConfig(maximum_bytes_billed=50_000_000_000)

BQ_TABLE   = "wmt-site-content-strategy.scs_production.hp_summary_asset"
FYTD_START = "2026-01-31"

# ── ATF zone list ─────────────────────────────────────────────────────────────
ATF_ZONES_LIST = [
    'contentzone1','contentzone2','contentzone3',
    'contentzone4','contentzone5','contentzone6',
]
_ATF_SQL = "','".join(ATF_ZONES_LIST)   # ready for IN ('<zone>','<zone>',...)

# ── Module bucketing ──────────────────────────────────────────────────────────
# ATF  : HPOV | SIG | Item Carousel   (content_zone IN contentzone1–6)
# BTF  : Navigation | Content | Carousels | Utility  (all other zones)
#
# ⚠️  MM SIG LAUNCH — May 14, 2026 (Thursday night)
# Multi-Modal SIG changed ATF zone assignments:
#   BEFORE May 14 → HPOV in contentzone3, SIG in contentzone4/5/6
#   AFTER  May 14 → HPOV in contentzone2, SIG Top Picks in contentzone3,
#                   Rye + Site Merch carousels in contentzone4/5/6
# Bucketing below uses hp_module_name as primary key (unchanged by MM SIG),
# so classification remains correct across both periods. The ATF boundary
# (contentzone1–6) is also unchanged.
# Any metric spikes after May 15, 2026 → attribute to MM SIG first.
NEW_MODULE_CASE = f"""
  CASE
    -- HPOV: AutoScroll Cards 1-5
    -- Pre-MM SIG:  contentzone3
    -- Post-MM SIG (May 14, 2026+): contentzone2
    WHEN hp_module_name IN (
      'AutoScroll Card 1','AutoScroll Card 2','AutoScroll Card 3',
      'AutoScroll Card 4','AutoScroll Card 5'
    ) AND LOWER(content_zone) IN ('{_ATF_SQL}')
    THEN 'HPOV'

    -- SIG: SIG Cards 1-6
    -- Pre-MM SIG:  contentzone4/5/6
    -- Post-MM SIG: Top Picks → contentzone3; Rye/Site Merch → contentzone4/5/6
    WHEN hp_module_name IN (
      'SIG Card 1','SIG Card 2','SIG Card 3',
      'SIG Card 4','SIG Card 5','SIG Card 6'
    ) AND LOWER(content_zone) IN ('{_ATF_SQL}')
    THEN 'SIG'

    -- Item Carousel: moduletype = ItemCarousel, ATF zones only
    WHEN LOWER(COALESCE(moduletype,'')) = 'itemcarousel'
      AND LOWER(content_zone) IN ('{_ATF_SQL}')
    THEN 'Item Carousel'

    WHEN hp_module_type = 'Navigation'
      AND LOWER(content_zone) NOT IN ('{_ATF_SQL}')
    THEN 'Navigation'

    WHEN hp_module_type = 'Content'
      AND LOWER(content_zone) NOT IN ('{_ATF_SQL}')
    THEN 'Content'

    WHEN hp_module_type = 'Carousel'
      AND LOWER(content_zone) NOT IN ('{_ATF_SQL}')
    THEN 'Carousels'

    WHEN hp_module_type = 'Utility'
    THEN 'Utility'
  END
"""

# ── Exclude video / interactive carousels ─────────────────────────────────────
VIDEO_CAROUSEL_FILTER = (
    "AND COALESCE(moduletype,'') NOT IN ('VideoCarousel','InteractiveImageCarousel')"
)

# ── Canonical Merch content-type filter (content_served_by approach) ──────────
CONTENT_TYPE_FILTER = """
AND CASE
  WHEN LOWER(IFNULL(content_served_by,'')) = 'ads'
    THEN 'WMC'
  WHEN LOWER(IFNULL(disable_content_personalization,'')) LIKE '%true%'
    THEN 'Merch'
  WHEN LOWER(IFNULL(disable_content_personalization,'')) LIKE '%false%'
    AND LOWER(IFNULL(personalized_asset,'')) = 'default'
    AND session_start_dt <= '2025-03-01'
    AND LOWER(IFNULL(content_zone,'')) = 'contentzone3'
    AND LOWER(IFNULL(hp_module_name,'')) IN (
      'autoscroll card 1','autoscroll card 2','autoscroll card 3'
    )
    THEN 'WMC'
  WHEN LOWER(IFNULL(disable_content_personalization,'')) LIKE '%false%'
    AND LOWER(IFNULL(personalized_asset,'')) = 'default'
    AND (
      (
        LOWER(IFNULL(content_zone,'')) IN ('contentzone8','contentzone9')
        AND LOWER(IFNULL(hp_module_name,'')) = 'adjustable banner small'
      )
      OR
      (
        LOWER(IFNULL(content_zone,'')) IN ('contentzone10','contentzone11')
        AND LOWER(IFNULL(hp_module_name,'')) = 'triple pack small'
      )
    )
    THEN 'WMC'
  ELSE 'Merch'
END = 'Merch'
"""

MODULE_ORDER = ['HPOV','SIG','Item Carousel','Navigation','Content','Carousels','Utility']
ATF_MODULES  = {'HPOV','SIG','Item Carousel'}
BTF_MODULES  = {'Navigation','Content','Carousels','Utility'}


# ─────────────────────────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────────────────────────

def get_walmart_fiscal_week_dates(selected_date: str):
    """Saturday → selected_date (current) and same days one week prior."""
    dt      = datetime.strptime(selected_date, "%Y-%m-%d")
    weekday = dt.weekday()                         # Mon=0 … Sun=6
    days_since_saturday = 0 if weekday == 5 else (1 if weekday == 6 else weekday + 2)
    sat          = dt - timedelta(days=days_since_saturday)
    curr_start   = sat.strftime("%Y-%m-%d")
    curr_end     = dt.strftime("%Y-%m-%d")
    prev_start   = (sat - timedelta(days=7)).strftime("%Y-%m-%d")
    prev_end     = (dt  - timedelta(days=7)).strftime("%Y-%m-%d")
    return curr_start, curr_end, prev_start, prev_end


def fmt_pct(value, decimals=2):
    if value is None:
        return "—"
    return f"{round(value, decimals)}%"


def fmt_wow(value):
    """Return (display_text, css_class) for a WoW value."""
    if value is None:
        return ("—", "")
    sign  = "+" if value > 0 else ""
    text  = f"{sign}{value}%"
    css   = "green" if value > 0 else ("red" if value < 0 else "")
    return (text, css)


# ─────────────────────────────────────────────────────────────────────────────
#  BigQuery: single query → FYTD baseline + current week
# ─────────────────────────────────────────────────────────────────────────────

def get_engagement_data(start_date: str, end_date: str):
    """
    Returns one row per module with:
      ctr_baseline  – FYTD CTR (Jan 31 2026 → max date in dataset)
      ctr_pct       – current-week CTR
      ctr_wow_pct   – (current_ctr / fytd_ctr − 1) × 100
      atc_baseline  – FYTD ATC contribution %
      atc_pct       – current-week ATC contribution %
      atc_wow_pct   – (current_contrib / fytd_contrib − 1) × 100
    """
    query = f"""
    WITH
    -- ── FYTD (Jan 31 → latest available date) ───────────────────────────
    fytd AS (
      SELECT
        {NEW_MODULE_CASE} AS Module,
        SUM(overall_click_count)  AS fytd_clicks,
        SUM(module_view_count)    AS fytd_impressions,
        SAFE_DIVIDE(SUM(overall_click_count), SUM(module_view_count)) AS fytd_ctr,
        SUM(total_atc_count)      AS fytd_atc
      FROM `{BQ_TABLE}`
      WHERE session_start_dt BETWEEN '{FYTD_START}' AND (
          SELECT MAX(session_start_dt)
          FROM `{BQ_TABLE}`
          WHERE session_start_dt >= '{FYTD_START}'
        )
        {VIDEO_CAROUSEL_FILTER}
        {CONTENT_TYPE_FILTER}
      GROUP BY Module
      HAVING Module IS NOT NULL
    ),
    fytd_total AS (
      SELECT SUM(fytd_atc) AS total_fytd_atc FROM fytd
    ),

    -- ── Current fiscal partial week ──────────────────────────────────────
    curr AS (
      SELECT
        {NEW_MODULE_CASE} AS Module,
        SUM(overall_click_count)  AS curr_clicks,
        SUM(module_view_count)    AS curr_impressions,
        SAFE_DIVIDE(SUM(overall_click_count), SUM(module_view_count)) AS curr_ctr,
        SUM(total_atc_count)      AS curr_atc
      FROM `{BQ_TABLE}`
      WHERE session_start_dt BETWEEN '{start_date}' AND '{end_date}'
        {VIDEO_CAROUSEL_FILTER}
        {CONTENT_TYPE_FILTER}
      GROUP BY Module
      HAVING Module IS NOT NULL
    ),
    curr_total AS (
      SELECT SUM(curr_atc) AS total_curr_atc FROM curr
    )

    SELECT
      c.Module,
      -- CTR Baseline = FYTD CTR
      ROUND(f.fytd_ctr * 100, 2)   AS ctr_baseline,
      -- Current CTR %
      ROUND(c.curr_ctr * 100, 2)   AS ctr_pct,
      -- WoW CTR = (current_ctr / fytd_ctr − 1) × 100
      ROUND((SAFE_DIVIDE(c.curr_ctr, f.fytd_ctr) - 1) * 100, 1) AS ctr_wow_pct,
      -- ATC Baseline = FYTD contribution %
      ROUND(SAFE_DIVIDE(f.fytd_atc, ft.total_fytd_atc) * 100, 2) AS atc_baseline,
      -- Current ATC contribution %
      ROUND(SAFE_DIVIDE(c.curr_atc, ct.total_curr_atc) * 100, 2) AS atc_pct,
      -- WoW ATC = (current_contrib / fytd_contrib − 1) × 100
      ROUND(
        (SAFE_DIVIDE(
          SAFE_DIVIDE(c.curr_atc,  ct.total_curr_atc),
          SAFE_DIVIDE(f.fytd_atc,  ft.total_fytd_atc)
        ) - 1) * 100,
      1) AS atc_wow_pct

    FROM curr c
    LEFT JOIN fytd f ON c.Module = f.Module
    CROSS JOIN fytd_total ft
    CROSS JOIN curr_total  ct

    ORDER BY
      CASE c.Module
        WHEN 'HPOV'          THEN 1
        WHEN 'SIG'           THEN 2
        WHEN 'Item Carousel' THEN 3
        WHEN 'Navigation'    THEN 4
        WHEN 'Content'       THEN 5
        WHEN 'Carousels'     THEN 6
        WHEN 'Utility'       THEN 7
        ELSE 99
      END
    """
    try:
        rows = list(client.query(query, job_config=JOB_CONFIG).result(timeout=90))
        return [{
            "module":       r.Module,
            "ctr_baseline": r.ctr_baseline,
            "ctr_pct":      r.ctr_pct,
            "ctr_wow_pct":  r.ctr_wow_pct,
            "atc_baseline": r.atc_baseline,
            "atc_pct":      r.atc_pct,
            "atc_wow_pct":  r.atc_wow_pct,
        } for r in rows]
    except Exception as e:
        print(f"[BQ Error] {e}")
        return []


# ─────────────────────────────────────────────────────────────────────────────
#  HTML table renderer  (merged ATF / BTF placement cells)
# ─────────────────────────────────────────────────────────────────────────────

def render_engagement_table(data: list) -> str:
    if not data:
        return '<p style="color:#6b7280;font-style:italic;">No data returned from BigQuery. Check your credentials and date range.</p>'

    by_module = {r["module"]: r for r in data}
    ordered   = [by_module[m] for m in MODULE_ORDER if m in by_module]

    atf_rows = [r for r in ordered if r["module"] in ATF_MODULES]
    btf_rows = [r for r in ordered if r["module"] in BTF_MODULES]
    placement_done = {"ATF": False, "BTF": False}

    TH  = 'style="padding:10px 14px;text-align:center;font-weight:700;border:1px solid #1a3a60;white-space:nowrap;"'
    TH_L= 'style="padding:10px 14px;text-align:left;font-weight:700;border:1px solid #1a3a60;white-space:nowrap;"'
    TD  = 'style="padding:9px 14px;text-align:center;border:1px solid #d1d5db;"'
    TD_L= 'style="padding:9px 14px;text-align:left;border:1px solid #d1d5db;"'

    html = f'''
<table style="border-collapse:collapse;width:100%;font-family:\'Segoe UI\',Arial,sans-serif;font-size:13px;margin-top:4px;">
  <thead>
    <tr style="background:#041e42;color:white;">
      <th {TH}>Homepage Placement</th>
      <th {TH}>Module</th>
      <th {TH}>CTR Baseline</th>
      <th {TH}>CTR%</th>
      <th {TH}>WoW</th>
      <th {TH}>ATC Baseline</th>
      <th {TH}>ATC%</th>
      <th {TH}>WoW</th>
      <th {TH}>Engagement Performance</th>
      <th {TH_L}>Insights</th>
    </tr>
  </thead>
  <tbody>
'''
    COLOR = {"green": "#16a34a", "red": "#dc2626", "": "#1a1a1a"}
    ALT_MODS = {"SIG", "Content", "Utility"}

    for row in ordered:
        mod       = row["module"]
        placement = "ATF" if mod in ATF_MODULES else "BTF"
        group     = atf_rows if placement == "ATF" else btf_rows
        bg        = "#f8f9fa" if mod in ALT_MODS else "#ffffff"

        ctr_wow_txt, ctr_wow_css = fmt_wow(row["ctr_wow_pct"])
        atc_wow_txt, atc_wow_css = fmt_wow(row["atc_wow_pct"])
        ctr_color = COLOR[ctr_wow_css]
        atc_color = COLOR[atc_wow_css]

        tr = f'<tr style="background:{bg};">'

        # ── Homepage Placement cell (merged) ──
        if not placement_done[placement]:
            placement_done[placement] = True
            rowspan = len(group)
            pl_bg   = "#dce8f5" if placement == "ATF" else "#e8f0e8"
            tr += (
                f'<td rowspan="{rowspan}" '
                f'style="padding:10px 14px;text-align:center;font-weight:800;'
                f'font-size:16px;border:1px solid #d1d5db;background:{pl_bg};'
                f'vertical-align:middle;color:#041e42;">{placement}</td>'
            )

        tr += f'''
      <td {TD}><strong>{mod}</strong></td>
      <td {TD}>{fmt_pct(row["ctr_baseline"])}</td>
      <td {TD}>{fmt_pct(row["ctr_pct"])}</td>
      <td style="padding:9px 14px;text-align:center;border:1px solid #d1d5db;font-weight:700;color:{ctr_color};">{ctr_wow_txt}</td>
      <td {TD}>{fmt_pct(row["atc_baseline"])}</td>
      <td {TD}>{fmt_pct(row["atc_pct"])}</td>
      <td style="padding:9px 14px;text-align:center;border:1px solid #d1d5db;font-weight:700;color:{atc_color};">{atc_wow_txt}</td>
      <td {TD}></td>
      <td {TD_L}></td>
    </tr>'''
        html += tr

    html += "  </tbody>\n</table>"
    return html


# ─────────────────────────────────────────────────────────────────────────────
#  PPT generator
# ─────────────────────────────────────────────────────────────────────────────

def generate_ppt_bytes(data: list, current_start: str, current_end: str) -> BytesIO:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN

    NAVY    = RGBColor(4,   30,  66)
    WHITE   = RGBColor(255, 255, 255)
    GREEN   = RGBColor(22,  163, 74)
    RED     = RGBColor(220, 38,  38)
    ATF_BG  = RGBColor(220, 232, 245)
    BTF_BG  = RGBColor(220, 237, 220)
    HDR_BDR = RGBColor(26,  58,  96)
    ROW_ALT = RGBColor(248, 249, 250)

    prs = Presentation()
    prs.slide_width  = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

    # ── Title ──────────────────────────────────────────────────────────────
    tb = slide.shapes.add_textbox(Inches(0.35), Inches(0.10), Inches(15.3), Inches(0.5))
    p  = tb.text_frame.paragraphs[0]
    p.text = "Homepage Engagement Performance"
    p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = NAVY

    tb2 = slide.shapes.add_textbox(Inches(0.35), Inches(0.58), Inches(15.3), Inches(0.35))
    p2  = tb2.text_frame.paragraphs[0]
    p2.text = (f"Week: {current_start} → {current_end}  |  "
               f"CTR Baseline = FYTD (Jan 31 2026 → latest)  |  "
               f"ATC Baseline = FYTD Contribution %  |  Merch only")
    p2.font.size = Pt(10); p2.font.color.rgb = RGBColor(100, 100, 100)

    # ── Build ordered data ─────────────────────────────────────────────────
    by_module = {r["module"]: r for r in data}
    ordered   = [by_module[m] for m in MODULE_ORDER if m in by_module]

    n_rows = len(ordered) + 1   # +1 header
    n_cols = 10

    # column widths (inches) — total ≈ 15.3
    col_w = [1.05, 1.4, 1.35, 1.15, 0.95, 1.35, 1.15, 0.95, 2.0, 3.9]

    tbl = slide.shapes.add_table(
        n_rows, n_cols,
        Inches(0.35), Inches(0.98),
        Inches(sum(col_w)), Inches(7.75)
    ).table

    for i, w in enumerate(col_w):
        tbl.columns[i].width = Inches(w)

    # ── Header row ─────────────────────────────────────────────────────────
    headers = [
        "Homepage\nPlacement", "Module",
        "CTR Baseline", "CTR%", "WoW",
        "ATC Baseline", "ATC%", "WoW",
        "Engagement\nPerformance", "Insights"
    ]
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
        tf = cell.text_frame; tf.word_wrap = True
        p  = tf.paragraphs[0]
        p.text = h; p.alignment = PP_ALIGN.CENTER
        p.font.color.rgb = WHITE; p.font.bold = True; p.font.size = Pt(10)

    # ── Data rows ──────────────────────────────────────────────────────────
    atf_indices = [i+1 for i, r in enumerate(ordered) if r["module"] in ATF_MODULES]
    btf_indices = [i+1 for i, r in enumerate(ordered) if r["module"] in BTF_MODULES]
    ALT_MODS_SET = {"SIG", "Content", "Utility"}

    for i, row in enumerate(ordered):
        ri  = i + 1
        mod = row["module"]

        def wow_str(v):
            if v is None: return "—"
            return f"{'+'if v>0 else ''}{v}%"

        vals = [
            "ATF" if mod in ATF_MODULES else "BTF",
            mod,
            fmt_pct(row["ctr_baseline"]),
            fmt_pct(row["ctr_pct"]),
            wow_str(row["ctr_wow_pct"]),
            fmt_pct(row["atc_baseline"]),
            fmt_pct(row["atc_pct"]),
            wow_str(row["atc_wow_pct"]),
            "",   # Engagement Performance — empty
            "",   # Insights — empty
        ]

        row_bg = ROW_ALT if mod in ALT_MODS_SET else WHITE

        for j, val in enumerate(vals):
            cell = tbl.cell(ri, j)
            cell.fill.solid(); cell.fill.fore_color.rgb = row_bg
            tf = cell.text_frame; tf.word_wrap = True
            p  = tf.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.alignment = PP_ALIGN.LEFT if j == 9 else PP_ALIGN.CENTER

            # WoW colour coding
            if j == 4 and row["ctr_wow_pct"] is not None:
                p.font.bold = True
                p.font.color.rgb = GREEN if row["ctr_wow_pct"] > 0 else (RED if row["ctr_wow_pct"] < 0 else RGBColor(0,0,0))
            elif j == 7 and row["atc_wow_pct"] is not None:
                p.font.bold = True
                p.font.color.rgb = GREEN if row["atc_wow_pct"] > 0 else (RED if row["atc_wow_pct"] < 0 else RGBColor(0,0,0))

    # ── Merge Placement column cells ───────────────────────────────────────
    for idx_list, label, bg in [
        (atf_indices, "ATF", ATF_BG),
        (btf_indices, "BTF", BTF_BG),
    ]:
        if len(idx_list) >= 2:
            tbl.cell(idx_list[0], 0).merge(tbl.cell(idx_list[-1], 0))
        if idx_list:
            mc = tbl.cell(idx_list[0], 0)
            mc.fill.solid(); mc.fill.fore_color.rgb = bg
            tf = mc.text_frame; tf.word_wrap = False
            p  = tf.paragraphs[0]
            p.text = label; p.alignment = PP_ALIGN.CENTER
            p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = NAVY

    buf = BytesIO()
    prs.save(buf)
    buf.seek(0)
    return buf


# ─────────────────────────────────────────────────────────────────────────────
#  Routes
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def home(selected_date: str = Query(default=datetime.today().strftime("%Y-%m-%d"))):
    curr_start, curr_end, prev_start, prev_end = get_walmart_fiscal_week_dates(selected_date)
    data       = get_engagement_data(curr_start, curr_end)
    table_html = render_engagement_table(data)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>WBR — Homepage Engagement Performance</title>
  <style>
    *   {{ box-sizing:border-box; margin:0; padding:0; }}
    body{{ background:#f0f2f5; font-family:'Segoe UI',Arial,sans-serif; padding:24px; }}
    .card{{ background:white; border-radius:12px; box-shadow:0 2px 14px rgba(0,0,0,.09); padding:30px; max-width:1500px; margin:0 auto; }}

    /* ── top bar ── */
    .topbar{{ display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:22px; gap:16px; flex-wrap:wrap; }}
    .title  {{ font-size:22px; font-weight:800; color:#041e42; }}
    .subtitle{{ font-size:12px; color:#6b7280; margin-top:5px; line-height:1.6; }}

    /* ── date form ── */
    .datebar{{ background:#f8f9fa; border-radius:8px; padding:14px 18px; margin-bottom:22px;
               display:flex; align-items:center; gap:14px; flex-wrap:wrap; border:1px solid #e5e7eb; }}
    .datebar label{{ font-size:13px; font-weight:600; color:#374151; }}
    .datebar input {{ border:1px solid #d1d5db; border-radius:6px; padding:7px 11px; font-size:13px; }}
    .datebar button{{ background:#041e42; color:white; border:none; border-radius:6px;
                      padding:8px 20px; font-size:13px; cursor:pointer; font-weight:600; }}
    .datebar button:hover{{ background:#0a3161; }}

    /* ── week badges ── */
    .badges{{ display:flex; gap:10px; flex-wrap:wrap; }}
    .badge {{ padding:5px 13px; border-radius:6px; font-size:12px; font-weight:600; white-space:nowrap; }}
    .badge-c{{ background:#dce8f5; border:1px solid #041e42; color:#041e42; }}
    .badge-p{{ background:#f3f4f6; border:1px solid #9ca3af; color:#6b7280; }}

    /* ── download button ── */
    .dl-btn{{ background:#0071ce; color:white; border:none; border-radius:8px;
              padding:10px 22px; font-size:14px; cursor:pointer; font-weight:700;
              text-decoration:none; display:inline-flex; align-items:center; gap:8px;
              white-space:nowrap; }}
    .dl-btn:hover{{ background:#005ba0; }}

    /* ── legend / note ── */
    .legend{{ margin-top:12px; font-size:12px; color:#6b7280; }}
    .g{{ color:#16a34a; font-weight:700; }}
    .r{{ color:#dc2626; font-weight:700; }}
    .note{{ font-size:11px; color:#9ca3af; margin-top:12px; padding-top:12px; border-top:1px solid #f0f2f5; line-height:1.8; }}
    code{{ background:#f3f4f6; padding:1px 5px; border-radius:3px; font-size:11px; }}
  </style>
</head>
<body>
<div class="card">

  <!-- ── Top bar ─────────────────────────────────────────── -->
  <div class="topbar">
    <div>
      <div class="title">📊 Homepage Engagement Performance</div>
      <div class="subtitle">
        CTR Baseline = FYTD (Jan 31 2026 → latest available date) &nbsp;|&nbsp;
        ATC Baseline = FYTD ATC Contribution % &nbsp;|&nbsp;
        WoW = Current partial week vs FYTD baseline<br>
        ATF = contentZone1–6 &nbsp;|&nbsp; BTF = all other zones &nbsp;|&nbsp; Merch only
      </div>
    </div>
    <a class="dl-btn" href="/download-ppt?selected_date={selected_date}">⬇&nbsp; Download PPT</a>
  </div>

  <!-- ── Date picker ─────────────────────────────────────── -->
  <div class="datebar">
    <form method="get" style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
      <label>Select Date (Fiscal Week End)</label>
      <input type="date" name="selected_date" value="{selected_date}">
      <button type="submit">Generate Report</button>
    </form>
    <div class="badges">
      <span class="badge badge-c">📅 Current: {curr_start} → {curr_end}</span>
      <span class="badge badge-p">🔙 Prior: {prev_start} → {prev_end}</span>
    </div>
  </div>

  <!-- ── Table ───────────────────────────────────────────── -->
  <div style="overflow-x:auto;">
    {table_html}
  </div>

  <!-- ── Legend ──────────────────────────────────────────── -->
  <div class="legend">
    <span class="g">■ Green WoW</span> = current week above FYTD baseline &nbsp;&nbsp;
    <span class="r">■ Red WoW</span> = current week below FYTD baseline
  </div>

  <div class="note">
    Source: <code>hp_summary_asset</code> &nbsp;|&nbsp;
    Content Type: Merch only (canonical <code>content_served_by</code> logic) &nbsp;|&nbsp;
    VideoCarousel &amp; InteractiveImageCarousel excluded &nbsp;|&nbsp;
    WoW formula: (Current / FYTD − 1) × 100
  </div>

</div>
</body>
</html>"""
    return HTMLResponse(content=html)


@app.get("/download-ppt")
async def download_ppt(selected_date: str = Query(default=datetime.today().strftime("%Y-%m-%d"))):
    curr_start, curr_end, _, _ = get_walmart_fiscal_week_dates(selected_date)
    data     = get_engagement_data(curr_start, curr_end)
    ppt_buf  = generate_ppt_bytes(data, curr_start, curr_end)
    filename = f"wbr-engagement-{curr_start}-to-{curr_end}.pptx"
    return StreamingResponse(
        ppt_buf,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
