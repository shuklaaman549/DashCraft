import numpy as np
import pandas as pd

def generate_hierarchical_data(filename="../data/hierarchical_expenses.csv"):
    np.random.seed(42)
    
    hierarchy_data = []
    total_budget = 125_000_000
    
    divisions = {
        "Operations": 0.35,
        "Technology": 0.25,
        "Sales & Marketing": 0.20,
        "Human Resources": 0.10,
        "Finance & Admin": 0.07,
        "Research & Development": 0.03
    }
    
    subcategories = {
        "Operations": {
            "Manufacturing": 0.40,
            "Supply Chain": 0.25,
            "Quality Control": 0.15,
            "Facilities": 0.20
        },
        "Technology": {
            "Infrastructure": 0.35,
            "Software Development": 0.30,
            "Data & Analytics": 0.20,
            "Cybersecurity": 0.15
        },
        "Sales & Marketing": {
            "Direct Sales": 0.35,
            "Digital Marketing": 0.25,
            "Brand Management": 0.20,
            "Customer Success": 0.20
        },
        "Human Resources": {
            "Talent Acquisition": 0.30,
            "Employee Development": 0.25,
            "Compensation & Benefits": 0.35,
            "HR Operations": 0.10
        },
        "Finance & Admin": {
            "Accounting": 0.30,
            "Legal & Compliance": 0.35,
            "Business Intelligence": 0.20,
            "Administrative Services": 0.15
        },
        "Research & Development": {
            "Product Research": 0.45,
            "Innovation Labs": 0.30,
            "Patents & IP": 0.25
        }
    }
    
    detailed_items = {
        "Manufacturing": ["Equipment Maintenance", "Raw Materials", "Labor Costs", "Utilities"],
        "Supply Chain": ["Logistics", "Inventory Management", "Vendor Relations", "Warehousing"],
        "Quality Control": ["Testing Equipment", "Inspection Staff", "Compliance Audits"],
        "Facilities": ["Building Maintenance", "Security", "Office Supplies", "Cleaning Services"],
        "Infrastructure": ["Cloud Services", "Network Equipment", "Data Centers", "Licenses"],
        "Software Development": ["Development Tools", "Platform Licenses", "DevOps", "Testing"],
        "Data & Analytics": ["Analytics Platforms", "Data Storage", "BI Tools", "Data Scientists"],
        "Cybersecurity": ["Security Software", "Monitoring Tools", "Security Staff", "Training"],
        "Direct Sales": ["Sales Salaries", "Commissions", "Travel", "CRM Tools"],
        "Digital Marketing": ["Ad Spend", "Content Creation", "SEO Tools", "Social Media"],
        "Brand Management": ["Creative Services", "PR Agencies", "Events", "Sponsorships"],
        "Customer Success": ["Support Staff", "Support Tools", "Training Programs", "Feedback Systems"],
        "Talent Acquisition": ["Recruiting Fees", "Job Boards", "Interview Expenses", "Onboarding"],
        "Employee Development": ["Training Programs", "Conferences", "E-Learning", "Coaching"],
        "Compensation & Benefits": ["Salaries", "Health Insurance", "Retirement Plans", "Bonuses"],
        "HR Operations": ["HRIS Systems", "Payroll Processing", "Employee Relations"],
        "Accounting": ["Audit Fees", "Tax Services", "Financial Software", "Staff Salaries"],
        "Legal & Compliance": ["Legal Fees", "Compliance Software", "Regulatory Filings", "Training"],
        "Business Intelligence": ["BI Platforms", "Analysts", "Reporting Tools", "Data Governance"],
        "Administrative Services": ["Office Management", "Reception", "Mail Services", "Supplies"],
        "Product Research": ["Lab Equipment", "Research Staff", "Materials", "Testing"],
        "Innovation Labs": ["Prototype Development", "Equipment", "Collaboration Tools"],
        "Patents & IP": ["Patent Filings", "Legal Fees", "IP Management", "Licensing"]
    }
    
    for division, div_pct in divisions.items():
        div_value = total_budget * div_pct
        
        hierarchy_data.append({
            "name": division,
            "parent": "Total Budget",
            "value": div_value,
            "level": 1
        })
        
        for subcat, subcat_pct in subcategories[division].items():
            subcat_value = div_value * subcat_pct
            
            hierarchy_data.append({
                "name": subcat,
                "parent": division,
                "value": subcat_value,
                "level": 2
            })
            
            if subcat in detailed_items:
                items = detailed_items[subcat]
                item_weights = np.random.dirichlet(np.ones(len(items)) * 2)
                
                for item, weight in zip(items, item_weights):
                    item_value = subcat_value * weight
                    hierarchy_data.append({
                        "name": item,
                        "parent": subcat,
                        "value": item_value,
                        "level": 3
                    })
    
    hierarchy_data.append({
        "name": "Total Budget",
        "parent": "",
        "value": total_budget,
        "level": 0
    })
    
    df = pd.DataFrame(hierarchy_data)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    generate_hierarchical_data()
    print("Dataset generated successfully!")