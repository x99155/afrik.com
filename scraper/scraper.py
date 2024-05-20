# scraper.py
import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2.extras import execute_values
import datetime

def scrape_afrik():
    url = 'https://www.afrik.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for article in soup.find_all('article'):
        title = article.find('h2').text.strip()
        link = article.find('a')['href']
        date = datetime.datetime.now()
        
        articles.append((title, link, date))
    
    return articles

def save_to_db(articles):
    conn = psycopg2.connect(
        dbname="afrikdb", 
        user="postgres", 
        password="juana", 
        host="localhost"
    )
    cursor = conn.cursor()
    execute_values(cursor, "INSERT INTO articles (title, link, date) VALUES %s", articles)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    articles = scrape_afrik()
    save_to_db(articles)
