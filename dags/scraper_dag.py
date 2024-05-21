from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': datetime(2024, 5, 21),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Cette fonction exécute le script scraper.py
def run_scraper():
    script_path = "/opt/airflow/scraper/scraper.py"
    result = subprocess.run(["python", script_path],
                            capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"L'exécution du script a échoué avec l'erreur: {result.stderr}")
    else:
        print(result.stdout)


# Crée un objet DAG 'scrape' avec les arguments définient plus hauts
# Le flux de travail est planifié pour s'exécuter tous les jours
dag = DAG(
    'scraper',
    default_args=default_args,
    description='scrape les nouveaux articles de afrik.com et stockes les dans une base de données PostgreSQL',
    schedule_interval=timedelta(days=1),
    catchup=False
)

# Création de la tache d'exécution
# Cette tâche utilise PythonOperator pour exécuter la fonction 'run_scraoer()' que nous avons définie précédemment
# Cette tâche est ensuite ajoutée au DAG
scrape_task = PythonOperator(
    task_id="run_scraper",
    python_callable=run_scraper,
    dag=dag
)

# Exécution du DAG
scrape_task