# Dockerfile
FROM apache/airflow:2.2.3

USER root
RUN apt-get update && apt-get install -y python3-dev libpq-dev

USER airflow
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY dags/ /opt/airflow/dags/
