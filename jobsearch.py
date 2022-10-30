import urllib
import cloudscraper
from bs4 import BeautifulSoup
import random

from pendulum import date


def select_agent():
    '''Randomly selects a useragent from a list of 28'''

    # Read a list of user agents and randomly select one line from the list
    with open('useragent.txt', 'r') as ua:
        lines = ua.readlines()
        return random.choice(lines).strip()


def scrape_jobs(query, page, location = ''):
    '''Returns a page from indeed. Takes a job title query string and starting result number.'''
    # Will need to do something regarding the location here: set to London for testing.

    # Create the URL from the query
    url_vars = {'q' : query,'l' : location, 'sort' : 'date', 'start' : page}
    url = ('https://uk.indeed.com/jobs?' + urllib.parse.urlencode(url_vars))
    
    # Get the page from the URL with cloudscraper to bypass cloudflare security
    scraper = cloudscraper.create_scraper()
    page = scraper.get(url)
    
    # Convert the page to soup and return soup
    soup = BeautifulSoup(page.content, "html.parser")
    return soup
    

def local_page():
    '''Uses a saved local page for testing'''

    # Open a previously scraped html file, convert to soup and return
    with open('jobpage.html') as jp:
        soup = BeautifulSoup(jp, 'html.parser')
        return soup


def extract_jobs(soup):
    '''Takes a soup input and extracts the posting date, 
    job title, company, description, and link'''

    # Indeed separates job listings in "JobCards". We'll start by pulling these out.
    jobcards = soup.find_all('div', class_='cardOutline')

    # The next step is to iterate through each jobcard and pull the information we need.
    for job in jobcards:
        # There's an odd bug with date: there's a span class="visually-hidden"
        # within "date" that adds an additional "posted". Need to strip it somehow.

        # We're getting the elements at this point, including a bunch of html data that
        # we can strip off later. To get the link, we'll need to fetch one of indeed's
        # identifiers to rebuild the link later.
        title_elem = job.find('h2', class_='jobTitle')
        company_elem = job.find('span', class_='companyName')
        date_elem = job.find('span', class_='date')
        link_elem = job.find('a').get("data-jk")

        # Cleaning the elements to get what we need
        title = title_elem.get_text()
        company = company_elem.get_text()
        for span in date_elem.findAll('span', class_="visually-hidden"):
            span.replace_with('')
        date = date_elem.get_text()
        link = 'https://uk.indeed.com/viewjob?jk=' + link_elem

        print(title)
        print(company)
        print(date)
        print(link)
        print("\n")

page = scrape_jobs("product manager", 1)
extract_jobs(page)