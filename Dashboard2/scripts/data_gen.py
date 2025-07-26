import numpy as np
import pandas as pd

def generate_kpi_metrics(filename="../data/kpi_metrics.csv"):
    """Generate top-level KPI metrics for the dashboard"""
    metrics = [
        ("Revenue", 9.2, 12.5, "$", "M"),
        ("Total Miles", 1.1, -5.2, "", "M"),
        ("Shipping Cost", 8.1, 8.9, "$", "M"),
        ("Avg Cost per Mile", 7.36, -2.1, "$", ""),
        ("On-Time Delivery", 94.2, 3.4, "", "%"),
    ]
    df = pd.DataFrame(metrics, columns=["metric", "value", "delta", "prefix", "suffix"])
    df.to_csv(filename, index=False)

def generate_trip_type_data(filename="../data/trip_type_data.csv"):
    """Generate trip type breakdown data"""
    np.random.seed(42)
    
    # Generate realistic trip type distribution
    trip_types = ["Domestic", "International", "Intercom"]
    
    # Domestic should be majority, international moderate, intercom smallest
    domestic_miles = np.random.normal(850000, 50000)
    international_miles = np.random.normal(450000, 30000)
    intercom_miles = np.random.normal(120000, 15000)
    
    data = {
        "trip_type": trip_types,
        "total_miles": [domestic_miles, international_miles, intercom_miles],
        "percentage": [0, 0, 0]  # Will calculate after
    }
    
    df = pd.DataFrame(data)
    df["total_miles"] = df["total_miles"].astype(int)
    total = df["total_miles"].sum()
    df["percentage"] = (df["total_miles"] / total * 100).round(1)
    
    df.to_csv(filename, index=False)

def generate_state_data(filename="../data/state_data.csv"):
    """Generate state-wise shipping data"""
    np.random.seed(123)
    
    states = ["IL", "MI", "WI", "IN", "OH", "IA"]
    state_names = ["Illinois", "Michigan", "Wisconsin", "Indiana", "Ohio", "Iowa"]
    
    data = []
    for state, name in zip(states, state_names):
        # Generate realistic revenue and miles for each state
        revenue = np.random.uniform(500000, 3000000)
        miles = np.random.uniform(100000, 800000)
        
        data.append({
            "state_code": state,
            "state_name": name,
            "revenue": revenue,
            "total_miles": miles
        })
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def generate_revenue_miles_scatter(filename="../data/revenue_miles_scatter.csv"):
    """Generate detailed revenue vs miles scatter plot data"""
    np.random.seed(789)
    
    # Generate 1000+ data points for realistic scatter plot
    n_points = 1200
    
    # Create correlation between miles and revenue with some noise
    miles = np.random.uniform(50, 1200, n_points)
    
    # Revenue should generally correlate with miles but with variation
    base_revenue = miles * np.random.uniform(15, 45, n_points)  # Variable rate per mile
    noise = np.random.normal(0, base_revenue * 0.2)  # 20% noise
    revenue = np.maximum(base_revenue + noise, miles * 5)  # Minimum rate
    
    # Add some trip type context
    trip_types = np.random.choice(["Domestic", "International", "Intercom"], n_points, 
                                 p=[0.6, 0.3, 0.1])
    
    data = {
        "total_miles": miles,
        "revenue": revenue,
        "trip_type": trip_types
    }
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def generate_city_data(filename="../data/city_data.csv"):
    """Generate city-wise revenue and miles data"""
    np.random.seed(101)
    
    # Generate 30+ cities for realistic bar chart
    cities = [
        "Chicago", "Detroit", "Milwaukee", "Indianapolis", "Columbus", "Des Moines",
        "Springfield", "Grand Rapids", "Madison", "Fort Wayne", "Toledo", "Davenport",
        "Rockford", "Peoria", "Lansing", "Green Bay", "Evansville", "Cedar Rapids",
        "Kalamazoo", "Appleton", "Terre Haute", "Lima", "Dubuque", "Joliet",
        "Naperville", "Warren", "Sterling Heights", "Ann Arbor", "Flint", "Dearborn",
        "Livonia", "Westland", "Farmington Hills", "Troy", "Southfield", "Pontiac"
    ]
    
    data = []
    for city in cities:
        # Generate realistic revenue and miles
        revenue = np.random.uniform(200000, 2500000)
        miles = np.random.uniform(50000, 600000)
        
        data.append({
            "city": city,
            "revenue": revenue,
            "total_miles": miles
        })
    
    df = pd.DataFrame(data)
    # Sort by revenue descending for better visualization
    df = df.sort_values("revenue", ascending=False)
    df.to_csv(filename, index=False)

def main():
    # Generate all datasets
    generate_kpi_metrics() 
    generate_trip_type_data()
    generate_state_data()
    generate_revenue_miles_scatter()
    generate_city_data()
    
    print("All datasets generated successfully!")

if __name__ == "__main__":
    main()