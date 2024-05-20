# dags/scrape_afrik.py
from airflow import DAG # utilisé pour définir le flux de travail
from airflow.operators.python import PythonOperator # utilisé pour exécuter les fonctions pythons
from datetime import datetime, timedelta # utilisé pour manipuler les dates et les heures
from scraper import scrape_afrik, save_to_db # fonction définient dans mon script 'scraper.py'

# définition des arguments
default_args = {
    'owner': 'boris',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# création du DAG
# 1. crée un objet DAG 'scrape_afrik' avec les arguments définient plus hauts
# 2. le flux de travail est planifié pour s'exécuter tous les jours
dag = DAG(
    'scrape_afrik',
    default_args=default_args,
    description='scrape les nouveaux articles de afrik.com et stockes les dans une base de données PostgreSQL',
    schedule_interval=timedelta(days=1),
)

# Définition de la fonction à exécuter
# Cette fonction appelle les fonctions 'scrape_afrik()' et 'save_to_db()'
def scrape_and_store():
    articles = scrape_afrik()
    save_to_db(articles)

# Création de la tache d'exécution
# Cette tâche utilise PythonOperator pour exécuter la fonction scrape_and_store que nous avons définie précédemment
# Le task_id est défini comme 'scrape_afrik', qui correspond également au nom du DAG. 
# Cette tâche est ensuite ajoutée au DAG
scrape_task = PythonOperator(
    task_id='scrape_afrik',
    python_callable=scrape_and_store,
    dag=dag,
)

# Exécution du DAG
scrape_task
