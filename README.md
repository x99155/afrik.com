# Afrik.com Scraper Project

Ce projet scrape les nouveaux articles de afrik.com et les stocke dans une base de données PostgreSQL, automatisé avec Apache Airflow et Docker.

## Prérequis

- Docker
- Docker Compose

## Structure du projet

- `dags/`: Contient les DAGs d'Airflow.
- `scraper/`: Contient le script de scraping.
- `requirements.txt`: Dépendances Python.
- `Dockerfile`: Image Docker pour Airflow.
- `docker-compose.yml`: Configuration Docker Compose.
- `README.md`: Instructions et informations sur le projet.

## Instructions

1. Clonez le dépôt.
2. Naviguez dans le répertoire du projet.
3. Créez et démarrez les conteneurs Docker:
4. 

    ```bash
    docker compose up init-airflow -d
    docker compose up
    ```

4. Accédez à l'interface web d'Airflow sur `http://localhost:8080` et activez le DAG `scraper`.

5. Accédez à la base de donnée:
- docker exec -it <nom du conteneur postgres> psql -U airflow : se connecter avec à l'utilisateur airflow
- \c airflow : pour se connecter à la bdd airflow
- \dt: liste les bdd
- vous devriez voir la table 'articles'
- select * from articles; pour voir qu'elle contient bien les data scraper sur le site afrik.com (le dernier article publié)

