import numpy as np
import pandas as pd

np.random.seed(42)
N_REQUESTS = 6810
START_DATE = pd.Timestamp("2024-01-01")
END_DATE   = pd.Timestamp("2024-12-31")
CITY_CENTRE = (40.4406, -79.9959) # Pittsburgh city center
CITY_RADIUS = 0.13

CATEGORIES = [
    "Accessibility", "Animal Issue", "Road Repair", "Streetlight", "Waste", "Trees/Public Space",
    "Graffiti", "Noise", "Water Leak", "General Inquiry"
]
STATUSES = ["New", "Open", "On Hold", "Closed"]
STATUS_PROBS = [0.22, 0.18, 0.03, 0.57]
DEPARTMENTS = [
    "DPW – Refuse", "DPW – Street Maint", "DOMI – Permits", "PWSA", "DOMI – TrafficShop", 
    "Public Safety", "Parks & Rec", "Animal Care", "Building Code", "311 General"
]
DEPT_PROBS = np.array([0.23,0.18,0.11,0.10,0.08,0.07,0.07,0.06,0.05,0.05])
ORIGINS = ["Call Center", "Website", "Mobile App", "Other"]
ORIGIN_PROBS = [0.59, 0.27, 0.08, 0.06]
DIVISIONS = ["North", "South", "East", "West", "Central"]

def random_points_around_city(n, lat_c, lon_c, radius):
    angles = np.random.uniform(0, 2*np.pi, n)
    radii = np.random.beta(2,2, n) * radius 
    lat_offsets = np.cos(angles) * radii
    lon_offsets = np.sin(angles) * radii * 1.2  
    return lat_c + lat_offsets, lon_c + lon_offsets

def generate_requests_log(filename="../data/requests_log.csv"):
    created_dates = pd.to_datetime(np.random.uniform(
        START_DATE.value, END_DATE.value, N_REQUESTS)).floor("min")
    statuses = np.random.choice(STATUSES, N_REQUESTS, p=STATUS_PROBS)
    categories = np.random.choice(CATEGORIES, N_REQUESTS)
    departments = np.random.choice(DEPARTMENTS, N_REQUESTS, p=DEPT_PROBS)
    origins = np.random.choice(ORIGINS, N_REQUESTS, p=ORIGIN_PROBS)
    divisions = np.random.choice(DIVISIONS, N_REQUESTS)
    neighborhoods = np.random.choice(
        ["Downtown","Brookline","Squirrel Hill","Carrick","North Oakland","Shadyside","Bloomfield","Beechview","East Liberty","Strip District"], 
        N_REQUESTS)
    latitudes, longitudes = random_points_around_city(N_REQUESTS, *CITY_CENTRE, CITY_RADIUS)
    
    # Build DF
    df_req = pd.DataFrame({
        "request_id": range(1, N_REQUESTS+1),
        "created_at": created_dates,
        "status": statuses,
        "category": categories,
        "department": departments,
        "origin": origins,
        "division": divisions,
        "neighborhood": neighborhoods,
        "latitude": latitudes,
        "longitude": longitudes
    })
    df_req.to_csv(filename, index=False)

def aggregate_tables(log_csv="../data/requests_log.csv"):
    df = pd.read_csv(log_csv, parse_dates=["created_at"])

    # By status
    status_df = df.groupby("status")["request_id"].count().reset_index()
    status_df.rename(columns={"request_id": "count"}, inplace=True)
    status_df.to_csv("../data/requests_status.csv", index=False)
    
    # By origin
    ori_df = df.groupby("origin")["request_id"].count().reset_index()
    ori_df.rename(columns={"request_id": "count"}, inplace=True)
    ori_df.to_csv("../data/requests_origin.csv", index=False)
    
    # By department (Top 10)
    dept_df = df.groupby("department")["request_id"].count().reset_index()
    dept_df.rename(columns={"request_id": "count"}, inplace=True)
    dept_df = dept_df.sort_values("count", ascending=False).head(10)
    dept_df.to_csv("../data/requests_department.csv", index=False)

    # By month
    df["month"] = df["created_at"].dt.to_period("M").astype(str)
    mo_df = df.groupby("month")["request_id"].count().reset_index()
    mo_df.rename(columns={"request_id": "count"}, inplace=True)
    mo_df.to_csv("../data/requests_monthly.csv", index=False)

def main():
    generate_requests_log()
    aggregate_tables()
    
    print("All datasets generated successfully!")

if __name__ == "__main__":
    main()