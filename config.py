#config.py

"""
This file contains the variables that dictate the parameters of the scraping and classification programs. Add more cities and search categories, edit the "good" and "bad" words list for classification, or edit the cleanTokens function to dictate the points assigned to sentences.
"""

# #Input mongoDB information here. Must use mongoDB for programs to work.
# db_info = {
#     "client": "REPLACE WITH CLIENT ADDRESS",
#     "database": "REPLACE WITH DATABSE NAME",
#     "table": "REPLACE WITH TABLE NAME"
# }

db_info = {
    "client": "mongodb://admin:admin123@ds117224-a0.mlab.com:17224,ds117224-a1.mlab.com:17224/competently-db?replicaSet=rs-ds117224",
    "database": "competently-db",
    "table": "jobs"
}


cities = ['Albuquerque, NM', 'Arlington, VA', 'Atlanta, GA', 'Austin, TX', 'Baltimore, MD', 'Boston, MA', 'Charlotte, NC', 'Chicago, IL', 'Cleveland, OH', 'Colorado Springs, CO', 'Columbus, OH', 'Dallas, TX', 'Denver, CO', 'Detroit, MI', 'El Paso, TX', 'Fort Worth, TX', 'Fresno, CA', 'Houston, TX', 'Indianapolis, IN', 'Jacksonville, FL',  'Kansas City, MO', 'Las Vegas, NV', 'Los Angeles, CA', 'Louisville, KY', 'Memphis, TN', 'Mesa, AZ', 'Miami, FL', 'Milwaukee, WI', 'Minneapolis, MN',  'Nashville, TN', 'New Orleans, LA', 'New York City, NY', 'Oakland, CA', 'Oklahoma City, OK', 'Omaha, NE', 'Philadelphia, PA', 'Poenix, AZ', 'Portland, OR', 'Raleigh, NC',  'Sacramento, CA', 'San Antonio, TX', 'San Diego, CA', 'San Francisco, CA', 'San Jose, CA', 'Seattle, WA', 'Tucson, AZ', 'Tulsa, OK', 'Virginia Beach, VA', 'Washington, DC', 'Wichita, KS']


levels = ['Internship', 'Entry Level', 'Mid Level', 'Senior Level']


search_categories = [
'creative design',
'sales', 
'legal',
'education',
'editorial',
'business operations strategy',
'human resources recruiting',
'management',
'health wellness fitness', 
'data analytics',
'healthcare medicine', 
'administration', 
'marketing pr media',
'information technology software', 
'engineering',
'accounting finance',
'insurance claims',
'customer service retail',
'fundraising development'
]

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}


#The following words are used to score a sentence on the likeliness of it containing required skills, competencies, education, certifications, etc.
word_values = {
    'associate': 1, 'commitment': 1, 'desire': 1, 'duties': 1, 'duty': 1, 'function': 1, 'good': 1,'include': 1, 'includes': 1, 'integral': 1, 'invaluable': 1, 'license': 1, 'love': 1, 'professional': 1, 'qualified': 1, 'require': 1, 'satisfactory': 1, 'talented': 1, 'talents': 1, 'willingness': 1,
    
    'abilities': 2, 'academic': 2, 'acceptable': 2, 'accountability': 2, 'accountable': 2, 'activities': 2, 'ambition': 2, 'ample': 2, 'basic': 2, 'candidate': 2, 'candidates': 2, 'capability': 2, 'certified': 2, 'competences': 2, 'competencies': 2, 'complete': 2, 'completed': 2, 'conduct': 2, 'confidence': 2, 'confident': 2, 'create': 2, 'credentials': 2, 'criteria': 2, 'critical': 2, 'crucial': 2, 'demonstrated': 2, 'design': 2, 'determines': 2, 'eager': 2, 'eagerness': 2, 'effectively': 2, 'ensure': 2, 'ensuresenthusiasm': 2, 'essential': 2, 'experiences': 2, 'experiment': 2, 'expert': 2, 'exposed': 2, 'exposure': 2, 'exprience': 2, 'field': 2, 'focus': 2, 'focuses': 2, 'functions': 2, 'ideal': 2, 'identify': 2, 'imperative': 2, 'important': 2, 'indispensable': 2, 'individual': 2, 'insight': 2, 'insights': 2, 'intellect': 2, 'key': 2, 'knack': 2, 'knowhow': 2, 'leverage': 2, 'leveraging': 2, 'maintain': 2, 'manage': 2, 'manages': 2, 'master': 2, 'mastery': 2, 'must': 2, 'necessary': 2, 'needed': 2, 'obligation': 2, 'obligations': 2, 'operate': 2, 'operation': 2, 'optimal': 2, 'organizing': 2, 'ought': 2, 'outstanding': 2, 'passion': 2, 'pedigree': 2, 'perform': 2, 'performance': 2, 'possess': 2, 'possesses': 2, 'prefer': 2, 'primary': 2, 'procedure': 2, 'procedures': 2, 'proper': 2, 'prowess': 2, 'pursuing': 2, 'qualification': 2, 'qualifications': 2, 'record': 2, 'reponsibilities': 2, 'requirement': 2, 'requirements': 2, 'requires': 2, 'requisite': 2, 'research': 2, 'responsibilities': 2, 'responsibility': 2, 'risks': 2, 'savvy': 2, 'sense': 2, 'shall': 2, 'should': 2, 'skill': 2, 'skills': 2, 'skillset': 2, 'solid': 2, 'solving': 2, 'specialize': 2, 'specialized': 2, 'specializing': 2, 'suitable': 2, 'superior': 2, 'support': 2, 'tactic': 2, 'tactics': 2, 'talent': 2, 'task': 2, 'tasks': 2, 'tools': 2, 'valuable': 2, 'vital': 2, 'will': 2, 'willing': 2, 'work': 2, 
    
    'ability': 3, 'able': 3, 'accredited': 3, 'acumen': 3, 'adequate': 3, 'advanced': 3, 'analytical': 3, 'analyze': 3, 'and/or': 3, 'appropriate': 3, 'aptitude': 3, 'assist': 3, 'bachelor': 3, 'bachelors': 3, 'background': 3, 'certification': 3, 'college': 3, 'comfortable': 3, 'competence': 3, 'comprehension': 3, 'compulsory': 3, 'cumulative': 3, 'degree': 3, 'demonstrate': 3, 'diploma': 3, 'domain': 3, 'effectively': 3, 'ensures': 3, 'enthusiasm': 3, 'equivalent': 3, 'etc': 3, 'excellent': 3, 'experience': 3, 'experienced': 3, 'expertise': 3, 'familiarity': 3, 'fluency': 3, 'fluent': 3, 'frameworks': 3, 'gpa': 3, 'imperative': 3, 'including': 3, 'knowledge': 3, 'knowledgeable': 3, 'least': 3, 'maintaining': 3, 'mandatory': 3, 'masters': 3, 'minimum': 3, 'multiple': 3, 'organize': 3, 'participate': 3, 'passionate': 3, 'plus': 3, 'preferable': 3, 'preferably': 3, 'preferred': 3, 'prior': 3, 'proficiency': 3, 'proficient': 3, 'properly': 3, 'proven': 3, 'related': 3, 'relevant': 3, 'required': 3, 'requiring': 3, 'responsible': 3, 'seasoned': 3, 'skilled': 3, 'specialization': 3, 'specification': 3, 'specifications': 3, 'strong': 3, 'sufficient': 3, 'technical': 3, 'typically': 3, 'understand': 3, 'understanding': 3, 'versed': 3, 'well-versed': 3, 'years': 3,


    'america': -1, 'company': -1, 'compensation': -1, 'country': -1, 'diversity': -1, 'gender': -1, 'globally': -1, 'inc.': -1, 'journey': -1, 'keywords': -1, 'not': -1, 'orientation': -1, 'paying': -1, 'u.s.': -1, 'wage': -1,
    
    'affirmative': -2, 'assistant': -2, 'brands': -2, 'check': -2, 'cities': -2, 'city': -2, 'contact': -2,'culture': -2, 'culture': -2, 'cv': -2, 'discriminatory': -2, 'drug': -2, 'eligibility': -2, 'employer': -2, 'headquartered': -2, 'headquarters': -2, 'incentives': -2, 'join': -2, 'location': -2, 'locations': -2, 'locations': -2, 'non-discriminatory': -2, 'offices': -2, 'organization': -2, 'our': -2, 'paid': -2, 'pay': -2, 'posted': -2, 'practice': -2, 'privileges': -2, 'receive': -2, 'salary': -2, 'screening': -2, 'sponsorship': -2, 'start': -2, 'teamates': -2, 'travel': -2, 'us': -2, 'violations': -2, 'workplace': -2, 'worldwide': -2, 
     
    'benefits': -3, 'citizenship': -3, 'contacted': -3, 'disability': -3, 'earn': -3, 'equal': -3, 'founded': -3, 'hours': -3, 'invite': -3, 'liable': -3, 'located': -3, 'perk': -3, 'perks': -3, 'race': -3, 'reimbursement': -3, 'resume': -3, 'sex': -3, 'stipend': -3, 'we': -3
}

