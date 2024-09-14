import requests
from bs4 import BeautifulSoup
import threading
import time
import logging

# configuring logging
logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Scrapping function
def scrap():
    while True:
        try:
            response = requests.get("https://news.ycombinator.com/news", timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extracting titles and links
            for item in soup.find_all(class_='storylink'):
                try:
                    title = item.find('a', class_='storylink').text
                    link = item.find('a', class_='storylink')['href']
                    logging.info(f'Title: {title} | Link: {link}')
                except Exception as e:
                    logging.error("Error extracting the desired data")
        # Handling exceptions
        except requests.exceptions.RequestException as e:
            logging.error("error in requests")
            #scrapping every hour
            logging.info("Waiting for next cycle")
            time.sleep(3600)

# Starting the scrapper
def start_scrapper():
    logging.info("Starting the scrapper")
    t = threading.Thread(target=scrap)
    t.start()