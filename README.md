# A Job Scraper for Indeed

## Background
Going through job listings drives me a bit crazy, because most of what I'm trying to do could be sped up considerably if I wasn't dealing with a website's bare-bones UI.

I wanted to improve on this process by writing a program that could actually deliver me the kinds of results I want, in the format I want it:

1. A list of jobs with just the most basic information: title, company posting, and date posted
2. Jobs that have been pre-filtered by keyword: I'm not looking to work as a receptionist, so I'd rather not see _any_ listing with that in the title
3. A way to quickly sort through and rank the jobs that have been posted.

## Usage

### Requirements

The program is built in Python 3.9, and relies on the following external packages:

| Package | Usage |
| - | - |
| Urllib | Dynamically builds URLs |
| Cloudscraper | Scrapes Indeed's website while bypassing CloudFlare's anti-bot protection |
| bs4 | BeautifulSoup: parses html files and retrieves text |
| pandas | Manages and filters lists of selected jobs |

You'll also need to have a ```jobs.txt``` file in the same folder as main.py: it's a text file with a list of search queries, separated by line. If your query is more than one word, separate it with spaces or a "+". Case doesn't matter. It should look something like the below:

```
Janitor
Head of Janitorial Services
Zamboni Driver
Bodyguard
secret agent
```

### Files

This is made up of three files:

| File | Description |
| - | - |
| [main.py](main.py) | The file used to run the program. It calls functions within the other two files to allow a text-based user interface for fetching and sorting jobs. |
| [jobscrape.py](jobscrape.py) | Stores functions related to scraping Indeed |
| [jobanalysis.py](jobanalysis.py) | Stores functions related to handling the output of jobanalysis.py |

### Running the Program

1. After installing any [dependencies](#requirements), run [main.py](main.py).
2. It will ask you if you want to scrape or load. If it's your first time running the program, choose scrape (s).
3. Choose a number of days to scrape jobs: if you select 1, it will search for jobs posted between yesterday and today. Type any number above 0.
4. The program will go through your list of jobs, and search each one until it hits the number of days you've specified. Don't worry if you get an error in the process: I haven't explicitly built in a way of handling "no results" pages, but the program will continue to work even if it hits one.
5. Go ahead and take a look at the results. Plug in a number to "rate" the job. If you're finished before going through the results, type "q".
6. You'll see a list with the job titles and links in the program: you can take a look through them here, or just go to the generated file ```selects.csv``` to look through them later. All jobs and ratings are stored in ```joblist.csv```, so you can come back and take a look through that later, if you want.

```
(S)crape new jobs or (L)oad old jobs? (S/L): s
Number of days ago to search jobs? 1
Retrieving results 1-15 for Janitor
Last posting: 2022-10-20

Press enter to continue to job sorting or anything else to quit: 
Number of days ago to display search results? 10

Result 1 of 535:
Title             Weekend Cleaner/Janitor
Company              Hayward Services Ltd
Date Posted           2022-10-27 00:00:00
Date Retrieved                 2022-11-02
Name: 0, dtype: object
Type an integer rating if interested. Enter or 0 to reject. (Q) to quit: 1

Result 2 of 535:
Title             Janitor with Driving License
Company              Essential Results Limited
Date Posted                2022-10-26 00:00:00
Date Retrieved                      2022-11-02
Name: 3, dtype: object
Type an integer rating if interested. Enter or 0 to reject. (Q) to quit: 2

Result 3 of 535:
Title                        Night Cleaner
Company           Britannia Services Group
Date Posted            2022-10-25 00:00:00
Date Retrieved                  2022-11-02
Name: 5, dtype: object
Type an integer rating if interested. Enter or 0 to reject. (Q) to quit: q
Selected jobs saved to selects.csv.
                          Title                    Company Date Posted  ... Time Retrieved                                               Link Select
3  Janitor with Driving License  Essential Results Limited  2022-10-26  ...       10:35:36  https://uk.indeed.com/viewjob?jk=0e591257c2b7f3ac    2.0
0       Weekend Cleaner/Janitor       Hayward Services Ltd  2022-10-27  ...       10:41:32  https://uk.indeed.com/viewjob?jk=d6a6ea7051082f9d    1.0

[2 rows x 7 columns]
```