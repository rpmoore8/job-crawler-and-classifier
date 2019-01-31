from crawlers.indeed_crawler import IndeedCrawler
from crawlers.the_muse_crawler import TheMuseCrawler
from crawlers.github_jobs_crawler import GithubJobsCrawler
from crawlers.authentic_jobs_crawler import AuthenticJobsCrawler

from data_processing.categorizer import categorize_jobs
from data_processing.keys_generator import generate_keywords_and_key_sentences
from db_utils.db_methods import get_jobs_table

from config import cities

def main():
    indeed_crawler = IndeedCrawler()
    muse_crawler = TheMuseCrawler()
    github_crawler = GithubJobsCrawler()
    authentic_crawler = AuthenticJobsCrawler()

    for city in cities:
        print("Collecting job listings from " + city)
        indeed_crawler.scrape(city)
        muse_crawler.scrape(city)
        github_crawler.scrape(city)
        authentic_crawler.scrape(city)

    generate_keywords_and_key_sentences()
    categorize_jobs()

main()
