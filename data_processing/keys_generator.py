import math
from nltk.corpus import stopwords
import string

from db_utils.db_methods import get_jobs_table
from config import word_values

punc = [p for p in list(string.punctuation)]
stop = stopwords.words('english') + punc + list(word_values.keys())


def generate_keywords_and_key_sentences():
    generator = KeysGenerator()
    generator.load_jobs()
    generator.determine_keywords()
    generator.determine_key_sentences()
    

class KeysGenerator:
    def __init__(self):
        self.jobs = {}


    def load_jobs(self, test = False):
        print("Loading jobs from database...")
        jobs_table = get_jobs_table()
        total = 0
        for job in jobs_table.find():
            total += 1
            new_job = {}
            new_job["name"] = job["name"].lower()
            new_job["contents"] = job["contents"]
            new_job["company"] = job["company"]
            new_job["category"] = job["category"]

            if "keywords" in job:
                new_job["keywords"] = job["keywords"]

            self.jobs[job["_id"]] = new_job

            if test and total >= 20 and len(job["contents"]) >= 10:
                return job["_id"]


    def determine_keywords(self, insert_into_db = True):
        self.calc_word_and_doc_frequency()
        self.calc_tf_dif()

        print("Determining keywords...")
        jobs_table = get_jobs_table()
        for id in self.jobs:
            if not jobs_table:
                jobs_table = get_jobs_table()

            sorted_values = sorted(self.jobs[id]["tf_dif"].values())
            index = int(len(sorted_values) // 1.5)
            cutoff_score = sorted_values[index]
            if len(sorted_values) > 20:
                cutoff_score = sorted_values[-20]

            for word, value in list(self.jobs[id]["tf_dif"].items()):
                if value <= cutoff_score:
                    del self.jobs[id]["tf_dif"][word]
            
            self.jobs[id]["keywords"] = list(self.jobs[id]["tf_dif"].keys())

            if insert_into_db:
                jobs_table.update_one({'_id': id}, {'$set': {'keywords': self.jobs[id]["keywords"]}})
            else:
                return self.jobs[id]["keywords"]


    def calc_word_and_doc_frequency(self):
        print("Calculating word frequency and document frequency...")
        self.document_frequency = {}
        for id in self.jobs:
            word_frequency = {}
            word_total = 0

            for word in self.jobs[id]["name"].split() + self.jobs[id]["category"].split():
                word_total += 1
                if word in word_frequency:
                    word_frequency[word] += 10
                else:
                    word_frequency[word] = 10
                    if word in self.document_frequency:
                        self.document_frequency[word] += 1
                    else:
                        self.document_frequency[word] = 1

            for sentence in self.jobs[id]["contents"]:
                for word in sentence["text"]:
                    if word not in stop + self.jobs[id]["company"].split() and word[:4] != 'www.':
                        word_total += 1
                        if word in word_frequency:
                            word_frequency[word] += sentence["score"]
                        else:
                            word_frequency[word] = sentence["score"]
                            if word in self.document_frequency:
                                self.document_frequency[word] += 1
                            else:
                                self.document_frequency[word] = 1

            self.jobs[id]["word_frequency"] = word_frequency
            self.jobs[id]["word_total"] = word_total


    def calc_tf_dif(self):
        print("Calculating tf-dif score...")
        for id in self.jobs:
            tf_dif = {}
            score_total = 0
            for word in self.jobs[id]["word_frequency"]:
                tf_dif[word] = 0
                if self.jobs[id]["word_frequency"][word] > 0:
                    tf_dif[word] = \
                    (self.jobs[id]["word_frequency"][word] / self.jobs[id]["word_total"]) \
                     * math.log(len(self.jobs) / self.document_frequency[word])

                score_total += tf_dif[word]

            self.jobs[id]["tf_dif"] = tf_dif

            # optimize by eliminating bottom half of scored words
            average_score = score_total / len(self.jobs[id]["word_frequency"])
            for word in self.jobs[id]["word_frequency"]:
                if self.jobs[id]["tf_dif"][word] < average_score:
                    del self.jobs[id]["tf_dif"][word]
        

    def determine_key_sentences(self, insert_into_db = True):
        print("Determining key sentences...")
        jobs_table = get_jobs_table()

        for id in self.jobs:
            if not jobs_table:
                jobs_table = get_jobs_table()

            for sentence in self.jobs[id]["contents"]:
                if sentence["score"] >= 0:
                    score = sentence["score"]
                    for word in sentence["text"]:
                        if word in self.jobs[id]["keywords"]:
                            score += 6
                    
                    if (score / (1 +len(sentence["text"])//10)) > 5:
                        sentence["key"] = True

            if insert_into_db:
                jobs_table.update_one({'_id': id}, {'$set': {'contents': self.jobs[id]["contents"]}})
            else:
                return self.jobs[id]["contents"]
                

    def print_job_summaries(self):  
        for id in self.jobs:
            print()
            print(self.jobs[id]["name"])
            for sentence in self.jobs[id]["contents"]:
                if sentence["key"]:
                    sentence_str = " ".join(sentence["text"])
                    print(sentence_str)
