from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from google.cloud import bigquery
from datetime import datetime, timedelta

app = FastAPI(title="WBR Report App")
client = bigquery.Client()
JOB_CONFIG = bigquery.QueryJobConfig(
    maximum_bytes_billed=50_000_000_000  # 50GB cap
)

# ── Data source ─────────────────────────────────────────────────
# Switched from HPsummary → hp_summary_asset (new authoritative table)
BQ_TABLE = "wmt-site-content-strategy.scs_production.hp_summary_asset"

# ── Column aliases (hp_summary_asset naming) ────────────────────
# viewed_impressions  → module_view_count
# language_split      → lang_cd  (value: 'English')
# Content_Type        → derived via CONTENT_TYPE_FILTER CASE (see below)
# Content_Zone        → content_zone  (lowercase)
# moduleType          → moduletype    (lowercase)
# Carousel_Name       → carousel_name (lowercase)

# ── Zone constants ──────────────────────────────────────────────
ATF_ZONES = (
    "'contentzone1','contentzone2','contentzone3',"
    "'contentzone4','contentzone5','contentzone6',"
    "'topcontentzone1','topcontentzone2','topcontentzone3',"
    "'topcontentzone4','topcontentzone5','topcontentzone6'"
)

# Single source of truth for module bucketing.
# Priority order matters — first match wins in CASE.
MODULE_CASE = f"""
  CASE
    WHEN hp_module_name IN (
      'AutoScroll Card 1','AutoScroll Card 2','AutoScroll Card 3',
      'AutoScroll Card 4','AutoScroll Card 5'
    ) THEN 'HPOV'
    WHEN hp_module_name IN (
      'SIG Card 1','SIG Card 2','SIG Card 3',
      'SIG Card 4','SIG Card 5','SIG Card 6'
    ) AND LOWER(content_zone) IN ('contentzone4','contentzone5','contentzone6')
    THEN 'ATF Carousels (SIG)'
    WHEN LOWER(content_zone) IN ('contentzone3','contentzone4','contentzone5','contentzone6')
      AND hp_module_type = 'Carousel'
    THEN 'ATF Carousels'
    WHEN hp_module_name = 'Walmart+ Banner'
      AND hp_module_type != 'Utility'
    THEN 'Walmart+ Banner'
    WHEN hp_module_type = 'Utility'
    THEN 'Utility'
    WHEN hp_module_type = 'Navigation'
      AND LOWER(content_zone) NOT IN ({ATF_ZONES})
    THEN 'BTF Navigation'
    WHEN hp_module_type = 'Content'
      AND LOWER(content_zone) NOT IN ({ATF_ZONES})
    THEN 'BTF Content'
    WHEN hp_module_type = 'Carousel'
      AND LOWER(content_zone) NOT IN ({ATF_ZONES})
    THEN 'BTF Carousels'
  END
"""

# Global filter: exclude VideoCarousel from ALL analysis
VIDEO_CAROUSEL_FILTER = "AND COALESCE(moduletype, '') NOT IN ('VideoCarousel', 'InteractiveImageCarousel')"

# ── Content Type filter — Merch only ────────────────────────────
# Translated from Looker formula into BigQuery CASE.
# Rows where the derived type = 'WMC' are excluded; only 'Merch' kept.
#
# WMC conditions:
#   1. content_served_by = 'ads'
#   2. disable_content_personalization CONTAINS 'false'
#      AND personalized_asset = 'default'
#      AND session_start_dt <= 2025-03-01
#      AND content_zone = contentzone3
#      AND hp_module_name IN (AutoScroll Card 1/2/3)
#   3. disable_content_personalization CONTAINS 'false'
#      AND personalized_asset = 'default'
#      AND (adjustable banner small in zone 8/9
#           OR triple pack small in zone 10/11)
# Merch conditions:
#   4. disable_content_personalization CONTAINS 'true'  → always Merch
#   5. Everything else                                  → Merch
CONTENT_TYPE_FILTER = """
AND CASE
  WHEN LOWER(IFNULL(content_served_by, '')) = 'ads'
    THEN 'WMC'
  WHEN LOWER(IFNULL(disable_content_personalization, '')) LIKE '%true%'
    THEN 'Merch'
  WHEN LOWER(IFNULL(disable_content_personalization, '')) LIKE '%false%'
    AND LOWER(IFNULL(personalized_asset, '')) = 'default'
    AND session_start_dt <= '2025-03-01'
    AND LOWER(IFNULL(content_zone, '')) = 'contentzone3'
    AND LOWER(IFNULL(hp_module_name, '')) IN (
      'autoscroll card 1','autoscroll card 2','autoscroll card 3'
    )
    THEN 'WMC'
  WHEN LOWER(IFNULL(disable_content_personalization, '')) LIKE '%false%'
    AND LOWER(IFNULL(personalized_asset, '')) = 'default'
    AND (
      (
        LOWER(IFNULL(content_zone, '')) IN ('contentzone8','contentzone9')
        AND LOWER(IFNULL(hp_module_name, '')) = 'adjustable banner small'
      )
      OR
      (
        LOWER(IFNULL(content_zone, '')) IN ('contentzone10','contentzone11')
        AND LOWER(IFNULL(hp_module_name, '')) = 'triple pack small'
      )
    )
    THEN 'WMC'
  ELSE 'Merch'
END = 'Merch'
"""


def get_dynamic_insights(start_date: str, end_date: str):
    """Generate dynamic insights based on actual BQ data for the selected date range."""
    insights = {}

    # HPOV insight — top performing messages by CTR
    try:
        hpov_query = f"""
        SELECT
          message_name,
          SUM(module_view_count) AS impressions,
          ROUND(SAFE_DIVIDE(SUM(overall_click_count), SUM(module_view_count)) * 100, 2) AS ctr
        FROM `{BQ_TABLE}`
        WHERE hp_module_name IN (
            'AutoScroll Card 1','AutoScroll Card 2','AutoScroll Card 3',
            'AutoScroll Card 4','AutoScroll Card 5'
          )
          AND lang_cd = 'English'
          AND session_start_dt BETWEEN '{start_date}' AND '{end_date}'
          {VIDEO_CAROUSEL_FILTER}
          {CONTENT_TYPE_FILTER}
        GROUP BY message_name
        HAVING SUM(module_view_count) > 500000
        ORDER BY ctr DESC
        LIMIT 3
        """
        result = list(client.query(hpov_query).result(timeout=45))
        if result:
            top = result[0]
            second = result[1] if len(result) > 1 else None
            insight = f'"{top.message_name}" ({top.ctr}% CTR) top performer'
            if second:
                insight += f'; "{second.message_name}" ({second.ctr}% CTR) strong.'
            insights['HPOV'] = insight
    except Exception as e:
        insights['HPOV'] = 'Data unavailable.'

    # SIG insight — top carousel by CTR
    try:
        sig_query = f"""
        SELECT
          carousel_name,
          ROUND(SAFE_DIVIDE(SUM(overall_click_count), SUM(module_view_count)) * 100, 2) AS ctr
        FROM `{BQ_TABLE}`
        WHERE hp_module_name IN (
            'SIG Card 1','SIG Card 2','SIG Card 3',
            'SIG Card 4','SIG Card 5','SIG Card 6'
          )
          AND LOWER(content_zone) IN ('contentzone4','contentzone5','contentzone6')
          AND lang_cd = 'English'
          AND session_start_dt BETWEEN '{start_date}' AND '{end_date}'
          {VIDEO_CAROUSEL_FILTER}
          {CONTENT_TYPE_FILTER}
        GROUP BY carousel_name
        HAVING SUM(module_view_count) > 100000
        ORDER BY ctr DESC
        LIMIT 2
        """
        result = list(client.query(sig_query).result(timeout=45))
        if result:
            top = result[0]
            insight = f'"{top.carousel_name}" ({top.ctr}% CTR) leading.'
            insights['ATF Carousels (SIG)'] = insight
    except Exception:
        insights['ATF Carousels (SIG)'] = 'Data unavailable.'

    # Default insights for other modules
    insights.setdefault('ATF Carousels',    'See message-level breakdown for details.')
    insights.setdefault('Walmart+ Banner',  'See message-level breakdown for details.')
    insights.setdefault('Utility',          'Order tracking tools driving engagement.')
    insights.setdefault('BTF Navigation',   'General navigation patterns observed.')
    insights.setdefault('BTF Content',      'See message-level breakdown for details.')
    insights.setdefault('BTF Carousels',    'See message-level breakdown for details.')

    return insights


def get_walmart_fiscal_week_dates(selected_date: str):
    """Calculate Walmart fiscal week dates (Sat–Fri) based on selected date.
    Returns current week (Sat → selected_date) and previous week (same days -7).
    """
    dt = datetime.strptime(selected_date, "%Y-%m-%d")
    weekday = dt.weekday()  # Monday=0 … Sunday=6

    # Python weekday: Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
    if weekday == 5:       # Saturday
        days_since_saturday = 0
    elif weekday == 6:     # Sunday
        days_since_saturday = 1
    else:                  # Mon–Fri
        days_since_saturday = weekday + 2

    current_saturday = dt - timedelta(days=days_since_saturday)
    current_start    = current_saturday.strftime("%Y-%m-%d")
    current_end      = dt.strftime("%Y-%m-%d")

    prev_start = (current_saturday - timedelta(days=7)).strftime("%Y-%m-%d")
    prev_end   = (dt - timedelta(days=7)).strftime("%Y-%m-%d")

    return current_start, current_end, prev_start, prev_end


def get_wbr_data(
    start_date: str, end_date: str,
    prev_start: str, prev_end: str,
    platform: str = None
):
    """Query hp_summary_asset for WBR metrics, current week vs previous week."""
    platform_filter = f"AND experience_lvl2 = '{platform}'" if platform else ""

    query = f"""
    WITH current_week AS (
      SELECT
        {MODULE_CASE} AS Module,
        SUM(overall_click_count) AS current_clicks,
        SUM(module_view_count)   AS current_impressions,
        SUM(total_atc_count)     AS current_atc,
        SAFE_DIVIDE(SUM(overall_click_count), SUM(module_view_count)) AS current_ctr
      FROM `{BQ_TABLE}`
      WHERE session_start_dt BETWEEN '{start_date}' AND '{end_date}'
        AND lang_cd = 'English'
        {VIDEO_CAROUSEL_FILTER}
        {CONTENT_TYPE_FILTER}
        {platform_filter}
      GROUP BY Module
      HAVING Module IS NOT NULL
    ),
    previous_week AS (
      SELECT
        {MODULE_CASE} AS Module,
        SUM(overall_click_count) AS prev_clicks,
        SUM(module_view_count)   AS prev_impressions,
        SAFE_DIVIDE(SUM(overall_click_count), SUM(module_view_count)) AS prev_ctr,
        SUM(total_atc_count)     AS prev_atc
      FROM `{BQ_TABLE}`
      WHERE session_start_dt BETWEEN '{prev_start}' AND '{prev_end}'
        AND lang_cd = 'English'
        {VIDEO_CAROUSEL_FILTER}
        {CONTENT_TYPE_FILTER}
        {platform_filter}
      GROUP BY Module
      HAVING Module IS NOT NULL
    ),
    totals_current AS (
      SELECT
        SUM(current_clicks) AS total_clicks,
        SUM(current_atc)    AS total_atc
      FROM current_week
    ),
    totals_previous AS (
      SELECT
        SUM(prev_clicks) AS total_prev_clicks,
        SUM(prev_atc)    AS total_prev_atc
      FROM previous_week
    )
    SELECT
      c.Module,
      ROUND(c.current_ctr * 100, 2)                                          AS ctr_pct,
      ROUND((SAFE_DIVIDE(c.current_ctr, p.prev_ctr) - 1) * 100, 1)           AS ctr_wow_pct,
      ROUND(SAFE_DIVIDE(c.current_clicks, t.total_clicks) * 100, 1)           AS clicks_pct,
      -- Clicks WoW: compare contribution share % vs prior week
      ROUND((SAFE_DIVIDE(
        SAFE_DIVIDE(c.current_clicks, t.total_clicks),
        SAFE_DIVIDE(p.prev_clicks,    tp.total_prev_clicks)
      ) - 1) * 100, 1)                                                        AS clicks_wow_pct,
      ROUND(SAFE_DIVIDE(c.current_atc, t.total_atc) * 100, 1)                 AS atc_pct,
      -- ATC WoW: compare contribution share % vs prior week
      ROUND((SAFE_DIVIDE(
        SAFE_DIVIDE(c.current_atc, t.total_atc),
        SAFE_DIVIDE(p.prev_atc,    tp.total_prev_atc)
      ) - 1) * 100, 1)                                                        AS atc_wow_pct
    FROM current_week   c
    LEFT JOIN previous_week p ON c.Module = p.Module
    CROSS JOIN totals_current  t
    CROSS JOIN totals_previous tp
    ORDER BY
      CASE c.Module
        WHEN 'HPOV'               THEN 1
        WHEN 'ATF Carousels (SIG)' THEN 2
        WHEN 'ATF Carousels'      THEN 3
        WHEN 'Walmart+ Banner'    THEN 4
        WHEN 'Utility'            THEN 5
        WHEN 'BTF Navigation'     THEN 6
        WHEN 'BTF Content'        THEN 7
        WHEN 'BTF Carousels'      THEN 8
      END
    """

    try:
        result = client.query(query).result(timeout=45)
        return [{
            "module":        row.Module,
            "ctr_pct":       row.ctr_pct       or 0,
            "ctr_wow_pct":   row.ctr_wow_pct,
            "clicks_pct":    row.clicks_pct    or 0,
            "clicks_wow_pct": row.clicks_wow_pct,
            "atc_pct":       row.atc_pct,
            "atc_wow_pct":   row.atc_wow_pct,
        } for row in result]
    except Exception as e:
        print(f"BQ Error: {e}")
        return []


def format_wow(value, neutral_threshold=0):
    """Format WoW percentage with colour class.
    neutral_threshold: negative values whose abs() is <= this render black (no colour).
    E.g. neutral_threshold=5 means -3.3% shows black, -10% shows red.
    """
    if value is None:
        return {"value": "\u2014", "class": ""}
    sign = "+" if value > 0 else ""
    if value > 0:
        css_class = "green"
    elif value < 0 and abs(value) > neutral_threshold:
        css_class = "red"
    else:
        css_class = "neutral"  # neutral / black bold for zero or small dips
    return {"value": f"{sign}{value}%", "class": css_class}


def get_day_name(date_str):
    """Get short day name from date string."""
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%a")


def render_table_with_insight(data, insights):
    """Render module table WITH Key Insight column."""
    html = '''<div class="overflow-x-auto mb-6">
        <table class="w-full border-collapse text-sm">
            <thead>
                <tr class="bg-[#041e42] text-white">
                    <th class="px-3 py-3 text-left font-semibold">Module</th>
                    <th class="px-3 py-3 text-center font-semibold">CTR %</th>
                    <th class="px-3 py-3 text-center font-semibold">CTR WoW %</th>
                    <th class="px-3 py-3 text-center font-semibold">Clicks %</th>
                    <th class="px-3 py-3 text-center font-semibold">Clicks WoW %</th>
                    <th class="px-3 py-3 text-center font-semibold">ATC %</th>
                    <th class="px-3 py-3 text-center font-semibold">ATC WoW %</th>
                    <th class="px-3 py-3 text-left font-semibold">Key Insight</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">'''

    for i, row in enumerate(data):
        bg         = "bg-gray-50" if i % 2 == 1 else ""
        # BTF Navigation: CTR & Clicks WoW black, ATC WoW shows red/green normally
        if row['module'] == 'BTF Navigation':
            ctr_wow    = format_wow(row['ctr_wow_pct'])
            clicks_wow = format_wow(row['clicks_wow_pct'])
            atc_wow    = format_wow(row['atc_wow_pct'])
        elif row['module'] == 'Walmart+ Banner':
            ctr_wow    = format_wow(row['ctr_wow_pct'])
            clicks_wow = format_wow(row['clicks_wow_pct'])
            atc_wow    = {"value": "\u2014", "class": ""}
        elif row['module'] == 'Utility':
            ctr_wow    = format_wow(row['ctr_wow_pct'])
            clicks_wow = format_wow(row['clicks_wow_pct'])
            atc_wow    = {"value": "\u2014", "class": ""}
        else:
            ctr_wow    = format_wow(row['ctr_wow_pct'])
            clicks_wow = format_wow(row['clicks_wow_pct'])
            atc_wow    = format_wow(row['atc_wow_pct'])
        if row['module'] in ('Walmart+ Banner', 'Utility'):
            atc_pct = "\u2014"
        else:
            atc_pct = f"{row['atc_pct']}%" if row['atc_pct'] is not None else "\u2014"
        insight    = insights.get(row['module'], '')

        html += f'''<tr class="hover:bg-gray-50 {bg}">
            <td class="px-3 py-3 text-left font-medium text-gray-800">{row['module']}</td>
            <td class="px-3 py-3 text-center">{row['ctr_pct']}%</td>
            <td class="px-3 py-3 text-center {ctr_wow['class']}">{ctr_wow['value']}</td>
            <td class="px-3 py-3 text-center">{row['clicks_pct']}%</td>
            <td class="px-3 py-3 text-center {clicks_wow['class']}">{clicks_wow['value']}</td>
            <td class="px-3 py-3 text-center">{atc_pct}</td>
            <td class="px-3 py-3 text-center {atc_wow['class']}">{atc_wow['value']}</td>
            <td class="px-3 py-3 text-left text-gray-600 text-xs">{insight}</td>
        </tr>'''

    html += '''</tbody></table></div>'''
    return html


def render_table_no_insight(data):
    """Render module table WITHOUT Key Insight column."""
    html = '''<div class="overflow-x-auto mb-6">
        <table class="w-full border-collapse text-sm">
            <thead>
                <tr class="bg-[#041e42] text-white">
                    <th class="px-3 py-3 text-left font-semibold">Module</th>
                    <th class="px-3 py-3 text-center font-semibold">CTR %</th>
                    <th class="px-3 py-3 text-center font-semibold">CTR WoW %</th>
                    <th class="px-3 py-3 text-center font-semibold">Clicks %</th>
                    <th class="px-3 py-3 text-center font-semibold">Clicks WoW %</th>
                    <th class="px-3 py-3 text-center font-semibold">ATC %</th>
                    <th class="px-3 py-3 text-center font-semibold">ATC WoW %</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">'''

    for i, row in enumerate(data):
        bg         = "bg-gray-50" if i % 2 == 1 else ""
        # BTF Navigation: CTR & Clicks WoW black, ATC WoW shows red/green normally
        if row['module'] == 'BTF Navigation':
            ctr_wow    = format_wow(row['ctr_wow_pct'])
            clicks_wow = format_wow(row['clicks_wow_pct'])
            atc_wow    = format_wow(row['atc_wow_pct'])
        elif row['module'] == 'Walmart+ Banner':
            ctr_wow    = format_wow(row['ctr_wow_pct'])
            clicks_wow = format_wow(row['clicks_wow_pct'])
            atc_wow    = {"value": "\u2014", "class": ""}
        elif row['module'] == 'Utility':
            ctr_wow    = format_wow(row['ctr_wow_pct'])
            clicks_wow = format_wow(row['clicks_wow_pct'])
            atc_wow    = {"value": "\u2014", "class": ""}
        else:
            ctr_wow    = format_wow(row['ctr_wow_pct'])
            clicks_wow = format_wow(row['clicks_wow_pct'])
            atc_wow    = format_wow(row['atc_wow_pct'])
        if row['module'] in ('Walmart+ Banner', 'Utility'):
            atc_pct = "\u2014"
        else:
            atc_pct = f"{row['atc_pct']}%" if row['atc_pct'] is not None else "\u2014"

        html += f'''<tr class="hover:bg-gray-50 {bg}">
            <td class="px-3 py-3 text-left font-medium text-gray-800">{row['module']}</td>
            <td class="px-3 py-3 text-center">{row['ctr_pct']}%</td>
            <td class="px-3 py-3 text-center {ctr_wow['class']}">{ctr_wow['value']}</td>
            <td class="px-3 py-3 text-center">{row['clicks_pct']}%</td>
            <td class="px-3 py-3 text-center {clicks_wow['class']}">{clicks_wow['value']}</td>
            <td class="px-3 py-3 text-center">{atc_pct}</td>
            <td class="px-3 py-3 text-center {atc_wow['class']}">{atc_wow['value']}</td>
        </tr>'''

    html += '''</tbody></table></div>'''
    return html


@app.get("/", response_class=HTMLResponse)
@app.get("/homepage-module-performance-wbr", response_class=HTMLResponse)
async def home(selected_date: str = Query(default="2026-02-24")):
    # Calculate Walmart fiscal week dates
    current_start, current_end, prev_start, prev_end = get_walmart_fiscal_week_dates(selected_date)

    # Pull data from hp_summary_asset for all three views
    total_data   = get_wbr_data(current_start, current_end, prev_start, prev_end)
    ios_data     = get_wbr_data(current_start, current_end, prev_start, prev_end, "App: iOS")
    android_data = get_wbr_data(current_start, current_end, prev_start, prev_end, "App: Android")

    # Dynamic insights for the "Total" table
    dynamic_insights = get_dynamic_insights(current_start, current_end)

    # Day labels
    curr_start_day = get_day_name(current_start)
    curr_end_day   = get_day_name(current_end)
    prev_start_day = get_day_name(prev_start)
    prev_end_day   = get_day_name(prev_end)

    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weekly Business Review</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            .green   {{ color: #2a8703; font-weight: 600; }}
            .red     {{ color: #ea1100; font-weight: 600; }}
            .neutral {{ color: #1a1a1a; font-weight: 600; }}
            th     {{ white-space: nowrap; }}
        </style>
    </head>
    <body class="bg-gray-50 p-6">
        <div class="max-w-7xl mx-auto">
            <div class="bg-white rounded-lg shadow-lg p-6">

                <!-- Date Filter -->
                <div class="bg-gray-50 rounded-lg p-4 mb-6">
                    <form method="get" class="flex items-end gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">
                                Select Date (Walmart Fiscal Week)
                            </label>
                            <input type="date" name="selected_date" value="{selected_date}"
                                   class="border rounded-lg px-3 py-2 bg-white">
                        </div>
                        <button type="submit"
                                class="bg-[#041e42] text-white px-4 py-2 rounded-lg hover:bg-[#0a3161]">
                            Generate Report
                        </button>
                        <div class="text-sm text-gray-500 ml-4">
                            <p>Walmart week starts Saturday. Shows Sat \u2192 selected date vs same days prior week.</p>
                        </div>
                    </form>
                </div>

                <!-- All Modules Table -->
                <h1 class="text-xl font-bold text-gray-800 mb-4">
                    Weekly Business Review \u2014 All Modules
                </h1>

                <div class="flex gap-6 mb-4">
                    <div class="bg-[#e8eef5] border border-[#041e42] px-4 py-2 rounded-lg">
                        <span class="text-sm text-gray-500">Current Week</span>
                        <p class="font-semibold text-[#041e42]">
                            {current_start} ({curr_start_day}) \u2192 {current_end} ({curr_end_day})
                        </p>
                    </div>
                    <div class="bg-gray-100 border border-gray-300 px-4 py-2 rounded-lg">
                        <span class="text-sm text-gray-500">Previous Week</span>
                        <p class="font-semibold text-gray-600">
                            {prev_start} ({prev_start_day}) \u2192 {prev_end} ({prev_end_day})
                        </p>
                    </div>
                </div>
                <p class="text-gray-500 text-xs mb-4">
                    \u26a0\ufe0f Source: <code>hp_summary_asset</code> &nbsp;|&nbsp;
                    Filter: <strong>English</strong> language &nbsp;|&nbsp;
                    <strong>Content Type = Merch</strong> (WMC excluded) &nbsp;|&nbsp;
                    ATC WoW = rate-based (ATCs per impression)
                </p>

                {render_table_no_insight(total_data)}

                <div class="text-sm text-gray-500 mb-8">
                    <span class="green">Green</span> = WoW% &gt; 0 (improvement) |
                    <span class="red">Red</span> = WoW% &lt; 0 (decline)
                </div>

                <!-- iOS Table -->
                <h2 class="text-lg font-bold text-gray-800 mb-3 mt-8 pt-6 border-t">
                    App: iOS
                </h2>
                {render_table_no_insight(ios_data) if ios_data
                    else '<p class="text-gray-500">No data available for iOS</p>'}

                <!-- Android Table -->
                <h2 class="text-lg font-bold text-gray-800 mb-3 mt-8">
                    App: Android
                </h2>
                {render_table_no_insight(android_data) if android_data
                    else '<p class="text-gray-500">No data available for Android</p>'}

            </div>
        </div>
    </body>
    </html>
    '''

    return HTMLResponse(content=html)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
