from bs4 import BeautifulSoup
from random import uniform
import requests
import time
import re

from config import levels, headers, cities, search_categories
from db_utils.job import Job
from db_utils.db_methods import get_jobs_table, get_taken_ids

class IndeedCrawler():
    def __init__(self):
        self.source = "indeed"


    def scrape(self, city, insert_jobs_into_db = True):
        taken_ids = get_taken_ids(city, self.source)
        collected_ids = []

        new_jobs = []

        for category in search_categories:

            # change second arg in range for more results, ex: range(0, 201, 50):
            for start in range(0, 1, 50):
                params = {'q': category, 'l': city, 'start': start }
                results = self.get_query_results(params)
                for result in results:
                    id = result['id']
                    link =  "https://www.indeed.com" + result.find('a')['href']
                    company = result.find("span", class_="company")
                    # make sure company is found / job is not already collected
                    if company and (id not in new_jobs + taken_ids):
                        comp = company.text.strip().lower()
                        taken_ids.append(id)
                        new_job = Job(category = category, city = city, \
                        source = self.source, company = comp, link = link, job_id = id)
                        new_jobs.append(new_job)

        for job in new_jobs:
            jobs_table = get_jobs_table()
            listing = self.get_listing(job.link)
            if listing != None:
                job.name = listing.find('h3').text
                job.contents = str(listing.find(class_ = \
                "jobsearch-JobComponent-description icl-u-xs-mt--md"))

                if insert_jobs_into_db:
                    if not jobs_table:
                        jobs_table = get_jobs_table()
                        time.sleep(20)
                    job.insert_into_table(jobs_table)
                else:
                    # for testing
                    return job

    def get_query_results(self, params):
        params["sort"] = "date"
        params["limit"] = '50'
        r = requests.get('https://www.indeed.com/jobs', params = params)
        time.sleep(uniform(.5,1.5))
        if r.status_code != requests.codes.ok:
            return []
        else:
            soup = BeautifulSoup(r.text, "lxml")
            content = soup.find(id='resultsCol')
            if not content:
                return []
            else:
                results = content.find_all('div', class_ = re.compile("row result"))
                return results


    def get_listing(self, link):
        r = requests.get(link)
        time.sleep(uniform(.5, 1.7))
        page = BeautifulSoup(r.text, "lxml")
        listing = page.find(class_ = "jobsearch-JobComponent icl-u-xs-mt--sm")
        
        return listing
