import pandas as pd
import plotly.graph_objects as go

def load_data():
    hierarchical = pd.read_csv("../data/hierarchical_expenses.csv")
    return hierarchical

def fix_duplicate_names(df):
    df_fixed = df.copy()
    name_counts = df_fixed['name'].value_counts()
    duplicates = name_counts[name_counts > 1].index.tolist()
    
    for dup_name in duplicates:
        dup_rows = df_fixed[df_fixed['name'] == dup_name]
        for idx, (_, row) in enumerate(dup_rows.iterrows()):
            if row['parent'] != '':
                new_name = f"{row['parent']} - {dup_name}"
                df_fixed.loc[df_fixed['name'] == dup_name, 'name'] = new_name
                children_mask = df_fixed['parent'] == dup_name
                if children_mask.any():
                    df_fixed.loc[children_mask, 'parent'] = new_name
                break
    
    return df_fixed

def fix_hierarchical_values(df):
    df_fixed = df.copy()
    
    for level in range(1, df_fixed['level'].max() + 1):
        level_parents = df_fixed[df_fixed['level'] == level - 1]['name'].unique()
        
        for parent in level_parents:
            if parent == '':
                continue
                
            children = df_fixed[df_fixed['parent'] == parent]
            if len(children) == 0:
                continue
                
            parent_value = df_fixed[df_fixed['name'] == parent]['value'].iloc[0]
            children_sum = children['value'].sum()
            
            if abs(children_sum - parent_value) > 1:
                df_fixed.loc[df_fixed['name'] == parent, 'value'] = children_sum
    
    return df_fixed

def find_root_division(df, node_name, color_families):
    current = node_name
    visited = set()
    
    while current and current != '' and current not in visited:
        visited.add(current)
        
        if current in color_families and current != "Total Budget":
            return current
            
        parent_row = df[df['name'] == current]
        if len(parent_row) == 0:
            break
            
        parent = parent_row['parent'].iloc[0]
        current = parent
    
    return None

def adjust_color_brightness(hex_color, factor):
    if not hex_color.startswith('#'):
        return hex_color
    
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    
    if factor < 1:
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
    else:
        r = int(r + (255 - r) * (factor - 1))
        g = int(g + (255 - g) * (factor - 1))
        b = int(b + (255 - b) * (factor - 1))
    
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    
    return f"rgb({r},{g},{b})"

def create_rectangular_budget_breakdown(hierarchical_df):
    df = hierarchical_df.copy()
    df['parent'] = df['parent'].fillna('')
    
    duplicates = df[df.duplicated('name', keep=False)]
    if len(duplicates) > 0:
        df = fix_duplicate_names(df)
    
    df = fix_hierarchical_values(df)
    df = df.sort_values(['level', 'value'], ascending=[True, False]).reset_index(drop=True)
    
    color_families = {
        "Total Budget": "#3bb3ef",
        "Operations": "#6647f0",
        "Technology": "#9851f6",
        "Sales & Marketing": "#e049db",
        "Human Resources": "#ee4376",
        "Finance & Admin": "#eba74d",
        "Research & Development": "#47f0d4"
    }
    
    color_assignments = {}
    
    for name, color in color_families.items():
        color_assignments[name] = color
    
    for _, row in df.iterrows():
        node_name = row['name']
        
        if node_name in color_assignments:
            continue
            
        root_division = find_root_division(df, node_name, color_families)
        
        if root_division:
            base_color = color_families[root_division]
            level = row['level']
            
            if level == 2:
                color_assignments[node_name] = adjust_color_brightness(base_color, 0.85)
            elif level == 3:
                color_assignments[node_name] = adjust_color_brightness(base_color, 1.15)
            else:
                brightness_factor = 1.1 + (level - 3) * 0.1
                color_assignments[node_name] = adjust_color_brightness(base_color, min(brightness_factor, 1.4))
        else:
            fallback_colors = list(color_families.values())[1:]
            color_assignments[node_name] = adjust_color_brightness(
                fallback_colors[hash(node_name) % len(fallback_colors)], 1.2
            )
    
    colors = [color_assignments.get(name, '#94a3b8') for name in df['name']]
    
    value_range = df['value'].max() - df['value'].min()
    small_values = df[df['value'] < value_range * 0.05]
    
    if len(small_values) > len(df) * 0.3:
        dynamic_pad = 0.3
    else:
        dynamic_pad = 0.8
    
    fig = go.Figure(go.Icicle(
        labels=df['name'],
        parents=df['parent'],
        values=df['value'],
        textinfo="label+value",
        texttemplate="<b>%{label}</b><br>$%{value:,.0f}",
        hovertemplate="<b>%{label}</b><br>Value: $%{value:,.0f}<br>%{percentParent} of parent<extra></extra>",
        maxdepth=4,
        branchvalues="total",
        marker=dict(
            colors=colors,
            line=dict(color='white', width=0.8)
        ),
        textfont=dict(color='white', size=10, family="Arial"),
        tiling=dict(orientation='h', pad=dynamic_pad),
        pathbar=dict(
            visible=True,
            thickness=25,
            textfont=dict(size=11, color='white', family="Arial")
        )
    ))
    
    fig.update_layout(
        title={
            'text': "Budget Distribution Overview",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': "#4f8beb"}
        },
        margin=dict(t=60, l=20, r=20, b=20),
        height=600,
        template="plotly_white",
        font=dict(size=10, family="Arial, sans-serif", color='white')
    )
    
    return fig

def create_dashboard(hierarchical, output="../outputs/dashboard.html"):
    budget_fig = create_rectangular_budget_breakdown(hierarchical)
    
    total_budget = hierarchical[hierarchical['name'] == 'Total Budget']['value'].values[0]
    num_divisions = len(hierarchical[hierarchical['level'] == 1])
    num_categories = len(hierarchical[hierarchical['level'] == 2])
    
    chart_html = budget_fig.to_html(
        full_html=False, 
        include_plotlyjs='cdn',
        div_id="budget-chart"
    )
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Budget Distribution Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }}
        
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                        radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                        radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
            z-index: -1;
            animation: float 20s ease-in-out infinite;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
            33% {{ transform: translateY(-20px) rotate(1deg); }}
            66% {{ transform: translateY(10px) rotate(-1deg); }}
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 40px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 100%);
            border-radius: 25px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1), 0 8px 32px rgba(0, 0, 0, 0.08);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
            animation: shine 3s infinite;
        }}
        
        @keyframes shine {{
            0% {{ left: -100%; }}
            100% {{ left: 100%; }}
        }}
        
        .header h1 {{
            color: #2c3e50;
            margin: 0 0 15px 0;
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            position: relative;
            z-index: 1;
        }}
        
        .header p {{
            color: #5a6c7d;
            margin: 0;
            font-size: 20px;
            font-weight: 400;
            position: relative;
            z-index: 1;
        }}
        
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}
        
        .metric {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.8) 100%);
            padding: 35px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 15px 45px rgba(0, 0, 0, 0.1), 0 5px 20px rgba(0, 0, 0, 0.05);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
            cursor: pointer;
        }}
        
        .metric::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .metric:hover {{
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 25px 70px rgba(0, 0, 0, 0.15), 0 10px 40px rgba(0, 0, 0, 0.1);
        }}
        
        .metric:hover::before {{
            opacity: 1;
        }}
        
        .metric.highlight {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            transform: scale(1.05);
        }}
        
        .metric.highlight:hover {{
            transform: translateY(-10px) scale(1.08);
            box-shadow: 0 30px 80px rgba(102, 126, 234, 0.4), 0 15px 50px rgba(118, 75, 162, 0.3);
        }}
        
        .metric.highlight .metric-value {{
            color: white;
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
            font-weight: 900;
            -webkit-text-fill-color: white;
            background: none;
        }}
        
        .metric.highlight .metric-label {{
            color: rgba(255, 255, 255, 0.9);
        }}
        
        .metric-value {{
            font-size: 48px;
            font-weight: 900;
            margin: 15px 0;
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            transition: all 0.3s ease;
        }}
        
        .metric-label {{
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 700;
            color: #5a6c7d;
            position: relative;
        }}
        
        .chart-container {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 100%);
            padding: 30px;
            border-radius: 25px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1), 0 8px 32px rgba(0, 0, 0, 0.08);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }}
        
        .chart-container:hover {{
            transform: translateY(-5px);
            box-shadow: 0 25px 70px rgba(0, 0, 0, 0.15), 0 10px 40px rgba(0, 0, 0, 0.1);
        }}
        
        .info {{
            text-align: center;
            color: rgba(255, 255, 255, 0.95);
            margin-top: 30px;
            padding: 25px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }}
        
        .info:hover {{
            transform: translateY(-3px);
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
        }}
        
        .info p {{
            font-size: 16px;
            font-weight: 500;
            margin: 0;
        }}
        
        .info strong {{
            color: #fff;
            font-weight: 700;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            body {{
                padding: 15px;
            }}
            
            .header {{
                padding: 25px;
                margin-bottom: 25px;
            }}
            
            .header h1 {{
                font-size: 32px;
            }}
            
            .header p {{
                font-size: 16px;
            }}
            
            .metrics {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            
            .metric {{
                padding: 25px;
            }}
            
            .metric-value {{
                font-size: 36px;
            }}
        }}
        
        /* Loading Animation */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .container > * {{
            animation: fadeInUp 0.8s ease-out forwards;
        }}
        
        .header {{
            animation-delay: 0.1s;
        }}
        
        .metrics {{
            animation-delay: 0.2s;
        }}
        
        .chart-container {{
            animation-delay: 0.3s;
        }}
        
        .info {{
            animation-delay: 0.4s;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Budget Distribution Dashboard</h1>
            <p>Interactive hierarchical visualization of organizational expenses</p>
        </div>
        
        <div class="metrics">
            <div class="metric highlight">
                <div class="metric-label">Total Budget</div>
                <div class="metric-value">${total_budget/1e6:.1f}M</div>
            </div>
            <div class="metric">
                <div class="metric-label">Divisions</div>
                <div class="metric-value">{num_divisions}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Categories</div>
                <div class="metric-value">{num_categories}</div>
            </div>
        </div>
        
        <div class="chart-container">
            {chart_html}
        </div>
        
        <div class="info">
            <p><strong>Interactive Features:</strong> Click on any section to zoom in and explore subcategories. 
            Use the path bar at the top to navigate back to parent levels.</p>
        </div>
    </div>
</body>
</html>
"""
    
    with open(output, "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    hierarchical = load_data()
    create_dashboard(hierarchical)
    print("Dashboard created successfully!")