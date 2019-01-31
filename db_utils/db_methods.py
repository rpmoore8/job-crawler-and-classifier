from pymongo import MongoClient
import pymongo

from config import db_info


def get_jobs_table():
    client = MongoClient(db_info["client"])
    db = client[db_info["database"]]
    jobs = db[db_info["table"]]
    if jobs == None:
        raise ValueError('Issue connecting to database. Make sure db_info is properly set in config.py')
    return jobs

def get_taken_ids(city, source):
    taken_ids = []
    jobs = get_jobs_table()
    for listing in jobs.find({"source": source, "city": city}):
        taken_ids.append(listing["job-id"])
    return taken_ids