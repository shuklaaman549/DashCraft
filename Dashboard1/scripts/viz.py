import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import warnings
import os
warnings.filterwarnings("ignore", category=DeprecationWarning)


def load_data():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")
    
    # Check if data directory exists, if not, look in current directory
    if not os.path.exists(data_dir):
        data_dir = os.path.join(script_dir, "data")
        if not os.path.exists(data_dir):
            # If still not found, use current working directory
            data_dir = "data"
    
    try:
        reqs = pd.read_csv(os.path.join(data_dir, 'requests_log.csv'), parse_dates=['created_at'])
        status = pd.read_csv(os.path.join(data_dir, 'requests_status.csv'))
        origin = pd.read_csv(os.path.join(data_dir, 'requests_origin.csv'))
        dept = pd.read_csv(os.path.join(data_dir, 'requests_department.csv'))
        months = pd.read_csv(os.path.join(data_dir, 'requests_monthly.csv'))
    except FileNotFoundError as e:
        print(f"Error: Could not find required CSV files.")
        print(f"Looking in directory: {os.path.abspath(data_dir)}")
        print("Required files: requests_log.csv, requests_status.csv, requests_origin.csv, requests_department.csv, requests_monthly.csv")
        raise e
    
    return reqs, status, origin, dept, months


def create_dashboard(reqs, status, origin, dept, months, output=None):
    if output is None:
        # Create outputs directory if it doesn't exist
        script_dir = os.path.dirname(os.path.abspath(__file__))
        outputs_dir = os.path.join(script_dir, "..", "outputs")
        if not os.path.exists(outputs_dir):
            outputs_dir = os.path.join(script_dir, "outputs")
            if not os.path.exists(outputs_dir):
                os.makedirs(outputs_dir)
        output = os.path.join(outputs_dir, "dashboard.html")
    
    BG_MAIN = "#1C1C2E"
    CARD = "#24243A"
    PRIMARY = "#7F74F2"
    ACCENT = "#4BC6B9"
    SECONDARY = "#F4B860"
    TERTIARY = "#FF6B6B"
    GRAY_LINE = "#5E6480"
    FONT_LABEL = "#A9B0C5"
    FONT_CARD = "#FFFFFF"

    main_kpi_html = f"""
    <div class="kpi-content">
        <div class="kpi-label">TOTAL REQUESTS</div>
        <div class="kpi-value">{len(reqs):,}</div>
    </div>
    """

    status_fig = go.Figure(go.Bar(
        x=status['status'],
        y=status['count'],
        marker=dict(color=[ACCENT, SECONDARY, PRIMARY, TERTIARY]),
        width=0.5
    ))
    status_fig.update_layout(
        title="<span style='font-weight:750; color:%s;'>Requests by Status</span>" % FONT_CARD,
        template="plotly_dark",
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        margin=dict(l=18, r=10, t=45, b=25),
        yaxis=dict(title="Requests", gridcolor=GRAY_LINE, color=FONT_LABEL),
        xaxis=dict(title="", color=FONT_LABEL, showgrid=False),
        height=180
    )

    pie_colors = [PRIMARY, ACCENT, SECONDARY, TERTIARY]
    origin_fig = go.Figure(go.Pie(
        labels=origin['origin'],
        values=origin['count'],
        hole=0.5,
        marker=dict(colors=pie_colors, line=dict(width=2, color=CARD)),
        textinfo="none"
    ))
    
    # Default legend configuration (will be adjusted by JavaScript)
    origin_fig.update_layout(
        title="<span style='font-weight:750; color:%s;'>Request Origins</span>" % FONT_CARD,
        template="plotly_dark",
        paper_bgcolor=CARD,
        margin=dict(l=10, r=10, t=45, b=10), 
        legend=dict(
            font=dict(size=11, color=FONT_LABEL), 
            orientation="v", 
            yanchor="middle", 
            y=0.5, 
            xanchor="left", 
            x=1.02,
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)"
        ),
        height=155,
        showlegend=True
    )

    dept_fig = px.bar(
        dept.sort_values("count"),
        y="department",
        x="count",
        orientation="h",
        color_discrete_sequence=["#B39DDB"],
        text="count"
    )
    dept_fig.update_traces(
        textposition="outside",
        marker_line_color=PRIMARY,
        marker_line_width=1.1,
        textfont_size=13,
        textfont_color=FONT_CARD
    )
    dept_fig.update_layout(
        title="<span style='font-weight:750; color=%s;'>Top 10 Departments</span>" % FONT_CARD,
        template="plotly_dark",
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        yaxis=dict(title="", autorange="reversed", tickfont=dict(size=13, color=FONT_LABEL)),
        xaxis=dict(title="Requests", color=FONT_LABEL, gridcolor=GRAY_LINE),
        margin=dict(l=30, r=14, t=45, b=12),
        height=260
    )

    months = months.sort_values("month")
    ts_fig = go.Figure(go.Scatter(
        x=months["month"], y=months["count"], mode="lines+markers",
        line=dict(color=ACCENT, width=3),
        marker=dict(size=7, color=PRIMARY, line=dict(width=2, color=CARD))
    ))
    ts_fig.update_layout(
        title="<span style='font-weight:750; color:%s;'>Monthly Request Trends</span>" % FONT_CARD,
        template="plotly_dark",
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        margin=dict(l=20, r=10, t=42, b=10),
        xaxis=dict(title="Month", color=FONT_LABEL, showgrid=False),
        yaxis=dict(title="Requests", gridcolor=GRAY_LINE, color=FONT_LABEL),
        height=180
    )

    # MAP without watermark
    subset = reqs.sample(n=min(len(reqs), 2000), random_state=3)
    map_fig = px.scatter_mapbox(
        subset,
        lat="latitude",
        lon="longitude",
        hover_name="category",
        color_discrete_sequence=[ACCENT],
        zoom=12.5,
        opacity=0.6,
        height=195,
        width=390
    )
    map_fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={"lat": subset["latitude"].mean(), "lon": subset["longitude"].mean()},
        paper_bgcolor=CARD,
        margin=dict(l=2, r=2, t=50, b=2),
        title="<span style='font-weight:750; color=%s;'>Request Locations</span>" % FONT_CARD,
        annotations=[]  # Watermark removed
    )
    map_fig.update_traces(marker=dict(size=6, opacity=0.5))

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>311 Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            html, body {{
                background: {BG_MAIN};
                font-family: 'Inter', sans-serif;
                margin: 0;
                padding: 0;
                overflow-x: hidden;
                width: 100%;
            }}
            
            .dash-container {{
                width: 100%;
                max-width: 1380px;
                margin: 0 auto;
                padding: 12px 15px 40px 15px;
            }}
            
            .dash-title {{
                font-weight: 800;
                font-size: 1.2rem;
                color: #ffffff;
                margin-left: 6px;
                margin-bottom: 0.2rem;
            }}
            
            .dash-subtitle {{
                font-weight: 400;
                font-size: 0.83rem;
                margin-bottom: 18px;
                margin-left: 8px;
                color: {FONT_LABEL};
                opacity: 0.93;
            }}
            
            /* Desktop Grid Layout */
            .card-grid {{
                display: grid;
                grid-template-columns: 0.8fr 0.9fr 0.9fr;
                grid-template-rows: auto auto auto;
                gap: 15px;
                width: 100%;
            }}
            
            .card {{
                box-shadow: 0 8px 26px rgba(0,0,0,0.25);
                border-radius: 16px;
                background: #24243A;
                border: 1px solid #39395A;
                padding: 12px 16px 6px 16px;
                transition: transform 0.2s ease, background-color 0.3s ease;
                overflow: hidden;
                min-height: 180px;
            }}
            
            .card:hover {{
                background-color: #24243A;
                transform: translateY(-4px);
                cursor: pointer;
            }}
            
            .kpi-card {{
                grid-row: 1;
                grid-column: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 0;
                min-height: 160px;
            }}
            
            .status-card {{
                grid-row: 1;
                grid-column: 2;
            }}
            
            .origin-card {{
                grid-row: 1;
                grid-column: 3;
            }}
            
            .map-card {{
                grid-row: 2;
                grid-column: 1;
            }}
            
            .dept-card {{
                grid-row: 2;
                grid-column: 2/4;
            }}
            
            .trend-card {{
                grid-row: 3;
                grid-column: 1/4;
            }}
            
            .kpi-content {{
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100%;
                color: {FONT_CARD};
                text-align: center;
            }}
            
            .kpi-label {{
                font-size: 1.1em;
                font-weight: 600;
                color: {FONT_LABEL};
                letter-spacing: 0.5px;
                margin-bottom: 6px;
            }}
            
            .kpi-value {{
                font-size: 3.2em;
                font-weight: 700;
                color: {PRIMARY};
            }}
            
            /* Make Plotly charts responsive */
            .plotly-graph-div {{
                width: 100% !important;
                height: auto !important;
            }}
            
            /* Large Desktop */
            @media screen and (min-width: 1400px) {{
                .dash-container {{
                    max-width: 1500px;
                    padding: 15px 20px 45px 20px;
                }}
                .card-grid {{
                    gap: 18px;
                }}
            }}
            
            /* Medium Desktop */
            @media screen and (min-width: 1200px) and (max-width: 1399px) {{
                .dash-container {{
                    max-width: 1200px;
                    padding: 12px 15px 40px 15px;
                }}
                .card-grid {{
                    gap: 15px;
                }}
            }}
            
            /* Small Desktop / Large Tablet */
            @media screen and (min-width: 1000px) and (max-width: 1199px) {{
                .dash-container {{
                    max-width: 95%;
                    padding: 10px 12px 35px 12px;
                }}
                .card-grid {{
                    gap: 12px;
                }}
                .card {{
                    padding: 10px 14px 5px 14px;
                }}
            }}
            
            /* Tablet Portrait */
            @media screen and (min-width: 768px) and (max-width: 999px) {{
                .dash-container {{
                    padding: 10px 12px 30px 12px;
                }}
                
                .card-grid {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    grid-template-rows: auto auto auto auto;
                    gap: 12px;
                }}
                
                .kpi-card {{
                    grid-row: 1;
                    grid-column: 1;
                }}
                
                .status-card {{
                    grid-row: 1;
                    grid-column: 2;
                }}
                
                .origin-card {{
                    grid-row: 2;
                    grid-column: 1;
                }}
                
                .map-card {{
                    grid-row: 2;
                    grid-column: 2;
                }}
                
                .dept-card {{
                    grid-row: 3;
                    grid-column: 1/3;
                }}
                
                .trend-card {{
                    grid-row: 4;
                    grid-column: 1/3;
                }}
                
                .card {{
                    min-height: 160px;
                    padding: 10px 12px 5px 12px;
                }}
            }}
            
            /* Mobile Landscape / Small Tablet */
            @media screen and (min-width: 600px) and (max-width: 767px) {{
                .dash-container {{
                    padding: 8px 10px 25px 10px;
                }}
                
                .dash-title {{
                    font-size: 1.1rem;
                    margin-left: 4px;
                }}
                
                .dash-subtitle {{
                    font-size: 0.8rem;
                    margin-left: 6px;
                    margin-bottom: 15px;
                }}
                
                .card-grid {{
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }}
                
                .card {{
                    width: 100%;
                    min-height: 140px;
                    padding: 10px 12px 5px 12px;
                    border-radius: 12px;
                }}
                
                .kpi-card {{
                    min-height: 120px;
                }}
                
                .kpi-label {{
                    font-size: 1em !important;
                }}
                
                .kpi-value {{
                    font-size: 2.8em !important;
                }}
            }}
            
            /* Mobile Portrait */
            @media screen and (max-width: 599px) {{
                .dash-container {{
                    padding: 6px 8px 20px 8px;
                }}
                
                .dash-title {{
                    font-size: 1rem;
                    margin-left: 2px;
                }}
                
                .dash-subtitle {{
                    font-size: 0.75rem;
                    margin-left: 4px;
                    margin-bottom: 12px;
                }}
                
                .card-grid {{
                    display: flex;
                    flex-direction: column;
                    gap: 8px;
                }}
                
                .card {{
                    width: 100%;
                    min-height: 120px;
                    padding: 8px 10px 4px 10px;
                    border-radius: 10px;
                }}
                
                .kpi-card {{
                    min-height: 100px;
                }}
                
                .kpi-label {{
                    font-size: 0.9em !important;
                    margin-bottom: 4px !important;
                }}
                
                .kpi-value {{
                    font-size: 2.4em !important;
                }}
            }}
            
            /* Very Small Mobile */
            @media screen and (max-width: 360px) {{
                .dash-container {{
                    padding: 4px 6px 15px 6px;
                }}
                
                .dash-title {{
                    font-size: 0.95rem;
                    margin-left: 1px;
                }}
                
                .dash-subtitle {{
                    font-size: 0.7rem;
                    margin-left: 2px;
                    margin-bottom: 10px;
                }}
                
                .card-grid {{
                    gap: 6px;
                }}
                
                .card {{
                    padding: 6px 8px 3px 8px;
                    border-radius: 8px;
                    min-height: 100px;
                }}
                
                .kpi-card {{
                    min-height: 90px;
                }}
                
                .kpi-label {{
                    font-size: 0.8em !important;
                    letter-spacing: 0.3px !important;
                }}
                
                .kpi-value {{
                    font-size: 2em !important;
                }}
            }}
        </style>
        <script>
            // Make Plotly charts responsive
            function resizePlotlyCharts() {{
                var plots = document.querySelectorAll('.plotly-graph-div');
                for (var i = 0; i < plots.length; i++) {{
                    Plotly.Plots.resize(plots[i]);
                }}
            }}
            
            // Adjust pie chart legend based on screen size and card width
            function adjustPieChartLegend() {{
                var screenWidth = window.innerWidth;
                var originCard = document.querySelector('.origin-card .plotly-graph-div');
                
                if (originCard) {{
                    var cardWidth = originCard.parentElement.offsetWidth;
                    var update = {{}};
                    
                    if (screenWidth >= 1200) {{
                        // Large desktop - normal legend
                        update = {{
                            showlegend: true,
                            legend: {{
                                font: {{size: 11, color: '{FONT_LABEL}'}}, 
                                orientation: 'v', 
                                yanchor: 'middle', 
                                y: 0.5, 
                                xanchor: 'left', 
                                x: 1.02,
                                bgcolor: 'rgba(0,0,0,0)',
                                bordercolor: 'rgba(0,0,0,0)'
                            }}
                        }};
                    }} else if (screenWidth >= 1000) {{
                        // Small desktop - smaller legend
                        update = {{
                            showlegend: true,
                            legend: {{
                                font: {{size: 9, color: '{FONT_LABEL}'}}, 
                                orientation: 'v', 
                                yanchor: 'middle', 
                                y: 0.5, 
                                xanchor: 'left', 
                                x: 1.01,
                                bgcolor: 'rgba(0,0,0,0)',
                                bordercolor: 'rgba(0,0,0,0)'
                            }}
                        }};
                    }} else if (screenWidth >= 768) {{
                        // Tablet - legend below chart
                        update = {{
                            showlegend: true,
                            legend: {{
                                font: {{size: 10, color: '{FONT_LABEL}'}}, 
                                orientation: 'h', 
                                yanchor: 'top', 
                                y: -0.1, 
                                xanchor: 'center', 
                                x: 0.5,
                                bgcolor: 'rgba(0,0,0,0)',
                                bordercolor: 'rgba(0,0,0,0)'
                            }}
                        }};
                    }} else if (screenWidth >= 600) {{
                        // Mobile landscape - compact legend below
                        update = {{
                            showlegend: true,
                            legend: {{
                                font: {{size: 9, color: '{FONT_LABEL}'}}, 
                                orientation: 'h', 
                                yanchor: 'top', 
                                y: -0.15, 
                                xanchor: 'center', 
                                x: 0.5,
                                bgcolor: 'rgba(0,0,0,0)',
                                bordercolor: 'rgba(0,0,0,0)'
                            }}
                        }};
                    }} else {{
                        // Mobile portrait - very small legend below
                        update = {{
                            showlegend: true,
                            legend: {{
                                font: {{size: 8, color: '{FONT_LABEL}'}}, 
                                orientation: 'h', 
                                yanchor: 'top', 
                                y: -0.2, 
                                xanchor: 'center', 
                                x: 0.5,
                                bgcolor: 'rgba(0,0,0,0)',
                                bordercolor: 'rgba(0,0,0,0)'
                            }}
                        }};
                    }}
                    
                    Plotly.relayout(originCard, update);
                }}
            }}
            
            window.addEventListener('resize', function() {{
                resizePlotlyCharts();
                setTimeout(adjustPieChartLegend, 100);
            }});
            
            window.addEventListener('load', function() {{
                setTimeout(function() {{
                    resizePlotlyCharts();
                    adjustPieChartLegend();
                }}, 300);
            }});
            
            window.addEventListener('orientationchange', function() {{
                setTimeout(function() {{
                    resizePlotlyCharts();
                    adjustPieChartLegend();
                }}, 500);
            }});
        </script>
    </head>
    <body>
        <div class="dash-container">
            <div class="dash-title">311 Requests Dashboard</div>
            <div class="dash-subtitle">A monthly breakdown of 311 activity across the city.</div>
            <div class="card-grid">
                <div class="card kpi-card">{main_kpi_html}</div>
                <div class="card status-card">{status_fig.to_html(full_html=False, include_plotlyjs='cdn')}</div>
                <div class="card origin-card">{origin_fig.to_html(full_html=False, include_plotlyjs=False)}</div>
                <div class="card map-card">{map_fig.to_html(full_html=False, include_plotlyjs=False)}</div>
                <div class="card dept-card">{dept_fig.to_html(full_html=False, include_plotlyjs=False)}</div>
                <div class="card trend-card">{ts_fig.to_html(full_html=False, include_plotlyjs=False)}</div>
            </div>
        </div>
    </body>
    </html>
    """

    with open(output, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Dashboard created successfully!")


def main():
    reqs, status, origin, dept, months = load_data()
    create_dashboard(reqs, status, origin, dept, months)


if __name__ == "__main__":
    main()
