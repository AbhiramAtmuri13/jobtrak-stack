# JobTrak – Real-Time Job Postings Pipeline

JobTrak is a real-time data engineering pipeline that fetches job postings using the Adzuna API and stores them in PostgreSQL via Apache Airflow DAGs. This project demonstrates ETL orchestration, API integration, and workflow automation in a modern data stack.

## 🔧 Tech Stack

- **Python 3.12**
- **PostgreSQL**
- **Apache Airflow**
- **Adzuna Job Search API**
- **Ubuntu (WSL 2)**
- **psycopg2 (PostgreSQL driver)**
- **Git & GitHub**

## 📦 Features

- Fetches fresh job listings from the Adzuna API
- Inserts raw JSON payloads into a PostgreSQL table (`jobs_raw`)
- Uses Airflow DAGs for scheduled ETL orchestration
- Logs task runs and supports retry logic
- Can be extended to process, transform, and visualize job trends

## 🏗️ Architecture

+--------------+ +-------------+ +--------------+
| Adzuna API + --> | Airflow DAG + --> | PostgreSQL DB |
+--------------+ +-------------+ +--------------+
|
v
+------------------+
| Python ETL Code |
+------------------+


## 🚀 How to Run

### 1. Clone this repo:

```bash
git clone https://github.com/AbhiramAtmuri13/jobtrak-stack.git
cd jobtrak-stack

### 2. Set up environment:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 3. Export API credentials (or add to .env)

export ADZUNA_APP_ID="your_app_id"
export ADZUNA_APP_KEY="your_app_key"

### 4. 4. Create the PostgreSQL table:

CREATE TABLE IF NOT EXISTS jobs_raw (
    id         TEXT PRIMARY KEY,
    api_time   TIMESTAMPTZ DEFAULT now(),
    payload    JSONB
);

### 5. Run Airflow:

airflow db migrate
airflow scheduler
airflow webserver --port 8080
Visit http://localhost:8080 to access the Airflow UI.

## 🛠️ Future Improvements

Data transformation and cleaning DAG
Dashboards with PowerBI or Streamlit
Integration with resume/job matching ML models

##👨‍💻 Author
Abhiram Atmuri
GitHub – AbhiramAtmuri13
