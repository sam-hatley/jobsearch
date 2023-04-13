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


def jobs_sort(df, date):
    '''Iterates through jobs in a dataframe from a specified date. User input 
    flags selects, returns a dataframe of selected jobs. Date should be in the 
    format "YYYY-MM-DD".'''

    df['Date Posted'] = pd.to_datetime(df['Date Posted'])
    df = df[(df['Date Posted'] >= date)]
    df = df.fillna('')
    df = df[(df['Select'] == '')]

    # Filter out some words
    with open('./filters.txt') as f:
        filters = f.readlines()
    
    filters = [line.strip() for line in filters]

    filter = '|'.join(filters)
    df = df[~df['Title'].str.contains(filter, case=False)]

    for i in range(0, len(df)):
        print(f'\nResult {i+1} of {len(df)+1}:')
        print(df.iloc[i,0:4])
        usr_input = input('Type an integer rating if interested. Enter or 0 to reject. (Q) to quit: ')
        if not usr_input.isdigit():
            if usr_input.lower() == 'q':
                break
            rating = 0
        else:
            rating = int(usr_input)
        
        df.iloc[i, df.columns.get_loc('Select')] = rating
    
    df['Select'] = pd.to_numeric(df['Select'])
    df = df.sort_values(by='Select', ascending=False)
    df_selects = df[(df['Select'] > 0)]

    df_selects.to_csv('selects.csv')

    return df_selects