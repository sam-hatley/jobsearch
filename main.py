from jobscrape import job_search_time
from jobanalysis import *
import datetime
import pandas as pd
import pyperclip

while True:
    runtype = input("(S)crape new jobs, (L)oad old jobs, or (E)xport jobs?: ").lower()
    usr_in = ""

    if runtype == "s":
        # Collect the queries saved in a text file
        queries = open("jobs.txt").read().splitlines()

        # Set a date range
        while True:
            usr_in = input("Number of days ago to search jobs? ")
            try:
                usr_in = int(usr_in)
                if usr_in <= 0:
                    print("Please type an integer above 0")
                    continue
                break
            except:
                print("Please type an integer above 0")

        # Search for the queries
        jobs_dict = job_search_time(queries, usr_in)
        jobs_df = jobs_save(jobs_dict)

        cont = input(
            "\nPress enter to continue to job sorting or anything else to quit: "
        )
        if cont != "":
            print("Exiting")
            exit(0)
        else:
            break

    elif runtype == "l":
        jobs_df = jobs_load()
        break

    elif runtype == "e":
        usr_in = input("Export (S)elects or (A)ll jobs? ").lower()
        df = jobs_load()
        export_type = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if usr_in == "s":
            df["Select"] = pd.to_numeric(df["Select"], errors="coerce")
            df = df[pd.notnull(df["Select"])]
            df = df[df["Select"] > 0]

            export_type = "selects_" + export_type
        elif usr_in != "a":
            continue

        df.to_csv(f"custom_export_{export_type}.csv")

        print(f"Results saved to custom_export_{export_type}.csv.")
        exit(0)

    else:
        print('\nInvalid input, please type "s", "l", or "e" to continue: ')

if not usr_in:
    usr_in = input("Number of days ago to display search results? ")
date_range = datetime.datetime.now() - datetime.timedelta(int(usr_in))

selects_df = jobs_sort(jobs_df, date_range)

try:
    if not selects_df:
        exit(0)
except ValueError:
    if selects_df.empty:
        exit(0)

# print(
#     f"Selected jobs saved to selects_{datetime.datetime.now().strftime('%Y-%m-%d')}.csv."
# )

links_string = "\n".join([str(link) for link in selects_df["Link"]])
pyperclip.copy(links_string)
print("Selected job links copied to clipboard.")

print(selects_df)
