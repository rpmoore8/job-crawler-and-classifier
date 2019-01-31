import requests
import re
import time

from config import cities, search_categories, levels, headers
from db_utils.job import Job
from db_utils.db_methods import get_jobs_table, get_taken_ids

class GithubJobsCrawler():
    def __init__(self):
        self.source = "githubjobs"

    def scrape(self, city, insert_into_db = True):
        jobs_table = get_jobs_table()
        taken_ids = get_taken_ids(city, self.source)

        for i in range(0, 5):
            params = {'page': str(i), 'location': city}
            results = self.get_query_results(params)

            for result in results:
                if result["id"] not in taken_ids:
                    job = Job(
                        job_id = result["id"],
                        name = result["title"],
                        contents = result["description"],
                        date = result["created_at"],
                        city = city,
                        link = result["url"],
                        company = result["company"].lower(),
                        category = "information technology software",
                        source = self.source
                    )
                    if insert_into_db:
                        job.insert_into_table(jobs_table)
                    else:
                        return job

    def get_query_results(self, params):
        r = requests.get('https://jobs.github.com/positions.json', params = params, headers = headers)
        time.sleep(1)
        results = r.json()
        
        return results