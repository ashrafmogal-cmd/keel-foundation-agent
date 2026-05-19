from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from google.cloud import bigquery
from datetime import datetime, timedelta
import json

app = FastAPI(title="HP Message Performance")
client = bigquery.Client()


def get_walmart_fiscal_week_dates(selected_date: str):
    """Calculate Walmart fiscal week dates (Sat to selected_date)."""
    dt = datetime.strptime(selected_date, "%Y-%m-%d")
    weekday = dt.weekday()
    if weekday == 5:
        days_since_saturday = 0
    elif weekday == 6:
        days_since_saturday = 1
    else:
        days_since_saturday = weekday + 2
    
    current_saturday = dt - timedelta(days=days_since_saturday)
    current_start = current_saturday.strftime("%Y-%m-%d")
    current_end = dt.strftime("%Y-%m-%d")
    prev_start = (current_saturday - timedelta(days=7)).strftime("%Y-%m-%d")
    prev_end = (dt - timedelta(days=7)).strftime("%Y-%m-%d")
    
    return current_start, current_end, prev_start, prev_end


def get_hpov_data(start_date: str, end_date: str):
    """Get HPOV data including Sponsored Ads."""
    query = f"""
    WITH sponsored AS (
      SELECT 
        'Sponsored Ads' as m0_nm,
        'Sponsored Ads' as message_name,
        SUM(viewed_impressions) as impressions,
        SUM(overall_click_count) as clicks,
        SAFE_DIVIDE(SUM(overall_click_count), SUM(viewed_impressions)) * 100 as ctr
      FROM `wmt-site-content-strategy.scs_production.HPsummary`
      WHERE session_start_dt BETWEEN '{start_date}' AND '{end_date}'
        AND LOWER(Content_Zone) = 'contentzone3'
        AND hp_module_name IN ('AutoScroll Card 1', 'AutoScroll Card 2', 'AutoScroll Card 3', 'AutoScroll Card 4', 'AutoScroll Card 5')
        AND Content_Type = 'WMC'
    ),
    merch_data AS (
      SELECT 
        m0_nm,
        message_name,
        SUM(viewed_impressions) AS impressions,
        SUM(overall_click_count) AS clicks,
        SAFE_DIVIDE(SUM(overall_click_count), SUM(viewed_impressions)) * 100 AS ctr
      FROM `wmt-site-content-strategy.scs_production.HPsummary`
      WHERE session_start_dt BETWEEN '{start_date}' AND '{end_date}'
        AND LOWER(Content_Zone) = 'contentzone3'
        AND hp_module_name IN ('AutoScroll Card 1', 'AutoScroll Card 2', 'AutoScroll Card 3', 'AutoScroll Card 4', 'AutoScroll Card 5')
        AND Content_Type = 'Merch'
        AND message_name NOT LIKE '%Great Value%'
        AND message_name NOT LIKE '%Resold%'
        AND message_name IS NOT NULL
        AND m0_nm IS NOT NULL
      GROUP BY m0_nm, message_name
      HAVING SUM(viewed_impressions) > 500000
    ),
    all_data AS (
      SELECT * FROM sponsored
      UNION ALL
      SELECT * FROM merch_data
    ),
    benchmark AS (
      SELECT SAFE_DIVIDE(SUM(overall_click_count), SUM(viewed_impressions)) * 100 AS benchmark_ctr
      FROM `wmt-site-content-strategy.scs_production.HPsummary`
      WHERE session_start_dt BETWEEN '{start_date}' AND '{end_date}'
        AND LOWER(Content_Zone) = 'contentzone3'
        AND hp_module_name IN ('AutoScroll Card 1', 'AutoScroll Card 2', 'AutoScroll Card 3', 'AutoScroll Card 4', 'AutoScroll Card 5')
        AND Content_Type = 'Merch'
    ),
    m0_totals AS (
      SELECT m0_nm, SUM(impressions) AS m0_total FROM all_data GROUP BY m0_nm
    ),
    grand_total AS (
      SELECT SUM(m0_total) AS total FROM m0_totals
    )
    SELECT 
      CASE 
        WHEN d.m0_nm IN ('Get It Fast', 'Walmart Plus') THEN 'Services'
        ELSE d.m0_nm 
      END as m0_nm,
      d.message_name,
      ROUND(d.impressions / 1000000, 1) AS impressions_m,
      ROUND(d.ctr, 2) AS ctr,
      ROUND(b.benchmark_ctr, 2) AS benchmark_ctr,
      ROUND(m.m0_total / g.total * 100, 0) AS sov_pct
    FROM all_data d
    CROSS JOIN benchmark b
    LEFT JOIN m0_totals m ON d.m0_nm = m.m0_nm
    CROSS JOIN grand_total g
    ORDER BY 
      CASE WHEN d.m0_nm = 'Sponsored Ads' THEN 0 ELSE 1 END,
      m.m0_total DESC, 
      d.impressions DESC
    """
    
    try:
        result = client.query(query).result()
        return [dict(row) for row in result]
    except Exception as e:
        print(f"HPOV Query Error: {e}")
        return []


def get_sig_data(start_date: str, end_date: str):
    """Get ATF Carousels (contentZone4/5/6, non-SIG modules) data."""
    query = f"""
    WITH sig_data AS (
      SELECT 
        COALESCE(NULLIF(hp_module_name, ''), 'Unknown') as m0_nm,
        COALESCE(NULLIF(message_name, ''), Carousel_Name, hp_module_name, 'Unknown') as message_name,
        SUM(viewed_impressions) AS impressions,
        SUM(overall_click_count) AS clicks,
        SAFE_DIVIDE(SUM(overall_click_count), SUM(viewed_impressions)) * 100 AS ctr
      FROM `wmt-site-content-strategy.scs_production.HPsummary`
      WHERE session_start_dt BETWEEN '{start_date}' AND '{end_date}'
        AND LOWER(Content_Zone) IN ('contentzone4', 'contentzone5', 'contentzone6')
        AND moduleType != 'PrismScrollableItemGrid'
        AND Content_Type = 'Merch'
        AND language_split = 'English'
      GROUP BY m0_nm, message_name
      HAVING SUM(viewed_impressions) > 500000
    ),
    benchmark AS (
      SELECT SAFE_DIVIDE(SUM(overall_click_count), SUM(viewed_impressions)) * 100 AS benchmark_ctr
      FROM `wmt-site-content-strategy.scs_production.HPsummary`
      WHERE session_start_dt BETWEEN '{start_date}' AND '{end_date}'
        AND LOWER(Content_Zone) IN ('contentzone4', 'contentzone5', 'contentzone6')
        AND moduleType != 'PrismScrollableItemGrid'
        AND Content_Type = 'Merch'
        AND language_split = 'English'
    ),
    m0_totals AS (
      SELECT m0_nm, SUM(impressions) AS m0_total FROM sig_data GROUP BY m0_nm
    ),
    grand_total AS (
      SELECT SUM(m0_total) AS total FROM m0_totals
    )
    SELECT 
      CASE WHEN d.m0_nm = 'Jump right back in' THEN 'CYS' ELSE d.m0_nm END as m0_nm,
      CASE WHEN d.message_name = 'Jump right back in' THEN 'CYS' ELSE d.message_name END as message_name,
      ROUND(d.impressions / 1000000, 1) AS impressions_m,
      ROUND(d.ctr, 2) AS ctr,
      ROUND(b.benchmark_ctr, 2) AS benchmark_ctr,
      ROUND(m.m0_total / g.total * 100, 0) AS sov_pct
    FROM sig_data d
    CROSS JOIN benchmark b
    LEFT JOIN m0_totals m ON d.m0_nm = m.m0_nm
    CROSS JOIN grand_total g
    ORDER BY m.m0_total DESC, d.impressions DESC
    """
    
    try:
        result = client.query(query).result()
        return [dict(row) for row in result]
    except Exception as e:
        print(f"SIG Query Error: {e}")
        return []


def group_by_m0(data):
    """Group messages by m0_nm for chart rendering."""
    campaigns = {}
    colors = [
        '#6b7280', '#3b82f6', '#ef4444', '#22c55e', '#8b5cf6', '#f59e0b', 
        '#ec4899', '#14b8a6', '#64748b', '#06b6d4', '#6366f1', '#a855f7', 
        '#f97316', '#84cc16', '#0ea5e9', '#d946ef'
    ]
    color_idx = 0
    
    for row in data:
        m0 = row['m0_nm']
        if m0 not in campaigns:
            campaigns[m0] = {
                'm0_nm': m0,
                'sov': row['sov_pct'],
                'color': colors[color_idx % len(colors)],
                'messages': []
            }
            color_idx += 1
        campaigns[m0]['messages'].append({
            'name': row['message_name'],
            'impressions': float(row['impressions_m']),
            'ctr': float(row['ctr'])
        })
    
    return list(campaigns.values())


def render_chart(chart_id: str, title: str, campaigns: list, benchmark: float):
    """Render a single chart HTML."""
    campaigns_json = json.dumps(campaigns)
    
    return f'''
    <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h2 class="text-xl font-bold text-center text-gray-800 mb-4">{title}</h2>
        <div style="height: 420px;">
            <canvas id="{chart_id}"></canvas>
        </div>
        <div id="{chart_id}Band" class="flex mt-0" style="margin-left: 50px; margin-right: 50px;"></div>
    </div>
    
    <script>
    (function() {{
        const campaigns = {campaigns_json};
        const benchmarkCTR = {benchmark};
        
        const labels = [];
        const impressionsData = [];
        const ctrData = [];
        const barColors = [];
        const campaignMsgCounts = [];
        
        campaigns.forEach(campaign => {{
            campaignMsgCounts.push({{
                m0_nm: campaign.m0_nm,
                count: campaign.messages.length,
                sov: campaign.sov,
                color: campaign.color
            }});
            campaign.messages.forEach(msg => {{
                labels.push(msg.name);
                impressionsData.push(msg.impressions);
                ctrData.push(msg.ctr);
                barColors.push(campaign.color);
            }});
        }});
        
        const ctx = document.getElementById('{chart_id}').getContext('2d');
        
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: labels,
                datasets: [
                    {{
                        label: 'Impressions (M)',
                        data: impressionsData,
                        backgroundColor: barColors,
                        borderRadius: 4,
                        order: 2,
                        yAxisID: 'y'
                    }},
                    {{
                        label: 'CTR %',
                        data: ctrData,
                        type: 'line',
                        borderColor: '#1f2937',
                        backgroundColor: '#1f2937',
                        pointRadius: 5,
                        pointBackgroundColor: '#ffffff',
                        pointBorderColor: '#1f2937',
                        pointBorderWidth: 2,
                        tension: 0,
                        order: 1,
                        yAxisID: 'y1'
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }},
                    datalabels: {{
                        display: true,
                        anchor: function(context) {{ return context.datasetIndex === 0 ? 'center' : 'end'; }},
                        align: function(context) {{ return context.datasetIndex === 0 ? 'center' : 'top'; }},
                        color: function(context) {{ return context.datasetIndex === 0 ? '#ffffff' : '#1f2937'; }},
                        font: {{ weight: 'bold', size: 9 }},
                        formatter: function(value, context) {{
                            if (context.datasetIndex === 0) return value + 'M';
                            else return value.toFixed(2) + '%';
                        }}
                    }},
                    annotation: {{
                        annotations: {{
                            benchmarkLine: {{
                                type: 'line',
                                yMin: benchmarkCTR,
                                yMax: benchmarkCTR,
                                yScaleID: 'y1',
                                borderColor: '#06b6d4',
                                borderWidth: 2,
                                borderDash: [6, 4],
                                label: {{
                                    display: true,
                                    content: benchmarkCTR.toFixed(2) + '%',
                                    position: 'end',
                                    backgroundColor: '#06b6d4',
                                    color: '#ffffff',
                                    font: {{ size: 10, weight: 'bold' }},
                                    padding: 3
                                }}
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{ grid: {{ display: false }}, ticks: {{ maxRotation: 45, minRotation: 45, font: {{ size: 8 }} }} }},
                    y: {{ type: 'linear', position: 'left', grid: {{ color: '#e5e7eb' }}, min: 0 }},
                    y1: {{ type: 'linear', position: 'right', grid: {{ display: false }}, min: 0 }}
                }}
            }},
            plugins: [ChartDataLabels]
        }});
        
        const m0Band = document.getElementById('{chart_id}Band');
        campaignMsgCounts.forEach(c => {{
            const div = document.createElement('div');
            div.style.cssText = 'display:flex;align-items:center;justify-content:center;color:white;font-weight:600;font-size:10px;text-align:center;padding:6px 2px;line-height:1.2;background-color:' + c.color + ';flex:' + c.count;
            div.innerHTML = c.m0_nm + '<br>' + c.sov + '% SOV';
            m0Band.appendChild(div);
        }});
    }})();
    </script>
    '''


@app.get("/", response_class=HTMLResponse)
async def home(selected_date: str = Query(default="2026-02-17")):
    current_start, current_end, prev_start, prev_end = get_walmart_fiscal_week_dates(selected_date)
    
    # Get data
    hpov_raw = get_hpov_data(current_start, current_end)
    sig_raw = get_sig_data(current_start, current_end)
    
    # Get benchmarks
    hpov_benchmark = hpov_raw[0]['benchmark_ctr'] if hpov_raw else 0.22
    sig_benchmark = sig_raw[0]['benchmark_ctr'] if sig_raw else 1.03
    
    # Group by m0_nm
    hpov_campaigns = group_by_m0(hpov_raw)
    sig_campaigns = group_by_m0(sig_raw)
    
    # Day names
    start_day = datetime.strptime(current_start, "%Y-%m-%d").strftime("%a")
    end_day = datetime.strptime(current_end, "%Y-%m-%d").strftime("%a")
    
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HP Message Performance</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation"></script>
    </head>
    <body class="bg-gray-100 p-6">
        <div class="max-w-7xl mx-auto">
            <!-- Header -->
            <div class="bg-white rounded-lg shadow-lg p-4 mb-6">
                <h1 class="text-2xl font-bold text-center text-gray-800 mb-4">HP Message Performance Dashboard</h1>
                
                <!-- Date Filter -->
                <form method="get" class="flex items-end justify-center gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Select Date (Walmart Fiscal Week)</label>
                        <input type="date" name="selected_date" value="{selected_date}" 
                               class="border rounded-lg px-3 py-2 bg-white">
                    </div>
                    <button type="submit" class="bg-[#041e42] text-white px-6 py-2 rounded-lg hover:bg-[#0a3161]">
                        Generate Report
                    </button>
                </form>
                
                <div class="flex justify-center gap-6 mt-4 text-sm">
                    <div class="bg-[#e8eef5] border border-[#041e42] px-4 py-2 rounded-lg">
                        <span class="text-gray-500">Date Range:</span>
                        <span class="font-semibold text-[#041e42]">{current_start} ({start_day}) \u2192 {current_end} ({end_day})</span>
                    </div>
                    <div class="bg-gray-100 px-4 py-2 rounded-lg">
                        <span class="text-gray-500">Filter:</span>
                        <span class="font-semibold">Content_Type = Merch | Impressions > 500K</span>
                    </div>
                </div>
            </div>
            
            <!-- HPOV Chart -->
            {render_chart('hpovChart', 'HPOV (AutoScroll Cards 1\u20135 | contentZone3)', hpov_campaigns, hpov_benchmark)}
            
            <!-- SIG Chart -->
            {render_chart('sigChart', 'ATF Carousels (contentZone4/5/6 | Non-SIG)', sig_campaigns, sig_benchmark)}
        </div>
    </body>
    </html>
    '''
    
    return HTMLResponse(content=html)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
