import urllib
import cloudscraper
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


def scrape_jobs(query, page, location = ''):
    '''Returns a (souped) page from indeed. Takes a job title query string and starting result number.'''

    # Create the URL from the query
    url_vars = {'q' : query,'l' : location, 'sort' : 'date', 'start' : page}
    url = ('https://uk.indeed.com/jobs?' + urllib.parse.urlencode(url_vars))
    
    # Get the page from the URL with cloudscraper to bypass cloudflare security
    scraper = cloudscraper.create_scraper()
    page = scraper.get(url)
    
    # Convert the page to soup and return soup
    soup = BeautifulSoup(page.content, "html.parser")
    return soup
    

def test_page(*args):
    '''Returns a saved local page for testing'''

    # Open a previously scraped html file, convert to soup and return
    with open('jobpage.html') as jp:
        soup = BeautifulSoup(jp, 'html.parser')
        return soup


def extract_jobs(soup):
    '''Takes a soup input and extracts job information. Returns
    four lists: titles, companies, dates, links.'''

    # We'll store the data in lists
    titles = []
    companies = []
    dates = []
    links = []

    # Indeed separates job listings in "JobCards". We'll start by pulling these out.
    jobcards = soup.find_all('div', class_='cardOutline')

    # The next step is to iterate through each jobcard and pull the information we need.
    for job in jobcards:
        title_elem = job.find('h2', class_='jobTitle')
        company_elem = job.find('span', class_='companyName')
        date_elem = job.find('span', class_='date')
        link_elem = job.find('a').get("data-jk")

        # Cleaning the elements to get what we need
        title = title_elem.get_text()
        company = company_elem.get_text()
        # Removing an extra 'Posted' in some date entries
        for span in date_elem.findAll('span', class_="visually-hidden"):
            span.replace_with('')
        date = date_elem.get_text()
        # Rebuilding the link with an ID fetched earlier
        link = 'https://uk.indeed.com/viewjob?jk=' + link_elem

        # Append the values to their lists
        titles.append(title)
        companies.append(company)
        dates.append(date)
        links.append(link)
    
    return titles, companies, dates, links

def jobs_save(jobs_dict):
    exit()
