import json
import os
import requests
import psycopg2
from datetime import datetime, timezone

# Load API credentials from environment variables
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
    raise ValueError("Missing Adzuna credentials. Set ADZUNA_APP_ID and ADZUNA_APP_KEY.")

# API endpoint
API_URL = f"https://api.adzuna.com/v1/api/jobs/in/search/1"
PARAMS = {
    "app_id": ADZUNA_APP_ID,
    "app_key": ADZUNA_APP_KEY,
    "results_per_page": 10,
    "what": "data engineer",   # You can change this search keyword
    "content-type": "application/json"
}

# Fetch job data
response = requests.get(API_URL, params=PARAMS)
data = response.json()

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="airflow_db",
    user="postgres",
    password="mystrongpass",  # Use the password you set earlier
    host="localhost"
)
cursor = conn.cursor()

# Insert jobs into jobs_raw table
for job in data.get("results", []):
    job_id = job.get("id")
    payload = job

    try:
        cursor.execute(
            """
            INSERT INTO jobs_raw (id, api_time, payload)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """,
            (job_id, datetime.now(timezone.utc), json.dumps(payload))
        )
    except Exception as e:
        print(f"Failed to insert job {job_id}: {e}")

conn.commit()
cursor.close()
conn.close()

print("✅ Job data fetched and inserted successfully!")

