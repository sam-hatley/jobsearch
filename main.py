from jobscrape import *
from jobanalysis import *
import datetime
import pandas as pd
import numpy as np

# Create a dictionary to hold the job info
jobs_dict = {
    'Title' : [],
    'Company' : [],
    'Date Posted' : [],
    'Date Retrieved' : [],
    'Link' : []
    }

# start by collecting the queries saved in a text file and specifing the time
job_queries = open('jobs.txt').read().splitlines()
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# For each query, grab a number of job results and append to lists
for query in job_queries:
    index = 1
    while index < 50:
        job_soup = test_page(query, index)
        ext_titles, ext_companies, ext_dates, ext_links = extract_jobs(job_soup)
        
        # Append each entry to the dictionary
        n = 0
        for i in ext_links:
            jobs_dict['Title'].append(ext_titles[n])
            jobs_dict['Company'].append(ext_companies[n])
            jobs_dict['Date Posted'].append(ext_dates[n])
            jobs_dict['Date Retrieved'].append(now)
            jobs_dict['Link'].append(ext_links[n])
            print(ext_titles[n],"::", ext_companies[n])
            n += 1
        
        index += 15

df = jobs_save(jobs_dict)

# Load a numpy array with previous information. If there is none, create it. 
# Check the jobs urls against the urls already in there. If it's there, don't add it.
# Add the jobs that aren't already in the list. Print it all to a .csv.

# How are we going to work with this data?
