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
