from bs4 import BeautifulSoup
import time, random, undetected_chromedriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging
import os

#logging
log = logging.getLogger()
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

#selenium
options = Options()
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--headless")
driver = undetected_chromedriver.Chrome(options=options)


location = 'guildford'
search_url = f'https://www.zoopla.co.uk/for-sale/property/{location}/'

def open_webpage(url):

    wait = random.randint(15, 30)

    driver.get(url)
    log.info(f'Connected.')
    
    log.info(f'Loading page for {wait} seconds')
    time.sleep(wait)
    return driver.page_source

html = open_webpage(search_url)
with open('out.txt', 'w') as f:
    f.write(html)