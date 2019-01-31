import re
from nltk import word_tokenize
import pymongo

from config import word_values, search_categories

class Job:
    def __init__(self, source = "none", job_id = "none", name = "none", contents = "none", \
        company = "none", date= "none", city = "none", link = "none", category="none"):
        self.source = source
        self.job_id = job_id
        self.name = name
        self.contents = contents
        self.company = company
        self.date = date
        self.city = city
        self.link = link
        self.category = category
        if category != "none":
            self.category = self.pick_category(category)

    def pick_category(self, given_category):
        if given_category in search_categories:
            return given_category
        for category in search_categories:
            for word in given_category.split():
                if word in category:
                    return category
        return "none"

    def insert_into_table(self, table, test = False):
        job = {"source": self.source, "job-id": self.job_id, "name": self.name, 
        "contents": self.score_sentences(self.tokenize(self.contents), self.company), "company": self.company,
        "date": self.date, "city": self.city, "link": self.link, "category": self.category}

        if not test:
            print(self.job_id, self.name)
            table.insert_one(job).inserted_id
        else:
            return job


    def tokenize(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, ' . ', raw_html)
        words = [word for word in word_tokenize(
        cleantext.lower())]
        return words

    def score_sentences(self, words, company):
        end_of_sent = ['!', '?', '.', '•', ';', '*']
        sentences, sent = [], []
        score = 0
        for word in words:
            if word in end_of_sent:
                if len(sent) > 1:
                    sentence = { "text": sent, "score": score, "key": False}
                    sentences.append(sentence)
                sent = []
                score = 0
            else:
                sent.append(word)
                if word in word_values:
                    score += word_values[word]
        return sentences
