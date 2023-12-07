from bs4 import BeautifulSoup
import time, random
from selenium import webdriver

driver = webdriver.Chrome()

# job details
job = 'data'
location = 'Guildford'
domain = 'https://uk.indeed.com'
url = f'{domain}/jobs?q={job}&l={location}&from=searchOnHP'

# open webpage
driver.get(url)

# parse page
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# find job card titles and urls to job spec
job_cards = soup.find_all('h2', class_='jobTitle')
job_page_urls = []

for job_card in job_cards:
    a = job_card.find('a')
    url = f"{domain}{a['href']}"
    job_page_urls.append(url)

# get job titles
titles = []

for url in job_page_urls:
    driver.get(url)
    time.sleep(random.randint(15, 30))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h1')
    titles.append(title.text)
    print(title.text, 'done')