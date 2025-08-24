# Dockerized Stock Data Pipeline

This project uses **Apache Airflow** to automatically fetch stock prices every day from the **Alpha Vantage API**, clean them, and save them into a **PostgreSQL database**.

---

## Files & Folders
- `docker-compose.yml` → defines services for Airflow & PostgreSQL  
- `.env` → environment variables (API key & DB credentials)  
- `airflow/dags/stock_dag.py` → DAG for scheduling stock fetching  
- `airflow/scripts/fetch_data.py` → script to fetch data from API and insert into DB  
- `requirements.txt` → Python dependencies  
- `Dockerfile` → build custom Airflow image  

---

## Setup Instructions
1. Clone this repo and go inside:
   ```bash
   git clone <repo_url>
   cd dockerized_stock_data
2. Fill your Alpha Vantage API key:
   ```bash
   cp .env .env
Then edit ```.env``` and set:
   ```bash
   API_KEY=your_api_key_here
   ```
3. Build and start services
   ```bash
   docker-compose up --build
   ```

This will:
- Start PostgreSQL on port ```5432```
- Start Airflow Webserver on port 8080 (http://localhost:8080)
   - Username: ```admin``` | Password: ```admin```
- Enable and trigger the DAG ```stock_data_pipeline``` in Airflow UI.
---

### Check Data
To open a psql shell inside the Postgres container:
```bash
docker exec -it postgres psql -U postgres -d stocks
```
Run query:
```sql
SELECT * FROM stock_data;
```
