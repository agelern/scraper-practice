import requests
from bs4 import BeautifulSoup


page_to_visit = ''
URL = f"http://books.toscrape.com/"


def get_homepage():
    homepage = 'index.html'
    page_to_visit = homepage
    page = requests.get(URL + page_to_visit)
    return page

def get_book_links(soup):
    list_of_links = []
    elements = soup.find_all('a', href=True)
    for link in elements:
        if link['href'].startswith('catalogue/category/'):
            continue
        else:
            page_to_visit = link['href']
            list_of_links.append(URL + page_to_visit)
    return list_of_links

def get_book_content(links):
    for page in links:
    
soup = BeautifulSoup(get_homepage().content, 'html.parser')
links = get_book_links(soup)
