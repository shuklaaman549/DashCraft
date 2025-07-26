import numpy as np
import pandas as pd

def generate_revenue_hierarchy(filename="../data/revenue_hierarchy.csv"):
    np.random.seed(42)
    
    hierarchy_data = [
        ("North America", "Technology", "Cloud Services", 45000000, 8.5),
        ("North America", "Technology", "Software Licenses", 32000000, 12.3),
        ("North America", "Technology", "AI/ML Solutions", 28000000, 15.7),
        ("North America", "Technology", "Data Analytics", 23000000, 9.8),
        ("North America", "Technology", "Cybersecurity", 19000000, 6.4),
        ("North America", "Manufacturing", "Automotive", 38000000, 4.2),
        ("North America", "Manufacturing", "Electronics", 31000000, 7.1),
        ("North America", "Manufacturing", "Industrial Equipment", 26000000, 3.8),
        ("North America", "Manufacturing", "Aerospace", 22000000, 5.9),
        ("North America", "Healthcare", "Medical Devices", 29000000, 11.2),
        ("North America", "Healthcare", "Pharmaceuticals", 25000000, 8.7),
        ("North America", "Healthcare", "Telehealth", 18000000, 22.4),
        ("North America", "Healthcare", "Diagnostics", 16000000, 6.3),
        ("North America", "Financial Services", "Fintech", 24000000, 18.9),
        ("North America", "Financial Services", "Insurance", 21000000, 5.1),
        ("North America", "Financial Services", "Investment Banking", 19000000, 7.8),
        ("North America", "Financial Services", "Retail Banking", 17000000, 3.2),
        ("Europe", "Technology", "Cloud Services", 35000000, 12.1),
        ("Europe", "Technology", "Software Licenses", 28000000, 9.4),
        ("Europe", "Technology", "AI/ML Solutions", 22000000, 19.3),
        ("Europe", "Technology", "Data Analytics", 18000000, 8.7),
        ("Europe", "Technology", "Cybersecurity", 15000000, 14.2),
        ("Europe", "Manufacturing", "Automotive", 42000000, 6.8),
        ("Europe", "Manufacturing", "Electronics", 26000000, 4.5),
        ("Europe", "Manufacturing", "Industrial Equipment", 24000000, 5.3),
        ("Europe", "Manufacturing", "Renewable Energy", 21000000, 16.7),
        ("Europe", "Healthcare", "Medical Devices", 23000000, 9.1),
        ("Europe", "Healthcare", "Pharmaceuticals", 28000000, 7.4),
        ("Europe", "Healthcare", "Telehealth", 14000000, 25.8),
        ("Europe", "Healthcare", "Diagnostics", 12000000, 8.9),
        ("Europe", "Financial Services", "Fintech", 19000000, 21.3),
        ("Europe", "Financial Services", "Insurance", 25000000, 4.7),
        ("Europe", "Financial Services", "Investment Banking", 16000000, 6.2),
        ("Europe", "Financial Services", "Digital Banking", 13000000, 28.1),
        ("Asia Pacific", "Technology", "Cloud Services", 29000000, 24.7),
        ("Asia Pacific", "Technology", "Software Licenses", 21000000, 18.6),
        ("Asia Pacific", "Technology", "AI/ML Solutions", 33000000, 31.2),
        ("Asia Pacific", "Technology", "Data Analytics", 19000000, 22.4),
        ("Asia Pacific", "Technology", "Mobile Solutions", 25000000, 19.8),
        ("Asia Pacific", "Manufacturing", "Electronics", 48000000, 13.5),
        ("Asia Pacific", "Manufacturing", "Automotive", 31000000, 11.2),
        ("Asia Pacific", "Manufacturing", "Semiconductors", 27000000, 8.9),
        ("Asia Pacific", "Manufacturing", "Consumer Goods", 22000000, 6.7),
        ("Asia Pacific", "Healthcare", "Medical Devices", 17000000, 15.3),
        ("Asia Pacific", "Healthcare", "Digital Health", 21000000, 29.4),
        ("Asia Pacific", "Healthcare", "Pharmaceuticals", 19000000, 12.1),
        ("Asia Pacific", "Healthcare", "Biotechnology", 15000000, 18.7),
        ("Asia Pacific", "Financial Services", "Digital Payments", 32000000, 35.6),
        ("Asia Pacific", "Financial Services", "Cryptocurrency", 18000000, 42.3),
        ("Asia Pacific", "Financial Services", "Insurance", 16000000, 8.4),
        ("Asia Pacific", "Financial Services", "Retail Banking", 14000000, 12.7),
        ("Latin America", "Technology", "Cloud Services", 12000000, 28.4),
        ("Latin America", "Technology", "Software Licenses", 8000000, 15.2),
        ("Latin America", "Technology", "Mobile Solutions", 14000000, 33.7),
        ("Latin America", "Technology", "E-commerce", 16000000, 41.2),
        ("Latin America", "Manufacturing", "Automotive", 18000000, 9.3),
        ("Latin America", "Manufacturing", "Food Processing", 22000000, 7.1),
        ("Latin America", "Manufacturing", "Textiles", 11000000, 5.8),
        ("Latin America", "Manufacturing", "Mining Equipment", 15000000, 8.4),
        ("Latin America", "Healthcare", "Telehealth", 9000000, 45.6),
        ("Latin America", "Healthcare", "Medical Devices", 7000000, 12.8),
        ("Latin America", "Healthcare", "Pharmaceuticals", 11000000, 9.7),
        ("Latin America", "Financial Services", "Digital Banking", 13000000, 38.9),
        ("Latin America", "Financial Services", "Microfinance", 8000000, 22.1),
        ("Latin America", "Financial Services", "Insurance", 6000000, 15.4),
        ("Middle East & Africa", "Technology", "Cloud Services", 8000000, 32.1),
        ("Middle East & Africa", "Technology", "Mobile Solutions", 12000000, 29.8),
        ("Middle East & Africa", "Technology", "Fintech", 10000000, 48.3),
        ("Middle East & Africa", "Manufacturing", "Oil & Gas Equipment", 25000000, 6.2),
        ("Middle East & Africa", "Manufacturing", "Construction", 18000000, 8.7),
        ("Middle East & Africa", "Manufacturing", "Mining", 15000000, 4.9),
        ("Middle East & Africa", "Healthcare", "Telehealth", 6000000, 52.3),
        ("Middle East & Africa", "Healthcare", "Medical Infrastructure", 9000000, 18.4),
        ("Middle East & Africa", "Healthcare", "Pharmaceuticals", 7000000, 14.2),
        ("Middle East & Africa", "Financial Services", "Digital Banking", 11000000, 44.7),
        ("Middle East & Africa", "Financial Services", "Islamic Banking", 14000000, 12.3),
        ("Middle East & Africa", "Financial Services", "Insurance", 5000000, 19.6)
    ]
    
    df = pd.DataFrame(hierarchy_data, columns=["region", "division", "product_category", "revenue", "growth_rate"])
    df.to_csv(filename, index=False)

def main():
    generate_revenue_hierarchy()
    print("Datasets generated successfully!")

if __name__ == "__main__":
    main()