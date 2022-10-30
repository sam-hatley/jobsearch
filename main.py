from jobsearch import *
import datetime
import pandas as pd
import numpy as np

# Here: build a program that iterates through extract_jobs as required for the
# number of jobs and job titles to fetch

# Need to do something with the data output: thinking we build it into a dataframe, which
# keeps a record of jobs (by link?), and does not save jobs that have been seen before.

# This program will be fairly simple: build a list of pages and queries to get. Get the results
# from those. Append to a list that will be saved in some kind of format, if they aren't already
# on that list. This will absolutely need to connect/disconnect from the VPN!

# If we can build some kind of interface to look through jobs, mark those that've been
# applied to, etc, that would be best. Total automation is possible, but will take quite
# a bit more work!

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
print(now)

# For each query, grab a number of job results and append to lists
for query in job_queries:
    index = 1
    while index < 10:
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
            n += 1
        
        index += 15

# Load a numpy array with previous information. If there is none, create it. 
# Check the jobs urls against the urls already in there. If it's there, don't add it.
# Add the jobs that aren't already in the list. Print it all to a .csv.

# How are we going to work with this data?

jobs_df = pd.DataFrame(jobs_dict)
jobs_df.to_parquet('jobs.parquet')