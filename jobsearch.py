import urllib
import cloudscraper
from bs4 import BeautifulSoup
import random


def select_agent():
    '''Randomly selects a useragent from a list of 28'''

    with open('useragent.txt', 'r') as ua:
        lines = ua.readlines()
        return random.choice(lines).strip()


def get_page(query, page):
    '''Returns a page from indeed'''

    # Create the URL from the query
    url_vars = {'q' : query,'l' : 'London', 'sort' : 'date', 'start' : page}
    url = ('https://uk.indeed.com/jobs?' + urllib.parse.urlencode(url_vars))
    debug_url = "https://webscraper.io/test-sites/e-commerce/allinone"
    
    # Get the page from the URL with cloudscraper to bypass cloudflare security
    scraper = cloudscraper.create_scraper()
    page = scraper.get(url)
    
    # Convert the page to soup
    soup = BeautifulSoup(page.content, "html.parser")
    return soup
    

def local_page():
    '''Uses a saved local page for testing'''

    with open('jobpage.html') as jp:
        soup = BeautifulSoup(jp, 'html.parser')
        return soup


def scrape_jobs(page):
    '''Takes a soup input and extracts the posting date, job title, company, description, and link'''
    # Each page has 15 jobs, we'll need to run through all of them.
    job_elems = page.find_all('div', class_='jobsearch-SerpJobCard')
    for je in job_elems:
        print(je)


page = local_page()
scrape_jobs(page)