import requests
from bs4 import BeautifulSoup
import threading

def scrap():
    while True:
        response = requests.get("https://news.ycombinator.com/news")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting titles and links
        for title in soup.find_all(class_='title'):
            pass
        #scrapping very hour
        time.sleep(3600)

def start_scrapper():
    t = threading.Thread(target=scrap)
    t.start()