import urllib
import cloudscraper
from bs4 import BeautifulSoup
import datetime
from time import sleep
from random import randint


def scrape_joblist(query, page, location = ''):
    '''Returns a (souped) page from indeed. Takes a job query string and 
    starting number.'''

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
    '''Takes a soup input and extracts job information. Returns four lists: 
    "titles", "companies", "dates", and "links".'''

    date_now = datetime.datetime.now()

    # We'll store the data in lists
    titles = []
    companies = []
    dates = []
    links = []

    # Indeed separates job listings in "JobCards". We'll start by pulling these
    # out.
    jobcards = soup.find_all('div', class_='cardOutline')

    # The next step is to iterate through each jobcard and pull the information
    # we need.
    for jobcard in jobcards:
        title_elem = jobcard.find('h2', class_='jobTitle')
        company_elem = jobcard.find('span', class_='companyName')
        date_elem = jobcard.find('span', class_='date')
        link_elem = jobcard.find('a').get("data-jk")

        # Cleaning the elements to get what we need
        title = title_elem.get_text()
        company = company_elem.get_text()

        # Removing an extra 'Posted' in some date entries
        for span in date_elem.findAll('span', class_="visually-hidden"):
            span.replace_with('')
        
        # Converting the posted date into a usable format now
        date_extr = date_elem.get_text().lower()
        print(date_extr)

        # Anything 'just posted' or 'today' will get timestamped for today
        if date_extr == 'just posted' or date_extr == 'today':
            date = date_now
            date = date.strftime("%Y-%m-%d")

        # 'hiring ongoing' means it's been there for a while: we'll use 30 days
        elif date_extr == 'hiring ongoing':
            date = date_now - datetime.timedelta(30)
            date = date.strftime("%Y-%m-%d")

        # If it's anything else, it's either in the format 'posted {n} days ago'
        # or something we haven't seen before. Converting date to a list,
        # checking to see if it's expected, and saving.
        else:
            date_list = date_extr.split()
            if date_list[0] == 'posted':
                # This will generally fail if the posting was "30+" days ago.
                if not date_list[1].isdigit():
                    date = date_now - datetime.timedelta(30)
                    date = date.strftime("%Y-%m-%d")
                else:
                    date = date_now - datetime.timedelta(int(date_list[1]))
                    date = date.strftime("%Y-%m-%d")
            else:
                date = ''


        # Rebuilding the link with an ID fetched earlier
        link = 'https://uk.indeed.com/viewjob?jk=' + link_elem

        # Append the values to their lists
        titles.append(title)
        companies.append(company)
        dates.append(date)
        links.append(link)
    
    return titles, companies, dates, links


def job_search(job_queries: list, results = 45, test = 0):
    '''Takes a list of job queries and a number of desired results for each.
    Returns a dictionary of results with the keys "Title", "Company", "Date
    Posted", "Date Retrieved", "Link", and "Select" (empty). Waits a 1-5 
    seconds between individual queries and half a second within.'''

    date_now = datetime.datetime.now().strftime("%Y-%m-%d")
    time_now = datetime.datetime.now().strftime("%H:%M:%S")

    # Create a dictionary to hold the job info
    jobs_dict = {
        'Title' : [],
        'Company' : [],
        'Date Posted' : [],
        'Date Retrieved' : [],
        'Time Retrieved' : [],
        'Link' : [],
        'Select' : []
        }

    # For each query, grab a number of job results and append to lists
    for query in job_queries:
        index = 1
        while index < results:
            print(f"Retrieving results {index}-{index+14} for {query}")
            # use test_page() for testing, scrape_joblist() for production
            if test == 1:
                job_soup = test_page()
            else:
                job_soup = scrape_joblist(query, index)
            
            ext_titles, ext_companies, ext_dates, ext_links = extract_jobs(job_soup)
            
            # Append each entry to the dictionary
            n = 0
            for i in ext_links:
                jobs_dict['Title'].append(ext_titles[n])
                jobs_dict['Company'].append(ext_companies[n])
                jobs_dict['Date Posted'].append(ext_dates[n])
                jobs_dict['Date Retrieved'].append(date_now)
                jobs_dict['Time Retrieved'].append(time_now)
                jobs_dict['Link'].append(ext_links[n])
                jobs_dict['Select'].append('')
                n += 1
            index += n
            sleep(0.5)

        # Wait between queries, unless it's the last query
        if query != job_queries[-1]:
            rand = randint(1,5)
            print(f'Waiting {rand} seconds')
            sleep(rand)
    
    return jobs_dict