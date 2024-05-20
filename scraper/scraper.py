import requests
from bs4 import BeautifulSoup
import psycopg2
import datetime
import time

# Configuration for the destination PostgreSQL database
db_config = {
    'dbname': 'airflow',
    'user': 'airflow',
    'password': 'airflow',
    'host': 'postgres', # nom du service défini dans le fichier docker-compose
    'port': 5432
}

# Constantes pour les tentatives et les délais d'attente
MAX_RETRIES = 5
RETRY_DELAY = 5

# Script SQL pour créer la table 'articles'
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    link TEXT NOT NULL,
    description TEXT,
    image_url TEXT,
    date TIMESTAMP
);
"""

def execute_sql(sql):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            print(f"SQL script executed successfully.")
            return
        except psycopg2.OperationalError as e:
            print(f"Error connecting to PostgreSQL database: {e}")
            retries += 1
            if retries < MAX_RETRIES:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print("Could not connect to the PostgreSQL database after several retries.")
                raise Exception("Could not connect to the PostgreSQL database after several retries")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error executing SQL script: {error}")
            if conn:
                cursor.close()
                conn.close()
            raise

def scrape_afrik():
    url = 'https://www.afrik.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Trouver tous les articles
    articles = soup.find_all('div', {'class': 'td_module_mob_1 td_module_wrap td-animation-stack td-meta-info-hide'})

    # Initialiser un dictionnaire pour stocker les informations de l'article
    article_info = {}

    # Extraire les informations du dernier article publié s'il existe
    if articles:
        latest_article = articles[0]
        link = latest_article.find('a', class_='td-image-wrap')['href']
        image_url = latest_article.find('img', class_='entry-thumb')['src']
        title = latest_article.find('h1', class_='entry-title td-module-title').get_text(strip=True)
        description = latest_article.find('div', class_='td-excerpt').get_text(strip=True)
        
        # Stocker ces informations dans le dictionnaire
        article_info = {
            'link': link,
            'image_url': image_url,
            'title': title,
            'description': description,
            'date': datetime.datetime.now()
        }
    else:
        print("Aucun article trouvé")
    
    return article_info

def save_to_db(article):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()
            print("Connexion à la base de donnée réussie ...")

            # Insertion de l'article dans la base de données
            cursor.execute(
                "INSERT INTO articles (title, link, description, image_url, date) VALUES (%s, %s, %s, %s, %s)",
                (article['title'], article['link'], article['description'], article['image_url'], article['date'])
            )

            # Validation des modifications et fermeture de la connexion
            conn.commit()
            cursor.close()
            conn.close()
            print("L'article a été enregistré avec succès dans la base de données.")
            return
        except psycopg2.OperationalError as e:
            print(f"Error connecting to PostgreSQL database: {e}")
            retries += 1
            if retries < MAX_RETRIES:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print("Could not connect to the PostgreSQL database after several retries.")
                raise Exception("Could not connect to the PostgreSQL database after several retries")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur lors de l'enregistrement de l'article dans la base de données:", error)
            if conn:
                cursor.close()
                conn.close()
            raise

if __name__ == "__main__":
    # Exécute le script SQL pour créer la table 'articles'
    execute_sql(CREATE_TABLE_SQL)

    # Scraping des informations sur l'article
    article = scrape_afrik()
    if article:
        save_to_db(article)
    else:
        print("Aucun article trouvé, aucun enregistrement n'a été effectué.")
