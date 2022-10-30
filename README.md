Goals here:

1. [vpn.py](vpn.py) will provide an interface for the program to get a random ip
2. [jobsearch.py](jobsearch.py) will scrape indeed for jobs according to our criteria, and print these to a list
3. [jobparser.py]

Notes from main:

Here: build a program that iterates through extract_jobs as required for the number of jobs and job titles to fetch

Need to do something with the data output: thinking we build it into a dataframe, which keeps a record of jobs (by link?), and does not save jobs that have been seen before.

This program will be fairly simple: build a list of pages and queries to get. Get the results from those. Append to a list that will be saved in some kind of format, if they aren't already on that list. This will absolutely need to connect/disconnect from the VPN!

If we can build some kind of interface to look through jobs, mark those that've been applied to, etc, that would be best. Total automation is possible, but will take quite a bit more work!


jobs.txt holds job queries, which is read by main.py. main.py iterates through each of the lines in jobs.txt and grabs the first 50 results by date.