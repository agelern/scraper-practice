from bs4 import BeautifulSoup
import time, random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging
import os
import psycopg2

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
driver = webdriver.Chrome(options=options)

#psycopg2
conn = psycopg2.connect("dbname=scraper user=benhurst")
cur = conn.cursor()



# job details
job = 'software'
location = 'Guildford'
domain = 'https://uk.indeed.com'
url = f'{domain}/jobs?q={job}&l={location}&from=searchOnHP'
log.info(f'Scrape started. About to try {url}')

# open webpage
driver.get(url)
log.info(f'Connected.')
wait = random.randint(15, 30)
log.info(f'Loading page for {wait} seconds')
time.sleep(wait)

# parse page
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
wait = random.randint(15, 30)
log.info(f'Homepage parsed. Waiting for {wait} seconds')
time.sleep(wait)

# find job card titles and urls to job spec
job_cards = soup.find_all('h2', class_='jobTitle')
job_page_urls = []
for job_card in job_cards:
    a = job_card.find('a')
    url = f"{domain}{a['href']}"
    log.info(url[:100])
    job_page_urls.append(url)
log.info(f'Found {len(job_page_urls)} job cards')

# get job titles
titles = []

for url in job_page_urls:
    # connect to page
    log.info(f'about to try connect {url[:100]}')
    driver.get(url)
    wait = random.randint(15, 30)
    time.sleep(wait)
    log.info(f'Connected. Now waiting for {wait} seconds')

    # parse page
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    log.info(f'Parsed the page')

    # find elements and store
    title = soup.find('h1')
    titles.append(title.text)
    log.info(f'{title.text} done')
log.info('Scrape complete.')