from data_processing.keys_generator import KeysGenerator


# Keys Generator

def test_load_jobs():
    """Loads a job from the database"""
    generator = KeysGenerator()
    id = generator.load_jobs(test = True)
    assert isinstance(generator.jobs[id]["name"], str)
    assert isinstance(generator.jobs[id]["company"], str)
    assert isinstance(generator.jobs[id]["category"], str)
    assert isinstance(generator.jobs[id]["contents"], list) 
    assert isinstance(generator.jobs[id]["contents"][0], dict) 
    assert isinstance(generator.jobs[id]["contents"][0]["text"], list)
    assert isinstance(generator.jobs[id]["contents"][0]["score"], int)
    assert isinstance(generator.jobs[id]["contents"][0]["key"], bool)


def test_calc_word_and_doc_frequency():
    """Calculates document frequency, word frequency, and word total"""
    generator = KeysGenerator()
    id = generator.load_jobs(test = True)
    generator.calc_word_and_doc_frequency()

    assert len(generator.document_frequency) > 0
    assert len(generator.jobs[id]["word_frequency"]) > 0
    assert generator.jobs[id]["word_total"] > 0

    for word in generator.document_frequency:
        assert generator.document_frequency[word] >= 1

    for word in generator.jobs[id]["word_frequency"]:
        assert word in generator.document_frequency


def test_calc_tf_dif():
    """Calculates tf-dif score for a job"""
    generator = KeysGenerator()
    id = generator.load_jobs(test = True)
    generator.calc_word_and_doc_frequency()
    generator.calc_tf_dif()

    assert len(generator.jobs[id]["tf_dif"]) < len(generator.jobs[id]["word_frequency"])

    for word in generator.jobs[id]["tf_dif"]:
        assert generator.jobs[id]["tf_dif"][word] >= 0


def test_determine_keywords():
    """Creates list of keywords of correct length"""
    generator = KeysGenerator()
    id = generator.load_jobs(test = True)
    keywords = generator.determine_keywords(insert_into_db = False)

    assert 0 < len(keywords) < 21
    assert isinstance(keywords, list)


def test_determine_key_sentences():
    """Flags key sentences"""
    generator = KeysGenerator()
    id = generator.load_jobs(test = True)
    keywords = generator.determine_keywords(insert_into_db = False)
    contents = generator.determine_key_sentences(insert_into_db = False)

    key_sentences = 0
    for sentence in contents:
        if sentence["key"] == True:
            assert sentence["score"] >= 0
            key_sentences += 1
    
    assert key_sentences > 0
