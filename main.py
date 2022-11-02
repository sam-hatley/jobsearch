from jobscrape import job_search_time
from jobanalysis import *
import datetime

while True:
    runtype = input('(S)crape new jobs or (L)oad old jobs? (S/L): ').lower()

    if runtype == 's':
        # Collect the queries saved in a text file
        queries = open('jobs.txt').read().splitlines()

        # Set a date range
        while True:
            usr_in = input('Number of days ago to search jobs? ')
            try:
                usr_in = int(usr_in)
                if usr_in <= 0:
                    print('Please type an integer above 0')
                    continue
                break
            except:
                print("Please type an integer above 0")

        # Search for the queries
        dict = job_search_time(queries, usr_in)
        jobs_df = jobs_save(dict)

        cont = input("\nPress enter to continue to job sorting or anything else to quit: ")
        if cont != "":
            print("Exiting")
            exit(0)
        else:
            break

    elif runtype == 'l':
        jobs_df = jobs_load()
        break

    else:
        print('\nInvalid input, please type "s" or "l" to continue: ')


usr_in = input('Number of days ago to display search results? ')
date_range = datetime.datetime.now() - datetime.timedelta(int(usr_in))

df = jobs_sort(jobs_df, date_range)
jobs_save(df, keep="first")

print("Selected jobs saved to selects.csv.")
print(df)