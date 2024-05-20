# scraper.py
import requests
from bs4 import BeautifulSoup
import psycopg2
import datetime
import config


def scrape_afrik():
    url = 'https://www.afrik.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

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
    try:
        # Connexion à la base de données PostgreSQL en utilisant les informations de configuration
        conn = psycopg2.connect(**config.load_config)
        cursor = conn.cursor()

        # Insertion de l'article dans la base de données
        cursor.execute("INSERT INTO articles (title, link, description, image_url, date) VALUES (%s, %s, %s, %s, %s)", 
                       (article['title'], article['link'], article['description'], article['image_url'], article['date']))

        # Validation des modifications et fermeture de la connexion
        conn.commit()
        cursor.close()
        conn.close()
        print("L'article a été enregistré avec succès dans la base de données.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erreur lors de l'enregistrement de l'article dans la base de données:", error)


if __name__ == "__main__":
    article = scrape_afrik()
    if article:
        save_to_db(article)
    else:
        print("Aucun article trouvé, aucun enregistrement n'a été effectué.")
