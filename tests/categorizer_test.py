from data_processing.categorizer import Categorizer
from config import search_categories


# Categorizer

def test_compile_category_words():
    """Creates dict of words from jobs in each category"""
    categorizer = Categorizer()
    categorizer.compile_category_words(test = True)

    for category in search_categories:
        assert isinstance(categorizer.word_scores[category], dict)
        for word in categorizer.word_scores[category]:
            assert categorizer.word_scores[category][word] > 0


def test_add_word_scores():
    """Assigns correct scores to words in job"""
    job = {"name": "civil engineer", "category": "engineering", "keywords": ["engineering", "civil", "architecture"], "contents": [{"text": ["this", "is", "a", "job"], "score": 0, "key": True}]}

    categorizer = Categorizer()
    categorizer.add_word_scores(job)

    assert categorizer.word_scores[job["category"]]["engineer"] == 20
    assert categorizer.word_scores[job["category"]]["civil"] == 35
    assert categorizer.word_scores[job["category"]]["engineering"] == 20
    assert categorizer.word_scores[job["category"]]["architecture"] == 15
    assert "a" not in categorizer.word_scores[job["category"]]


def test_sort_category_words_and_lower_scores_of_common_words():
    """Words with smaller scores are removed from the dict and scores lowered for common words"""
    categorizer = Categorizer()
    categorizer.compile_category_words(test = True)

    category = 'marketing pr media'
    word_score_pairs = [(key, value) for key, value in categorizer.word_scores[category].items()]
    sorted_words = sorted(word_score_pairs, key = lambda kv: kv[1], reverse = True)[:50]

    categorizer.sort_category_words()

    for word in sorted_words:
        if word[1] > 2:
            assert word[0] in categorizer.word_scores[category]

    category_total = 0
    for word in categorizer.word_scores[category]:
            category_total += categorizer.word_scores[category][word]

    categorizer.lower_scores_of_common_words()

    new_total = 0
    for word in categorizer.word_scores[category]:
        new_total += categorizer.word_scores[category][word]

    assert new_total < category_total


def test_normalize_word_scores():
    categorizer = Categorizer()
    categorizer.compile_category_words(test = True)
    categorizer.normalize_word_scores()

    total = None
    for category in categorizer.word_scores:
        if category == "none":
            continue

        category_total = 0
        for word in categorizer.word_scores[category]:
            category_total += categorizer.word_scores[category][word]

        if total:
            assert abs(category_total - total) < 0.1
        else:
            total = category_total


def test_calc_category_scores():

    assert True
    

def test_use_scores_to_categorize():
    assert True
