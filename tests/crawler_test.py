from crawlers.indeed_crawler import IndeedCrawler
from crawlers.the_muse_crawler import TheMuseCrawler
from crawlers.authentic_jobs_crawler import AuthenticJobsCrawler
from crawlers.github_jobs_crawler import GithubJobsCrawler
from config import db_info, search_categories


# Indeed Crawler

def test_indeed_get_query_results():
    """Make request to Indeed.com and extract listings"""
    indeed_crawler = IndeedCrawler()
    params = {'q': 'marketing', 'l': 'Los Angeles, CA', 'start': 0 }
    results = indeed_crawler.get_query_results(params)
    assert len(results) > 0

    params["l"] = "Chicago, IL"
    different_results = indeed_crawler.get_query_results(params)
    assert results != different_results

def test_indeed_scrape():
    """Output a job scraped from Indeed.com"""
    indeed_crawler = IndeedCrawler()
    params = {'q': 'marketing', 'l': 'Los Angeles, CA', 'sort': 'date', 'limit': '50', 'start': 0 }
    job = indeed_crawler.scrape('Wichita, KS', insert_jobs_into_db = False)
    assert job.city == 'Wichita, KS'
    assert job.category == 'creative design' # The first category of the list
    assert job.source == 'indeed'
    assert len(job.company) > 0
    assert len(job.contents) > 0
    assert 'https://www.indeed.com' in job.link


# The Muse Crawler

def test_the_muse_get_query_results():
    """Make request to The Muse API and extract listings"""
    the_muse_crawler = TheMuseCrawler()
    params = { 'page': 1, 'location': "Detroit, MI", 
                'level': "Entry Level"}
    j = the_muse_crawler.get_query_results(params)
    assert len(j["results"]) > 0

def test_the_muse_scrape():
    """Output a job scraped from The Muse API"""
    the_muse_crawler = TheMuseCrawler()
    job = the_muse_crawler.scrape('San Francisco, CA', insert_jobs_into_db = False)
    assert job.city == 'San Francisco, CA'
    assert job.source == 'themuse'
    assert len(job.company) > 0
    assert len(job.contents) > 0
    assert len(job.link) > 0
    assert job.category in search_categories + ["none"]


# Authentic Jobs Crawler

def test_authentic_jobs_get_query_results():
    """Make request to Authentic Jobs API and extract listings"""
    authentic_jobs_crawler = AuthenticJobsCrawler()
    params = {"page": 0, "location": 'Boston, MA'}
    results = authentic_jobs_crawler.get_query_results(params)
    assert len(results) > 0 

def test_authentic_jobs_scrape():
    """Output a job scraped from Authentic Jobs API"""
    authentic_jobs_crawler = AuthenticJobsCrawler()
    job = authentic_jobs_crawler.scrape('Chicago, IL', insert_into_db = False)
    assert job.city == 'Chicago, IL'
    assert job.source == 'authenticjobs'
    assert len(job.company) > 0
    assert len(job.contents) > 0
    assert len(job.link) > 0
    assert job.category in search_categories + ["none"]


# Github Jobs Crawler

def test_github_jobs_get_query_results():
    """Make request to Github Jobs API and extract listings"""
    github_crawler = GithubJobsCrawler()
    params = {'page': 0, 'location': 'San Francisco, CA'}
    results = github_crawler.get_query_results(params)
    assert len(results) > 0

def test_github_jobs_scrape():
    """Output a job scraped from Github Jobs API"""
    github_crawler = GithubJobsCrawler()
    job = github_crawler.scrape("Chicago, IL", insert_into_db = False)
    assert job.city == 'Chicago, IL'
    assert job.source == 'githubjobs'
    assert len(job.company) > 0
    assert len(job.contents) > 0
    assert len(job.link) > 0
    assert job.category == "information technology software"
