import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

# SETTINGS
ROWS = 1000
START_DATE = datetime(2024, 4, 16)
END_DATE = datetime(2026, 4, 16)
REGIONS = ["North America", "South America", "Europe", "UK", "India", "APAC", "Middle East", "Africa"]
SKILLS = ["Data Analytics", "Data Engineering", "Power BI", "SQL", "Python", "Azure", "AWS", "ETL", "Snowflake", "Tableau"]
INDUSTRIES = ["FinTech", "Healthcare", "Retail", "SaaS", "Manufacturing", "Telecom", "Banking", "Logistics"]

def rand_date():
    return START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days))

# DIMENSIONS
recruiters = pd.DataFrame({
    "recruiter_id": range(1, 26),
    "recruiter_name": [fake.name() for _ in range(25)],
    "region": [random.choice(REGIONS) for _ in range(25)]
})

clients = pd.DataFrame({
    "client_id": range(1, 51),
    "client_name": [fake.company() for _ in range(50)],
    "industry": [random.choice(INDUSTRIES) for _ in range(50)],
    "region": [random.choice(REGIONS) for _ in range(50)]
})

roles = pd.DataFrame({
    "role_id": range(1, 61),
    "role_title": [random.choice(["Data Analyst", "Data Engineer", "BI Analyst", "Analytics Engineer", "ETL Developer"]) for _ in range(60)],
    "primary_skill": [random.choice(SKILLS) for _ in range(60)],
    "priority": [random.choice(["High", "Medium", "Low"]) for _ in range(60)]
})

candidates = pd.DataFrame({
    "candidate_id": range(1, 301),
    "candidate_name": [fake.name() for _ in range(300)],
    "years_experience": [random.randint(1, 12) for _ in range(300)],
    "primary_skill": [random.choice(SKILLS) for _ in range(300)],
    "region": [random.choice(REGIONS) for _ in range(300)]
})

# FACTS
applications = []
for i in range(1, ROWS+1):
    app_date = rand_date()
    applications.append({
        "application_id": i,
        "candidate_id": random.choice(candidates["candidate_id"].tolist()),
        "client_id": random.choice(clients["client_id"].tolist()),
        "role_id": random.choice(roles["role_id"].tolist()),
        "recruiter_id": random.choice(recruiters["recruiter_id"].tolist()),
        "application_date": app_date.strftime("%Y-%m-%d"),
        "status": random.choice(["Applied", "Interviewing", "Offered", "Rejected", "Hired"])
    })
applications = pd.DataFrame(applications)

interviews = []
for i in range(1, int(ROWS*0.6)+1):
    app = applications.sample(1).iloc[0]
    interviews.append({
        "interview_id": i,
        "application_id": app["application_id"],
        "interview_date": (pd.to_datetime(app["application_date"]) + pd.Timedelta(days=random.randint(2, 20))).strftime("%Y-%m-%d"),
        "interview_stage": random.choice(["Screen", "Technical", "Client", "Final"]),
        "result": random.choice(["Pass", "Fail"])
    })
interviews = pd.DataFrame(interviews)

offers = []
for i in range(1, int(ROWS*0.35)+1):
    app = applications.sample(1).iloc[0]
    offer_date = pd.to_datetime(app["application_date"]) + pd.Timedelta(days=random.randint(10, 35))
    offers.append({
        "offer_id": i,
        "application_id": app["application_id"],
        "offer_date": offer_date.strftime("%Y-%m-%d"),
        "salary_usd": random.randint(45000, 140000),
        "offer_status": random.choice(["Accepted", "Declined", "Pending"])
    })
offers = pd.DataFrame(offers)

placements = []
for i in range(1, int(ROWS*0.25)+1):
    app = applications.sample(1).iloc[0]
    start_date = pd.to_datetime(app["application_date"]) + pd.Timedelta(days=random.randint(20, 60))
    placements.append({
        "placement_id": i,
        "application_id": app["application_id"],
        "start_date": start_date.strftime("%Y-%m-%d"),
        "bill_rate_usd": random.randint(35, 120),
        "employment_type": random.choice(["Contract", "Full-time"])
    })
placements = pd.DataFrame(placements)

timesheets = []
for i in range(1, int(ROWS*0.8)+1):
    placement = placements.sample(1).iloc[0]
    week_start = rand_date()
    timesheets.append({
        "timesheet_id": i,
        "placement_id": placement["placement_id"],
        "week_start_date": week_start.strftime("%Y-%m-%d"),
        "billable_hours": random.choice([20, 30, 35, 40]),
        "non_billable_hours": random.choice([0, 2, 5, 10])
    })
timesheets = pd.DataFrame(timesheets)

# DATE DIM
dates = pd.date_range(start=START_DATE, end=END_DATE)
dim_date = pd.DataFrame({
    "date": dates,
    "year": dates.year,
    "quarter": dates.quarter,
    "month": dates.month,
    "month_name": dates.strftime("%B"),
    "week": dates.isocalendar().week
})

# SAVE CSVs
recruiters.to_csv("recruiters.csv", index=False)
clients.to_csv("clients.csv", index=False)
roles.to_csv("roles.csv", index=False)
candidates.to_csv("candidates.csv", index=False)
applications.to_csv("applications.csv", index=False)
interviews.to_csv("interviews.csv", index=False)
offers.to_csv("offers.csv", index=False)
placements.to_csv("placements.csv", index=False)
timesheets.to_csv("timesheets.csv", index=False)
dim_date.to_csv("dates.csv", index=False)

print("CSVs generated.")
