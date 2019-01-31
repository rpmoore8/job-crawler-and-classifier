# XXXX DECOMISSIONED (will not work as written) XXXX
# monster.com will temporarily block your IP address after 100 or so consecutive requests
# This file is kept as an example of a crawler BEFORE refactoring - yikes!


from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
import pymongo
import re
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import time
from random import uniform

from config import dbInfo, badWords, goodWords, cities, searchCategories, cleanTokens


url = "https://www.monster.com/jobs/search"
payload = {'q': 'category', 'where': 'location', 'stpage': '1', 'page': '10' }

client = MongoClient(dbInfo["client"])
db = client[dbInfo["database"]]
posts = db[dbInfo["table"]]


takenIds = []
for post in posts.find({"source": "monster"}):
    takenIds.append(post["job-id"])

jobIds = {}
for city in cities:
    print("Collecting jobs in " + city)
    for category in searchCategories:
        payload['q'] = category
        payload['where'] = city
        pageNumber = 1

        content = None
        notEnoughPages = True

        while(notEnoughPages):
            payload['page'] = str(pageNumber)

            r = requests.get(url, params=payload)
            soup = BeautifulSoup(r.text, "lxml")
            if r.status_code != 200:
                pageNumber -= 1
                time.sleep(uniform(.5,1.5))
            else:
                notEnoughPages = False
                content = soup.find(id="SearchResults")
        for result in content.find_all("section", class_="card-content"):
            try:
                id = result['data-jobid']
                link = result.find('a')['href']

                if id not in jobIds and id not in takenIds:
                    # print(link)
                    jobIds[id] = [link, category, city]

            except (TypeError, KeyError) as e:
                # print(e)
                continue 


for id in jobIds:
    time.sleep(uniform(.5,1.5))
    link = jobIds[id][0]
    category = jobIds[id][1]
    city = jobIds[id][2]
    r = requests.get(link)
    posting = BeautifulSoup(r.text, "lxml")
    h = posting.find("h1", class_="title")
    if h == None:
        continue
    title = h.text
    end = title.find(' at ')
    company = title[(end + 4):-2]
    title = title[:end]
    details = str(posting.find("div", id="JobDescription"))

    post = {
    "source": "monster", 
    "job-id": id, 
    "name": title, 
    "contents": cleanTokens(details, company.lower()), 
    "company": company, 
    "city": city,
    "link": link,
    "category": category
    }

    try:
        post_id = posts.insert_one(post).inserted_id
        print(post_id)
    except pymongo.errors.DuplicateKeyError:
        continue
