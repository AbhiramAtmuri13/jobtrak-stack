import os
import requests
import psycopg2
import json
from datetime import datetime

def fetch_and_store_jobs():
    APP_ID = os.getenv("ADZUNA_APP_ID")
    APP_KEY = os.getenv("ADZUNA_APP_KEY")
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={APP_ID}&app_key={APP_KEY}&results_per_page=10"

    response = requests.get(url)
    data = response.json()

    conn = psycopg2.connect(
        dbname="airflow_db",
        user="postgres",
        password="mystrongpass",  # Replace with your actual password
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    for job in data.get("results", []):
        job_id = str(job.get("id"))
        payload = job
        try:
            cursor.execute(
                """
                INSERT INTO jobs_raw (id, api_time, payload)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (job_id, datetime.utcnow(), json.dumps(payload))
            )
        except Exception as e:
            print(f"Failed to insert job {job_id}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Job data fetched and inserted successfully!")

