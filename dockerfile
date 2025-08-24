# Use official Apache Airflow image as base
FROM apache/airflow:2.6.2
# Switch to root user to install system dependencies
USER root
# Install PostgreSQL client libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev build-essential && \
    rm -rf /var/lib/apt/lists/*
# Switch back to airflow user
USER airflow
# Install Python dependencies for data pipeline
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy pipeline scripts into container
COPY airflow/dags/ /opt/airflow/dags/
COPY airflow/scripts/ /opt/airflow/scripts/
