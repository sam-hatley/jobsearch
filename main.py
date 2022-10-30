from jobsearch import *
import pandas as pd

page = test_page()
titles, companies, dates, links = extract_jobs(page)

print(titles)