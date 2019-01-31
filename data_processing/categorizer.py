from nltk.corpus import stopwords
import string

from config import word_values, search_categories
from db_utils.db_methods import get_jobs_table

punc = [p for p in list(string.punctuation)]
stop = stopwords.words('english') + punc + list(word_values.keys())


def categorize_jobs():
    categorizer = Categorizer()
    classifying = True
    round = 1

    while classifying:
        print("Round ", round, "of classification")
        categorizer.compile_category_words()
        reclassified_jobs = categorizer.reclassify_job_categories()
        round += 1
        if reclassified_jobs == 0:
            classifying = False


class Categorizer:
    def __init__(self):
        self.word_scores = {}

        for category in search_categories + ['none']:
            self.word_scores[category] = {}
    

    def compile_category_words(self, test = False):
        print("Loading category words from database")
        for category in search_categories:
            jobs_table = get_jobs_table()
            total_jobs = 0

            for job in jobs_table.find({"category": category}):
                total_jobs += 1
                self.add_word_scores(job)

                if test and total_jobs >= 30:
                    break
                    
    
    def add_word_scores(self, job):
        category = job["category"]
        for word in job["name"].lower().split():
            if word in self.word_scores[category]: self.word_scores[category][word] += 20
            else: self.word_scores[category][word] = 20

        for word in job["keywords"]:
            if word in self.word_scores[category]: self.word_scores[category][word] += 15
            else: self.word_scores[category][word] = 15

        for word in category.split():
            if word in self.word_scores[category]: self.word_scores[category][word] += 5
            else: self.word_scores[category][word] = 5

        for sentence in job["contents"]:
            if sentence["key"]:
                for word in sentence["text"]:
                    if word not in stop:
                        if word in self.word_scores[category]: self.word_scores[category][word] += 5
                        else: self.word_scores[category][word] = 5


    def reclassify_job_categories(self, insert_into_db = True):
        self.sort_category_words()
        self.lower_scores_of_common_words()
        self.normalize_word_scores()
        self.print_category_words()

        print("Reclassify job categories")
        jobs_table = get_jobs_table()
        reclassified_jobs = 0

        for job in jobs_table.find():
            scores = self.calc_category_scores(job)

            if len(scores) > 0:
                if self.use_scores_to_categorize(scores, job, jobs_table, insert_into_db):
                    reclassified_jobs += 1

        return reclassified_jobs


    def sort_category_words(self):
        print("Sort category words")
        for category in self.word_scores:
            for word, value in list(self.word_scores[category].items()):
                if value <= 2:
                    del self.word_scores[category][word]

            if len(self.word_scores[category]) > 50:
                sorted_values = sorted(self.word_scores[category].values())
                cutoff_score = sorted_values[-50]
                for word, value in list(self.word_scores[category].items()):
                    if value < cutoff_score:
                        del self.word_scores[category][word]


    def lower_scores_of_common_words(self):
        print("Lower scores of common words")
        for category in self.word_scores:
            for cat in search_categories:
                if category != cat:
                    for word in self.word_scores[cat]:
                        if word in self.word_scores[category]:
                            self.word_scores[category][word] /= 1.2


    def normalize_word_scores(self):
        print("normalize word scores")
        for category in self.word_scores:
            total = 0
            for word in self.word_scores[category]:
                total += self.word_scores[category][word]

            denominator = total / 100
            for word in self.word_scores[category]:
                self.word_scores[category][word] /= denominator


    def calc_category_scores(self, job):
        scores = []
        for category in self.word_scores:
            if category == "none":
                continue

            points = 0
            name = job["name"].lower()
            for word in self.word_scores[category]:
                if word in name:
                    points += (7 * self.word_scores[category][word])

                if word in job["keywords"]:
                    points += (2.5 * self.word_scores[category][word])
            
            if points >= 20:
                for sentence in job["contents"]:
                    if sentence["key"]:
                        for word in self.word_scores[category]:
                            if word in sentence:
                                points += self.word_scores[category][word]
                scores.append((category, points))

        return scores


    def use_scores_to_categorize(self, scores, job, jobs_table, insert_into_db):
        sorted_scores = sorted(scores, key=lambda kv: kv[1], reverse=True)
        rank, i = 1, 0
        while i < len(sorted_scores) and sorted_scores[i][0] != job["category"]:
            i += 1

        if i >= len(sorted_scores) or sorted_scores[0][1] >= (2.2 * sorted_scores[i][1]):
            print(job["name"], " - ", job["category"])
            print("CHANGE TO", sorted_scores[0][0])
            for score in sorted_scores[:5]:
                print(str(rank) + '. ', score[0], str(score[1] * 10 / (len(job["contents"]) + 1))[:5] + "%")
                rank += 1
            print()
            print()
            if insert_into_db:
                jobs_table.update_one({'_id': job["_id"]}, {'$set': {'category': sorted_scores[0][0]}}, upsert=False)

            return True

        else:
            return False


    def print_category_words(self):
        for category in self.word_scores:
            print(category)
            for word in self.word_scores[category]:
                print(word, self.word_scores[category][word])       
            print()
            print()
