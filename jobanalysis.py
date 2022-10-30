import os.path
import pandas as pd


def jobs_save(dict):
    '''Checks job links against previously fetched jobs, and saves new entries to a file.
    Returns a dataframe of all jobs'''

    new_jobs_df = pd.DataFrame(dict)

    # Check if file exists
    if os.path.isfile('joblist.pkl'):
        old_jobs_df = pd.read_pickle('joblist.pkl')
        df = pd.concat([new_jobs_df, old_jobs_df])
        # Remove any entry with the same link
        df = df.drop_duplicates(subset="Link", keep="last")
    else:
        df = new_jobs_df

    df.to_pickle('joblist.pkl')
    df.to_csv('joblist.csv')

    return df


def jobs_sort(df):
    '''Iterates through jobs in a dataframe from a specified timeframe. 
    User input flags selects, returns a dataframe of selected jobs'''

    exit()