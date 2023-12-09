from bs4 import BeautifulSoup
import time, random, logging, math, os, psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime

log = logging.getLogger()
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=os.environ.get("LOGLEVEL", "INFO"),
    datefmt="%Y-%m-%d %H:%M:%S",
)

options = Options()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

conn = psycopg2.connect("dbname=scraper user=benhurst")
cur = conn.cursor()

search_queries = ["data+engineer", "data+analyst", "software+engineer"]
location = "Guildford"
domain = "https://uk.indeed.com"
age = 7
wait = random.randint(7, 18)
date = datetime.today().strftime("%Y-%m-%d")


def create_table(table_name, columns):
    query = f"""CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"""
    cur.execute(query)
    conn.commit()


def open_webpage(url):
    driver.get(url)
    log.info(f"Connected to {url}")
    log.info(f"Loading page for {wait} seconds")
    time.sleep(wait)
    return driver.page_source


def parse_page(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    log.info(f"Page parsed. Waiting for {wait} seconds")
    time.sleep(wait)
    return soup


# find job card titles and urls to job spec
def process_job_urls(soup):
    job_cards = soup.find_all("a", class_="jcs-JobTitle")
    job_urls = []
    for job_card in job_cards:
        id = job_card["id"].split("_")[1]
        url = f"{domain}/viewjob?jk={id}"
        job_urls.append(url)
    return job_urls


def fetch_text(soup, type: str, element: str, identifier: str):
    if type == "class":
        try:
            item = soup.find(element, class_=identifier).text.replace("'", "''")
        except:
            item = "NULL"
        finally:
            return item
    else:
        try:
            item = soup.find(element, id=identifier).text.replace("'", "''")
        except:
            item = "NULL"
        finally:
            return item


def process_data(soup):
    title = fetch_text(soup, "class", "h1", "jobsearch-JobInfoHeader-title")
    company = fetch_text(soup, "class", "a", "css-1f8zkg3")
    location = fetch_text(soup, "class", "div", "css-6z8o9s")
    salary_and_type = fetch_text(soup, "id", "div", "salaryInfoAndJobType")
    details = fetch_text(soup, "id", "div", "jobDetailsSection")
    description = fetch_text(soup, "id", "div", "jobDescriptionText")

    return {
        "job_title": title,
        "company": company,
        "location": location,
        "salary_and_type": salary_and_type,
        "details": details,
        "description": description,
    }


def insert_data(table_name, columns: list, data: dict, url, search_query):
    query = f"""INSERT INTO {table_name} ({', '.join(columns[1:10])}) VALUES ('{data['job_title']}', '{data['company']}', '{data['location']}', '{data['salary_and_type']}', '{data['details']}', '{data['description']}', '{date}', '{search_query}', '{url}') ON CONFLICT (url) DO NOTHING"""
    cur.execute(query)
    conn.commit()
    return


def main():
    table_name = "raw_indeed_data"
    columns = [
        "id",
        "job_title",
        "company",
        "location",
        "salary_and_type",
        "details",
        "description",
        "date_added",
        "search_term_used",
        "url",
    ]

    create_table(
        f"{table_name}",
        [
            f"{columns[0]} SERIAL PRIMARY KEY",
            f"{columns[1]} TEXT",
            f"{columns[2]} TEXT",
            f"{columns[3]} TEXT",
            f"{columns[4]} TEXT",
            f"{columns[5]} TEXT",
            f"{columns[6]} TEXT",
            f"{columns[7]} DATE",
            f"{columns[8]} TEXT",
            f"{columns[9]} TEXT UNIQUE",
        ],
    )

    for search_query in search_queries:
        page = 0
        pages = 2
        while page < pages:
            search_url = f"{domain}/jobs?q={search_query}&l={location}&sort=date&fromage={age}&start={page * 10}"

            homepage_source = open_webpage(search_url)
            homepage_html = parse_page(homepage_source)

            if page == 0:
                log.info(f"Scrape started.")
                jobs_found = homepage_html.find(
                    "div", class_="jobsearch-JobCountAndSortPane-jobCount"
                ).text.split(" ")[0]
                pages = math.ceil(int(jobs_found) / 15)
                log.info(f"{jobs_found} jobs found across {pages} pages.")

            log.info(f"Starting on page {page + 1} of {pages}")

            job_urls = process_job_urls(homepage_html)
            log.info(f"Found {len(job_urls)} job cards")
            for index, url in enumerate(job_urls):
                log.info(f"Connecting to {index + 1} of {len(job_urls)}.")
                job_page_source = open_webpage(url)
                html = parse_page(job_page_source)
                job_details_dict = process_data(html)
                log.info(
                    f"Retrieved {job_details_dict['job_title']} at {job_details_dict['company']}."
                )
                insert_data(
                    table_name, columns, job_details_dict, url, search_query
                )
                log.info(f"Job inserted")
            log.info(f"Page {page} complete.")

            page += 1

        log.info(f"{search_query} complete.")
    log.info(f"Complete")


main()
