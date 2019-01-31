import time
import requests

from config import levels, headers, cities
from db_utils.job import Job
from db_utils.db_methods import get_jobs_table, get_taken_ids

class TheMuseCrawler():
    def __init__(self):
        self.source = "themuse"

    def scrape(self, city, insert_jobs_into_db = True):
        jobs_table = get_jobs_table()
        taken_ids = get_taken_ids(city, self.source)

        for level in levels:
            total_pages = 9
            for page in range(1, total_pages):
                params = { 'page': str(page), 'location': city, 
                'level': level}
                j = self.get_query_results(params)
                total_pages = int(j['page_count'])

                for result in j["results"]:
                    if result["id"] not in taken_ids \
                    and "landing_page" in result["refs"] \
                    and len(result["locations"]) > 0 \
                    and city == result["locations"][0]["name"]:
                        category = "none"
                        if len(result["categories"]) > 0:
                            category = result["categories"][0]["name"].lower()
                        job = Job(
                            name = result["name"],
                            category = category,
                            city = city,
                            source = self.source,
                            contents = result["contents"],
                            company = result["company"]["name"].lower(),
                            date = result["publication_date"],
                            link = result["refs"]["landing_page"],
                            job_id = result["id"])

                        if insert_jobs_into_db:
                            job.insert_into_table(jobs_table)
                        else:
                            return job


    def get_query_results(self, params):
        params['descending'] = 'true'
        params['api_key'] =  'e45578e2555dcc93550818c70d5df559a9b1efae3c2a6eb0cbb48a2e7db562aa'
        r = requests.get( 'https://www.themuse.com/api/public/jobs', params = params, headers = headers)
        time.sleep(0.7)
        j = r.json()

        return j