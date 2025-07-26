import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def load_data():
    reqs = pd.read_csv('../data/requests_log.csv', parse_dates=['created_at'])
    status = pd.read_csv('../data/requests_status.csv')
    origin = pd.read_csv('../data/requests_origin.csv')
    dept = pd.read_csv('../data/requests_department.csv')
    months = pd.read_csv('../data/requests_monthly.csv')
    return reqs, status, origin, dept, months

def create_dashboard(reqs, status, origin, dept, months, output="../outputs/dashboard.html"):
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
    <div style="display:flex;flex-direction:column;justify-content:center;align-items:center;height:140px;color:{FONT_CARD};">
        <div style="font-size:1.1em;font-weight:600;color:{FONT_LABEL};letter-spacing:0.5px;margin-bottom:6px;">TOTAL REQUESTS</div>
        <div style="font-size:3.2em;font-weight:700;color:{PRIMARY};">{len(reqs):,}</div>
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
        height=180  # Squeezed
    )

    pie_colors = [PRIMARY, ACCENT, SECONDARY, TERTIARY]
    origin_fig = go.Figure(go.Pie(
        labels=origin['origin'],
        values=origin['count'],
        hole=0.5,
        marker=dict(colors=pie_colors, line=dict(width=2, color=CARD)),
        textinfo="none"
    ))
    origin_fig.update_layout(
        title="<span style='font-weight:750; color:%s;'>Request Origins</span>" % FONT_CARD,
        template="plotly_dark",
        paper_bgcolor=CARD,
        margin=dict(l=0, r=20, t=45, b=10), 
        legend=dict(font=dict(size=13, color=FONT_LABEL), orientation="v", yanchor="middle", y=0.5, xanchor="right", x=1.0),
        height=155  # Squeezed
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
        title="<span style='font-weight:750; color:%s;'>Top 10 Departments</span>" % FONT_CARD,
        template="plotly_dark",
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        yaxis=dict(title="", autorange="reversed", tickfont=dict(size=13, color=FONT_LABEL)),
        xaxis=dict(title="Requests", color=FONT_LABEL, gridcolor=GRAY_LINE),
        margin=dict(l=30, r=14, t=45, b=12),
        height=260  # Squeezed
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
        height=195,  # Squeezed
        width=390
    )
    map_fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={"lat": subset["latitude"].mean(), "lon": subset["longitude"].mean()},
        paper_bgcolor=CARD,
        margin=dict(l=2, r=2, t=50, b=2),
        title="<span style='font-weight:750; color:%s;'>Request Locations</span>" % FONT_CARD,
        annotations=[]  # Watermark Removed
    )
    map_fig.update_traces(marker=dict(size=6, opacity=0.5))

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>311 Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
        <style>
            html, body {{
                background: {BG_MAIN};
                font-family: 'Inter', sans-serif;
                margin: 0;
                padding: 0;
            }}
            .dash-container {{
                max-width: 1380px;
                margin: 12px auto;
                padding-bottom: 40px;
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
            .card-grid {{
                display: grid;
                grid-template-columns: 0.8fr 0.9fr 0.9fr;
                grid-template-rows: auto auto auto;
                gap: 15px;
            }}
            .card {{
                box-shadow: 0 8px 26px rgba(0,0,0,0.25);
                border-radius: 16px;
                background: #24243A;
                border: 1px solid #39395A;
                padding: 12px 16px 6px 16px;
                transition: transform 0.2s ease, background-color 0.3s ease;
            }}
            .card:hover {{
                background-color: #24243A;
                transform: translateY(-4px);
                cursor: pointer;
            }}
            .kpi-card {{
                grid-row:1;
                grid-column:1;
                padding:0;
                display:flex;
                align-items:center;
                justify-content:center;
            }}
        </style>
    </head>
    <body>
        <div class="dash-container">
            <div class="dash-title">311 Requests Dashboard</div>
            <div class="dash-subtitle">A monthly breakdown of 311 activity across the city.</div>
            <div class="card-grid">
                <div class="card kpi-card">{main_kpi_html}</div>
                <div class="card" style="grid-row:1;grid-column:2;">{status_fig.to_html(full_html=False, include_plotlyjs='cdn')}</div>
                <div class="card" style="grid-row:1;grid-column:3;">{origin_fig.to_html(full_html=False, include_plotlyjs=False)}</div>
                <div class="card" style="grid-row:2;grid-column:1;">{map_fig.to_html(full_html=False, include_plotlyjs=False)}</div>
                <div class="card" style="grid-row:2;grid-column:2/4;">{dept_fig.to_html(full_html=False, include_plotlyjs=False)}</div>
                <div class="card" style="grid-row:3;grid-column:1/4;">{ts_fig.to_html(full_html=False, include_plotlyjs=False)}</div>
            </div>
        </div>
    </body>
    </html>
    """

    with open(output, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Your dashboard is ready!")

if __name__ == "__main__":
    reqs, status, origin, dept, months = load_data()
    create_dashboard(reqs, status, origin, dept, months)
