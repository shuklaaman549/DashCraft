import pandas as pd
import plotly.graph_objects as go

def load_data():
    revenue_hierarchy = pd.read_csv("../data/revenue_hierarchy.csv")
    return revenue_hierarchy

def create_sunburst_chart(revenue_data):
    region_colors = {
        'North America': '#FF6B6B',
        'Europe': '#4ECDC4',
        'Asia Pacific': '#45B7D1',
        'Latin America': '#96CEB4',
        'Middle East & Africa': '#FFEAA7'
    }
    
    division_colors = {
        'Technology': '#6C5CE7',
        'Manufacturing': '#FD79A8',
        'Healthcare': '#00B894',
        'Financial Services': '#FDCB6E'
    }
    
    sunburst_data = []
    colors = []
    
    total_revenue = revenue_data['revenue'].sum()
    sunburst_data.append({
        'ids': 'Global Business',
        'labels': 'Global Business',
        'parents': '',
        'values': total_revenue,
        'hover_text': f'Total Global Revenue: ${total_revenue:,.0f}'
    })
    colors.append('#E8E8E8')
    
    region_totals = revenue_data.groupby('region').agg({
        'revenue': 'sum',
        'growth_rate': 'mean'
    }).reset_index()
    
    for _, row in region_totals.iterrows():
        sunburst_data.append({
            'ids': row['region'],
            'labels': row['region'],
            'parents': 'Global Business',
            'values': row['revenue'],
            'hover_text': f"{row['region']}<br>Revenue: ${row['revenue']:,.0f}<br>Avg Growth: {row['growth_rate']:.1f}%"
        })
        colors.append(region_colors.get(row['region'], '#74B9FF'))
    
    division_totals = revenue_data.groupby(['region', 'division']).agg({
        'revenue': 'sum',
        'growth_rate': 'mean'
    }).reset_index()
    
    for _, row in division_totals.iterrows():
        division_id = f"{row['region']} - {row['division']}"
        sunburst_data.append({
            'ids': division_id,
            'labels': row['division'],
            'parents': row['region'],
            'values': row['revenue'],
            'hover_text': f"{row['division']}<br>Region: {row['region']}<br>Revenue: ${row['revenue']:,.0f}<br>Avg Growth: {row['growth_rate']:.1f}%"
        })
        colors.append(division_colors.get(row['division'], '#A29BFE'))
    
    product_color_variations = {
        'Cloud Services': '#E17055', 'Software Licenses': '#0984E3', 'AI/ML Solutions': '#6C5CE7',
        'Data Analytics': '#00B894', 'Cybersecurity': '#E84393', 'Mobile Solutions': '#FDCB6E',
        'Automotive': '#FF7675', 'Electronics': '#74B9FF', 'Industrial Equipment': '#81ECEC',
        'Aerospace': '#A29BFE', 'Semiconductors': '#FD79A8', 'Consumer Goods': '#FDCB6E',
        'Renewable Energy': '#00B894', 'Medical Devices': '#55A3FF', 'Pharmaceuticals': '#26DE81',
        'Telehealth': '#FD79A8', 'Digital Health': '#A29BFE', 'Diagnostics': '#FF9FF3',
        'Biotechnology': '#54A0FF', 'Fintech': '#5F27CD', 'Insurance': '#00D2D3',
        'Investment Banking': '#FF9F43', 'Retail Banking': '#EE5A24', 'Digital Banking': '#0ABDE3',
        'Digital Payments': '#10AC84', 'Cryptocurrency': '#EE5A24', 'Microfinance': '#FFC312',
        'Islamic Banking': '#C4E538', 'E-commerce': '#FF6348', 'Food Processing': '#7BED9F',
        'Textiles': '#FF6B9D', 'Mining Equipment': '#70A1FF', 'Oil & Gas Equipment': '#5352ED',
        'Construction': '#FF4757', 'Mining': '#7292D8', 'Medical Infrastructure': '#3742FA'
    }
    
    for _, row in revenue_data.iterrows():
        product_id = f"{row['region']} - {row['division']} - {row['product_category']}"
        parent_id = f"{row['region']} - {row['division']}"
        sunburst_data.append({
            'ids': product_id,
            'labels': row['product_category'],
            'parents': parent_id,
            'values': row['revenue'],
            'hover_text': f"{row['product_category']}<br>Division: {row['division']}<br>Region: {row['region']}<br>Revenue: ${row['revenue']:,.0f}<br>Growth Rate: {row['growth_rate']:.1f}%"
        })
        product_color = product_color_variations.get(row['product_category'], 
        division_colors.get(row['division'], '#A29BFE'))
        colors.append(product_color)
    
    df_sunburst = pd.DataFrame(sunburst_data)
    
    fig = go.Figure(go.Sunburst(
        ids=df_sunburst['ids'],
        labels=df_sunburst['labels'],
        parents=df_sunburst['parents'],
        values=df_sunburst['values'],
        branchvalues="total",
        hovertemplate='<b>%{customdata}</b><extra></extra>',
        customdata=df_sunburst['hover_text'],
        maxdepth=4,
        insidetextorientation='radial',
        rotation=90,
        marker=dict(
            colors=colors,
            line=dict(color="white", width=2)
        )
    ))
    
    fig.update_layout(
        title={
            'text': '<b style="font-size: 28px; color: white;">Global Business Revenue Hierarchy</b><br><span style="font-size: 16px; color: rgba(255, 255, 255, 0.8);">Interactive Multi-Level Sunburst Analysis</span>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'family': 'Inter, Arial, sans-serif', 'color': 'white'}
        },
        font={'size': 14, 'family': 'Inter, Arial, sans-serif'},
        margin=dict(t=100, b=50, l=50, r=50),
        height=700,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_dashboard(revenue_data, output="../outputs/dashboard.html"):
    sunburst_fig = create_sunburst_chart(revenue_data)
    
    total_revenue = revenue_data['revenue'].sum()
    avg_growth = revenue_data['growth_rate'].mean()
    total_regions = revenue_data['region'].nunique()
    total_products = revenue_data['product_category'].nunique()
    highest_growth_product = revenue_data.loc[revenue_data['growth_rate'].idxmax()]
    
    sunburst_div = sunburst_fig.to_html(
        full_html=False, 
        include_plotlyjs='cdn',
        config={'displayModeBar': True, 'responsive': True}
    )
    
    dashboard_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Global Business Intelligence Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                min-height: 100vh;
                color: #1a202c;
                overflow-x: hidden;
            }}
            
            .dashboard-container {{
                max-width: 1600px;
                margin: 0 auto;
                padding: 20px;
                min-height: 100vh;
            }}
            
            .header {{
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                padding: 40px;
                text-align: center;
                margin-bottom: 30px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                position: relative;
                overflow: hidden;
                color: white;
            }}
            
            .header::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(102,126,234,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
                opacity: 0.5;
            }}
            
            .header h1 {{
                font-size: 3rem;
                font-weight: 800;
                color: white;
                margin-bottom: 15px;
                position: relative;
                z-index: 1;
                text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            }}
            
            .header p {{
                font-size: 1.2rem;
                color: rgba(255, 255, 255, 0.9);
                font-weight: 500;
                position: relative;
                z-index: 1;
            }}
            
            .kpi-section {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 25px;
                margin-bottom: 30px;
            }}
            
            .kpi-card {{
                backdrop-filter: blur(20px);
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
                text-align: center;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                border: 1px solid rgba(255, 255, 255, 0.3);
                position: relative;
                overflow: hidden;
                color: white;
            }}
            
            .kpi-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 5px;
                background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c, #4facfe, #00f2fe);
                background-size: 300% 300%;
                animation: gradientShift 4s ease infinite;
            }}
            
            @keyframes gradientShift {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
            
            .kpi-card:nth-child(1) {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            
            .kpi-card:nth-child(2) {{
                background: linear-gradient(135deg, #f093fb 0%, #764ba2 100%);
            }}
            
            .kpi-card:nth-child(3) {{
                background: linear-gradient(135deg, #4facfe 0%, #764ba2 100%);
            }}
            
            .kpi-card:nth-child(4) {{
                background: linear-gradient(135deg, #43e97b 0%, #764ba2 100%);
            }}
            
            .kpi-card:hover {{
                transform: translateY(-10px) scale(1.02);
                box-shadow: 0 25px 70px rgba(0, 0, 0, 0.25);
            }}
            
            .kpi-icon {{
                font-size: 2.5rem;
                margin-bottom: 15px;
                color: rgba(255, 255, 255, 0.9);
                text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            }}
            
            .kpi-value {{
                font-size: 2.8rem;
                font-weight: 800;
                color: white;
                margin-bottom: 10px;
                line-height: 1;
                text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            }}
            
            .kpi-label {{
                font-size: 1rem;
                color: rgba(255, 255, 255, 0.9);
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            .kpi-change {{
                font-size: 0.9rem;
                margin-top: 8px;
                padding: 8px 16px;
                border-radius: 25px;
                font-weight: 600;
                box-shadow: 
                    0 4px 15px rgba(0, 0, 0, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3),
                    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
                position: relative;
                overflow: hidden;
                transition: all 0.3s ease;
            }}
            
            .kpi-change::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 50%;
                background: linear-gradient(180deg, rgba(255, 255, 255, 0.15) 0%, transparent 100%);
                pointer-events: none;
            }}
            
            .kpi-change:hover {{
                transform: translateY(-2px);
                box-shadow: 
                    0 6px 20px rgba(0, 0, 0, 0.25),
                    inset 0 1px 0 rgba(255, 255, 255, 0.4),
                    inset 0 -1px 0 rgba(0, 0, 0, 0.15);
            }}
            
            .positive {{
                backdrop-filter: blur(10px);
                font-weight: 600;
            }}
            
            .chart-main-container {{
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #667eea 100%);
                backdrop-filter: blur(20px);
                border-radius: 25px;
                padding: 40px;
                box-shadow: 0 25px 70px rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                margin-bottom: 30px;
                position: relative;
                overflow: hidden;
            }}
            
            .chart-main-container::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(5px);
                border-radius: 25px;
                pointer-events: none;
            }}
            
            .chart-container {{
                position: relative;
                z-index: 1;
                min-height: 700px;
            }}
            
            .insights-section {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #2C3E50 100%);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                padding: 35px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
            }}
            
            .insights-title {{
                font-size: 1.8rem;
                font-weight: 800;
                color: white;
                margin-bottom: 25px;
                display: flex;
                align-items: center;
                gap: 15px;
                text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
                border-bottom: 2px solid rgba(255, 255, 255, 0.2);
                padding-bottom: 15px;
            }}
            
            .insight-item {{
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.15));
                border-left: 4px solid #FFD700;
                padding: 20px 25px;
                margin-bottom: 18px;
                border-radius: 12px;
                font-weight: 500;
                color: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                backdrop-filter: blur(15px);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
                transition: all 0.3s ease;
            }}
            
            .insight-item:hover {{
                transform: translateY(-3px);
                box-shadow: 0 12px 35px rgba(0, 0, 0, 0.25);
                border-left-color: #FFA500;
            }}
            
            .insight-item strong {{
                color: #FFD700;
                font-weight: 700;
            }}
            
            @media (max-width: 768px) {{
                .header h1 {{
                    font-size: 2.2rem;
                }}
                
                .kpi-section {{
                    grid-template-columns: 1fr;
                    gap: 20px;
                }}
                
                .chart-main-container {{
                    padding: 20px;
                }}
                
                .dashboard-container {{
                    padding: 15px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <div class="header">
                <h1>Global Business Intelligence</h1>
                <p>Multi-Level Hierarchical Data Exploration & Revenue Analytics</p>
            </div>
            
            <div class="kpi-section">
                <div class="kpi-card">
                    <div class="kpi-icon"><i class="fas fa-chart-line"></i></div>
                    <div class="kpi-value">${total_revenue/1000000:.1f}M</div>
                    <div class="kpi-label">Total Revenue</div>
                    <div class="kpi-change positive" style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.4)); color: #10b981; border: 1px solid rgba(102, 126, 234, 0.4);">+{avg_growth:.1f}% Growth</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-icon"><i class="fas fa-globe-americas"></i></div>
                    <div class="kpi-value">{total_regions}</div>
                    <div class="kpi-label">Global Regions</div>
                    <div class="kpi-change positive" style="background: linear-gradient(135deg, rgba(240, 147, 251, 0.3), rgba(118, 75, 162, 0.4)); color: white; border: 1px solid rgba(240, 147, 251, 0.4);">Worldwide Coverage</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-icon"><i class="fas fa-boxes"></i></div>
                    <div class="kpi-value">{total_products}</div>
                    <div class="kpi-label">Product Categories</div>
                    <div class="kpi-change positive" style="background: linear-gradient(135deg, rgba(79, 172, 254, 0.3), rgba(118, 75, 162, 0.4)); color: white; border: 1px solid rgba(79, 172, 254, 0.4);">Diversified Portfolio</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-icon"><i class="fas fa-rocket"></i></div>
                    <div class="kpi-value">{highest_growth_product['growth_rate']:.1f}%</div>
                    <div class="kpi-label">Highest Growth</div>
                    <div class="kpi-change positive" style="background: linear-gradient(135deg, rgba(67, 233, 123, 0.3), rgba(118, 75, 162, 0.4)); color: #FD79A8; border: 1px solid rgba(67, 233, 123, 0.4);">{highest_growth_product['product_category']}</div>
                </div>
            </div>
            
            <div class="chart-main-container">
                <div class="chart-container">
                    {sunburst_div}
                </div>
            </div>
            
            <div class="insights-section">
                <div class="insights-title">
                    <i class="fas fa-lightbulb"></i>
                    Key Insights
                </div>
                <div class="insight-item">
                    <strong>Revenue Distribution:</strong> Click on any segment to drill down into sub-categories and explore the hierarchical data structure.
                </div>
                <div class="insight-item">
                    <strong>Growth Leaders:</strong> Technology division shows the highest growth rates across most regions, particularly in AI/ML Solutions.
                </div>
                <div class="insight-item">
                    <strong>Geographic Performance:</strong> Asia Pacific demonstrates strong growth in digital solutions, while North America leads in absolute revenue.
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(output, 'w', encoding='utf-8') as f:
        f.write(dashboard_html)

def main():
    revenue_data = load_data()
    create_dashboard(revenue_data)
    print("Dashboard created successfully!")

if __name__ == "__main__":
    main()