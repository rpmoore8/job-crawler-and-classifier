import requests
import time
from bs4 import BeautifulSoup

from config import db_info, cities, headers
from db_utils.job import Job
from db_utils.db_methods import get_jobs_table, get_taken_ids


class AuthenticJobsCrawler():
    def __init__(self):
        self.source = "authenticjobs"
        
        
    def scrape(self, city, insert_into_db = True):
        jobs_table = get_jobs_table()
        taken_ids = get_taken_ids(city, self.source)

        for page in range(0, 1):
            params = {"page": str(page), "location": city}
            results = self.get_query_results(params)

            for result in results:
                if result["id"] not in taken_ids:
                    job = Job(
                        job_id = result["id"],
                        source = self.source,
                        name = result["title"].lower(),
                        contents = result["description"],
                        category = result["category"]["name"].lower(),
                        city = city,
                        date = result["post_date"],
                        link = result["apply_url"]
                    )
                    if insert_into_db:
                        job.insert_into_table(jobs_table)
                    else:
                        return job


    def get_query_results(self, params):
        params["api_key"] = "f30e0368501d3c1cd9548c11c85c53df"
        params["method"] = "aj.jobs.search"
        params["perpage"] = "100"
        params["format"] = "JSON"
        r = requests.get('https://authenticjobs.com/api/', params = params, headers = headers)
        time.sleep(15)
        j = r.json()
        results = j["listings"]["listing"]
        
        return results