import pandas as pd
import plotly.graph_objects as go
import os


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
        kpi_metrics = pd.read_csv(os.path.join(data_dir, "kpi_metrics.csv"))
        trip_type = pd.read_csv(os.path.join(data_dir, "trip_type_data.csv"))
        state_data = pd.read_csv(os.path.join(data_dir, "state_data.csv"))
        revenue_miles_scatter = pd.read_csv(os.path.join(data_dir, "revenue_miles_scatter.csv"))
        city_data = pd.read_csv(os.path.join(data_dir, "city_data.csv"))
    except FileNotFoundError as e:
        print(f"Error: Could not find CSV files. Please ensure the following files exist:")
        print("- kpi_metrics.csv")
        print("- trip_type_data.csv")
        print("- state_data.csv")
        print("- revenue_miles_scatter.csv")
        print("- city_data.csv")
        print(f"\nLooking in directory: {os.path.abspath(data_dir)}")
        raise e
    
    return kpi_metrics, trip_type, state_data, revenue_miles_scatter, city_data


def create_kpi_indicators(kpi_metrics):
    indicator_figs = []
    colors = ["#A838F3", "#C084FC", "#A838F3", "#C084FC", "#A838F3"]
    
    for i, row in kpi_metrics.iterrows():
        prefix = "" if pd.isna(row["prefix"]) else row["prefix"]
        suffix = "" if pd.isna(row["suffix"]) else row["suffix"]
        
        fig = go.Figure(go.Indicator(
            mode="number",
            title={"text": f"<b>{str(row['metric']).upper()}</b>", "font": {"size": 14, "family": "Arial", "color": "#4A5568"}},
            value=row["value"],
            number={"prefix": prefix, "suffix": suffix, "font": {"size": 40, "color": colors[i % len(colors)], "family": "Arial"}}
        ))
        
        fig.update_layout(
            height=120,
            margin=dict(t=40, b=20, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        
        indicator_figs.append(fig)
    
    return indicator_figs


def create_trip_type_donut(trip_type):
    colors = ["#6B46C1", "#C084FC", "#DAAAF8"]
    fig = go.Figure(data=[go.Pie(
        labels=trip_type["trip_type"],
        values=trip_type["total_miles"],
        hole=0.33,
        marker_colors=colors,
        textinfo="percent",
        textposition="auto",
        textfont=dict(size=12, color="white"),
        hovertemplate="<b>%{label}</b><br>Miles: %{value:,.0f}<br>Percentage: %{percent}<extra></extra>"
    )])
    
    fig.update_layout(
        title={"text": "<b>TotalMiles by TripType</b>", "x": 0.02, "y": 0.95, "xanchor": "left", "font": {"size": 16, "color": "#2D3748"}},
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.9,
            xanchor="left",
            x=1.02,
            font=dict(size=11)
        ),
        margin=dict(t=50, b=20, l=20, r=20),
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_state_analysis(state_data):
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Revenue", x=state_data["state_code"], y=state_data["revenue"], marker_color="#6B46C1", yaxis="y", offsetgroup=1))
    fig.add_trace(go.Bar(name="TotalMiles", x=state_data["state_code"], y=state_data["total_miles"], marker_color="#C084FC", yaxis="y2", offsetgroup=2))
    
    fig.update_layout(
        title={"text": "<b>TotalMiles and Revenue by shipping state</b>", "x": 0.02, "y": 0.95, "xanchor": "left", "font": {"size": 16, "color": "#2D3748"}},
        xaxis=dict(title=dict(text="OriginState", font=dict(size=12))),
        yaxis=dict(title=dict(text="Revenue", font=dict(size=12)), side="left", tickformat="$,.0f"),
        yaxis2=dict(title=dict(text="TotalMiles", font=dict(size=12)), side="right", overlaying="y", tickformat=",.0f"),
        barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=80, b=60, l=60, r=60),
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_revenue_miles_scatter(revenue_miles_scatter):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=revenue_miles_scatter["total_miles"],
        y=revenue_miles_scatter["revenue"],
        mode="markers",
        marker=dict(color="#6B46C1", size=4, opacity=0.6),
        name="Data Points",
        hovertemplate="<b>Miles: %{x:,.0f}</b><br>Revenue: $%{y:,.0f}<extra></extra>"
    ))
    
    fig.update_layout(
        title={"text": "<b>Revenue Vs TotalMiles</b>", "x": 0.02, "y": 0.95, "xanchor": "left", "font": {"size": 16, "color": "#2D3748"}},
        xaxis=dict(title=dict(text="TotalMiles", font=dict(size=12)), tickformat=",.0f"),
        yaxis=dict(title=dict(text="Revenue", font=dict(size=12)), tickformat="$,.0f"),
        showlegend=False,
        margin=dict(t=50, b=60, l=80, r=20),
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_city_analysis(city_data):
    top_cities = city_data.head(20)
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Revenue", x=top_cities["city"], y=top_cities["revenue"], marker_color="#6B46C1", yaxis="y", offsetgroup=1))
    fig.add_trace(go.Bar(name="TotalMiles", x=top_cities["city"], y=top_cities["total_miles"], marker_color="#C084FC", yaxis="y2", offsetgroup=2))
    
    fig.update_layout(
        title={"text": "<b>Revenue and TotalMiles by Shipping City</b>", "x": 0.02, "y": 0.95, "xanchor": "left", "font": {"size": 16, "color": "#2D3748"}},
        xaxis=dict(title=dict(text="OriginCity", font=dict(size=12)), tickangle=-45),
        yaxis=dict(title=dict(text="Revenue", font=dict(size=12)), side="left", tickformat="$,.0f"),
        yaxis2=dict(title=dict(text="TotalMiles", font=dict(size=12)), side="right", overlaying="y", tickformat=",.0f"),
        barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=80, b=120, l=80, r=80),
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_dashboard(kpi_metrics, trip_type, state_data, revenue_miles_scatter, city_data, output=None):
    if output is None:
        # Create outputs directory if it doesn't exist
        script_dir = os.path.dirname(os.path.abspath(__file__))
        outputs_dir = os.path.join(script_dir, "..", "outputs")
        if not os.path.exists(outputs_dir):
            outputs_dir = os.path.join(script_dir, "outputs")
            if not os.path.exists(outputs_dir):
                os.makedirs(outputs_dir)
        output = os.path.join(outputs_dir, "dashboard.html")
    
    kpi_indicators = create_kpi_indicators(kpi_metrics)
    trip_type_donut = create_trip_type_donut(trip_type)
    state_analysis = create_state_analysis(state_data)
    revenue_miles_scatter = create_revenue_miles_scatter(revenue_miles_scatter)
    city_analysis = create_city_analysis(city_data)
    
    custom_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Logistics Analysis Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #F3E8FF 0%, #FAF5FF 100%);
                min-height: 100vh;
            }}
            .dashboard-header {{
                text-align: center;
                margin-bottom: 20px;
                padding: 15px;
                background: #7C3AED;
                border-radius: 10px;
                color: white;
                box-shadow: 0 6px 20px rgba(107, 70, 193, 0.2);
            }}
            .dashboard-title {{
                font-size: 36px;
                font-weight: bold;
                margin: 0;
            }}
            .dashboard-container {{
                max-width: 1800px;
                margin: 0 auto;
            }}
            .card {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(107, 70, 193, 0.15);
                padding: 20px;
                margin: 8px;
                transition: all 0.3s ease;
                border: 1px solid rgba(107, 70, 193, 0.1);
            }}
            .card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 12px 48px rgba(107, 70, 193, 0.25);
            }}
            .kpi-card {{
                text-align: center;
                position: relative;
            }}
            .delta-indicator {{
                position: absolute;
                top: 10px;
                right: 15px;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
                color: white;
            }}
            .positive {{ background: #10B981; }}
            .negative {{ background: #EF4444; }}
            .dashboard-grid {{
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                grid-template-rows: auto auto auto;
                gap: 15px;
                max-width: 1800px;
                margin: 0 auto;
            }}
            .row-1 {{ grid-row: 1; }}
            .row-2 {{ grid-row: 2; }}
            .row-3 {{ grid-row: 3; }}
            .col-1 {{ grid-column: 1; }}
            .col-2 {{ grid-column: 2; }}
            .col-3 {{ grid-column: 3; }}
            .col-4 {{ grid-column: 4; }}
            .col-5 {{ grid-column: 5; }}
            .col-1-2 {{ grid-column: 1/3; }}
            .col-3-5 {{ grid-column: 3/6; }}
            
            /* Responsive Design */
            @media screen and (max-width: 1200px) {{
                .dashboard-grid {{
                    grid-template-columns: repeat(3, 1fr);
                    grid-template-rows: auto auto auto auto;
                }}
                .col-1 {{ grid-column: 1; }}
                .col-2 {{ grid-column: 2; }}
                .col-3 {{ grid-column: 3; }}
                .col-4 {{ grid-column: 1; grid-row: 2; }}
                .col-5 {{ grid-column: 2; grid-row: 2; }}
                .col-1-2 {{ grid-column: 3; grid-row: 1/3; }}
                .col-3-5 {{ grid-column: 1/4; grid-row: 3; }}
                .row-3.col-1-2 {{ grid-column: 1/3; grid-row: 4; }}
                .row-3.col-3-5 {{ grid-column: 3; grid-row: 4; }}
            }}
            
            @media screen and (max-width: 900px) {{
                body {{
                    padding: 15px;
                }}
                .dashboard-title {{
                    font-size: 28px;
                }}
                .dashboard-grid {{
                    grid-template-columns: repeat(2, 1fr);
                    grid-template-rows: auto auto auto auto auto auto;
                    gap: 12px;
                }}
                .col-1 {{ grid-column: 1; grid-row: 1; }}
                .col-2 {{ grid-column: 2; grid-row: 1; }}
                .col-3 {{ grid-column: 1; grid-row: 2; }}
                .col-4 {{ grid-column: 2; grid-row: 2; }}
                .col-5 {{ grid-column: 1; grid-row: 3; }}
                .col-1-2 {{ grid-column: 2; grid-row: 3/5; }}
                .col-3-5 {{ grid-column: 1/3; grid-row: 5; }}
                .row-3.col-1-2 {{ grid-column: 1/3; grid-row: 6; }}
                .row-3.col-3-5 {{ grid-column: 1/3; grid-row: 7; }}
                .card {{
                    padding: 15px;
                    margin: 4px;
                }}
            }}
            
            @media screen and (max-width: 600px) {{
                body {{
                    padding: 10px;
                }}
                .dashboard-title {{
                    font-size: 24px;
                }}
                .dashboard-header {{
                    padding: 12px;
                }}
                .dashboard-grid {{
                    grid-template-columns: 1fr;
                    grid-template-rows: repeat(8, auto);
                    gap: 10px;
                }}
                .col-1, .col-2, .col-3, .col-4, .col-5, 
                .col-1-2, .col-3-5, .row-3.col-1-2, .row-3.col-3-5 {{
                    grid-column: 1;
                }}
                .col-1 {{ grid-row: 1; }}
                .col-2 {{ grid-row: 2; }}
                .col-3 {{ grid-row: 3; }}
                .col-4 {{ grid-row: 4; }}
                .col-5 {{ grid-row: 5; }}
                .col-1-2 {{ grid-row: 6; }}
                .col-3-5 {{ grid-row: 7; }}
                .row-3.col-1-2 {{ grid-row: 8; }}
                .row-3.col-3-5 {{ grid-row: 9; }}
                .card {{
                    padding: 12px;
                    margin: 2px;
                }}
                .delta-indicator {{
                    font-size: 10px;
                    padding: 3px 6px;
                }}
            }}
            
            @media screen and (max-width: 400px) {{
                body {{
                    padding: 8px;
                }}
                .dashboard-title {{
                    font-size: 20px;
                }}
                .dashboard-header {{
                    padding: 10px;
                }}
                .card {{
                    padding: 10px;
                    margin: 1px;
                }}
            }}
            
            /* Make Plotly charts responsive */
            .plotly-graph-div {{
                width: 100% !important;
                height: auto !important;
            }}
        </style>
        <script>
            // Make Plotly charts responsive
            window.addEventListener('resize', function() {{
                var plots = document.querySelectorAll('.plotly-graph-div');
                for (var i = 0; i < plots.length; i++) {{
                    Plotly.Plots.resize(plots[i]);
                }}
            }});
        </script>
    </head>
    <body>
        <div class="dashboard-container">
        <div class="dashboard-header">
            <h1 class="dashboard-title">Logistics Insights Dashboard</h1>
        </div>
        <div class="dashboard-grid">
            {''.join([
                f'''
                <div class="card kpi-card row-1 col-{i+1}">
                    {kpi_indicators[i].to_html(full_html=False, include_plotlyjs='cdn' if i==0 else False)}
                    <div class="delta-indicator {'positive' if kpi_metrics.iloc[i]['delta'] > 0 else 'negative'}">
                        {'+' if kpi_metrics.iloc[i]['delta'] > 0 else ''}{kpi_metrics.iloc[i]['delta']:.1f}%
                    </div>
                </div>
                '''
                for i in range(min(5, len(kpi_indicators)))
            ])}
            <div class="card row-2 col-1-2">
                {trip_type_donut.to_html(full_html=False, include_plotlyjs=False)}
            </div>
            <div class="card row-2 col-3-5">
                {state_analysis.to_html(full_html=False, include_plotlyjs=False)}
            </div>
            <div class="card row-3 col-1-2">
                {revenue_miles_scatter.to_html(full_html=False, include_plotlyjs=False)}
            </div>
            <div class="card row-3 col-3-5">
                {city_analysis.to_html(full_html=False, include_plotlyjs=False)}
            </div>
        </div>
    </body>
    </html>
    """
    with open(output, "w") as f:
        f.write(custom_html)
    print(f"Dashboard created successfully!")


def main():
    kpi_metrics, trip_type, state_data, revenue_miles_scatter, city_data = load_data()
    create_dashboard(kpi_metrics, trip_type, state_data, revenue_miles_scatter, city_data)


if __name__ == "__main__":
    main()
