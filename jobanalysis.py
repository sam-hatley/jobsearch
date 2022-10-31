import os.path
import pandas as pd


def jobs_save(dict, keep="last"):
    '''Checks job links against previously fetched jobs, and saves new entries
    to file. Takes a dictionary which must have the key "Link" and returns a
    dataframe of all jobs'''

    new_jobs_df = pd.DataFrame(dict)

    # Check if file exists
    if os.path.isfile('joblist.pkl'):
        old_jobs_df = pd.read_pickle('joblist.pkl')
        df = pd.concat([new_jobs_df, old_jobs_df])
        # Remove any entry with the same link
        df = df.drop_duplicates(subset="Link", keep=keep)
    else:
        df = new_jobs_df

    df.to_pickle('joblist.pkl')
    df.to_csv('joblist.csv')

    return df


def jobs_load():
    df = pd.read_pickle('joblist.pkl')
    return df


def job_info(arg):
    '''Takes a link and extracts (info) from a job posting'''


def jobs_sort(df, date):
    '''Iterates through jobs in a dataframe from a specified date. User input 
    flags selects, returns a dataframe of selected jobs. Date should be in the 
    format "YYYY-MM-DD".'''

    df = df[(df['Date Posted'] == date)]

    # Filter out some words
    filters = [
        'senior',
        'data entry',
        'c\+\+',
        'trading',
        'receptionist',
        'Executive Assistant',
    ]
    filter = '|'.join(filters)
    df = df[~df['Title'].str.contains(filter, case=False)]


    # Date posted: want to convert to a date. Maybe it's better to do this in input?
    

    return df

df = jobs_load()
df = jobs_sort(df, "2022-10-31")

pd.set_option('display.max_rows', 100)
print(df)


# Either a number in the format "Posted {n} day(s) ago", from today with "Just posted" or "Today", or "Hiring ongoing"
# Possibly something else entirely, but we haven't seen it yet.

# Want to convert this value into an actual date.