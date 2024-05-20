# dags/scrape_afrik.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scraper import scrape_afrik, save_to_db

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'scrape_afrik',
    default_args=default_args,
    description='Scrape afrik.com and store in PostgreSQL',
    schedule_interval=timedelta(days=1),
)

def scrape_and_store():
    articles = scrape_afrik()
    save_to_db(articles)

scrape_task = PythonOperator(
    task_id='scrape_afrik',
    python_callable=scrape_and_store,
    dag=dag,
)

scrape_task
