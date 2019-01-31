from db_utils.db_methods import get_jobs_table, get_taken_ids
from db_utils.job import Job

# DB Methods

def test_get_jobs_table():
    """Connect to the jobs table in the DB"""
    jobs = get_jobs_table()
    assert jobs.name == "jobs"

def test_get_taken_ids():
    """Retrieve list of current job listings in DB"""
    indeed_taken_ids = get_taken_ids("Chicago, IL", "indeed")
    assert len(indeed_taken_ids) > 100

    indeed_taken_ids = get_taken_ids("blahblahblah", "indeed")
    assert len(indeed_taken_ids) == 0

    the_muse_taken_ids = get_taken_ids("New York City, NY", "themuse")
    assert len(the_muse_taken_ids) > 20


    # Job

    def test_pick_category():
        """"Reclassify an arbitrary category into one of the predefined search categories"""
        marketing_job = Job(category = "something to do with marketing")
        # pick_category(category) called in Job init
        assert marketing_job.category == 'marketing pr media'

        undefined_job = Job()
        assert undefined_job.category == "none"

        admin_job = Job(category = 'administration')
        assert admin_job.category == 'administration'

        software_job = Job(category = 'software engineering')
        assert software_job.category == 'information technology software'

    def test_insert_into_table():
        """Turns object into JSON with appropriate fields and parsed content"""

        content = """<div><h2 class="jobSectionHeader"><b>Job Description
</b></h2><div><div><div><p><b>Bring your passion to the Forefront</b></p><p><b><br>
The University of Chicago Medicine is Hiring : </b><b>Desktop Systems Engineer</b></p><div><b><br> Job Summary</b></div><div><br> The Desktop Engineer is responsible for the design, management and support of moderate to complex support and operating systems with general supervision. Areas of management and support may include but are not limited to, core operating systems; such as Macintosh and Windows, software distribution and anti-virus solutions. Engineer will serve as level three desktop supports for complex end user device management.</div><div><b><br> Essential Job Functions</b></div><ul><li> Responsible for installing, configuring, and maintaining operating system workstations and in support of business processing requirements</li><li>
Performs software installation and upgrade to operating systems and layered software packages utilizing effective distribution tools</li><li> Supports custom software systems working closely with key vendors</li><li> Conducts routine hardware and software audits of workstations to ensure compliance with established standards, policies and configuration guidelines</li><li> Develops and maintains a comprehensive operating system hardware and software configuration database/library of all support documentation</li><li>
Mentors less experienced support staff and peers</li><li> Performs other duties as requested by senior management.</li></ul><div><b><br> Qualifications</b></div><ul><li>
Bachelors degree in related technical area or technical training/experience equivalent required</li><li> Excellent decision making and problem solving skills</li><li>
Comprehensive experience in analyzing complex functions, procedures and problems to find creative, logical and appropriate solutions.</li><li> Effective time management skills, with the ability to complete projects and daily responsibilities both timely and effectively.</li><li> Ability to effectively deliver services in a high volume environment.</li></ul><div><b> Technical Abilities</b></div><ul><li> Macintosh support experience preferred. </li><li>Good working knowledge of Microsoft Active Directory and policy management within a directory services system is required.
</li><li> Experience with wireless device management preferred.</li><li>
Experience with software distribution systems required.</li><li> Experience with Anti-virus management consoles and troubleshooting required.</li><li> Experience with Anti-spyware solution preferred. </li><li>Experience in hardware and software design, installation, configuration, maintenance, and troubleshooting required</li></ul>
</div></div></div><h2 class="jobSectionHeader"><b>Why Join Us
</b></h2><div><div><div><div><i>We’ve been at the forefront of medicine since 1899. We provide superior healthcare with compassion, always mindful that each patient is a person, an individual. To accomplish this, we need employees with passion, talent and commitment… with patients and with each other. We’re in this together: working to advance medical innovation, serve the health needs of the community, and move our collective knowledge forward. If you’d like to add enriching human life to your profile, The University of Chicago Medicine is for you. Here at the forefront, we’re doing work that really matters. Join us. Bring your passion.</i></div><div><i><br> Bring your career to the next level at a hospital that is thriving; from patient satisfaction to employee engagement, we are at the Forefront of Medicine. Take advantage of all we have to offer and #BringYourPassiontotheForefront</i></div><div><i><br>
University of Chicago Medicine is growing; discover how you can be a part of this pursuit of excellence at: </i><i>www.uchospitals.edu/jobs</i></div><p><i><br>
The University of Chicago Medical Center is an equal opportunity employer. We evaluate qualified applicants without regard to race, color, ethnicity, ancestry, sex, sexual orientation, gender identity, marital status, civil union status, parental status, religion, national origin, age, disability, veteran status and other legally protected characteristics.</i></p></div></div></div></div>"""

        job = Job(name = "desktop systems engineer", category = 'information technology software', city = "Chicago, IL", source = "indeed", contents = contents, company = "UChicago Medicine", link = "https://www.indeed.com/viewjob?jk=83d4683581660e43&tk=1d237b4fragct802&from=serp&vjs=3")

        assert job.date == "none"
        assert job.name == "desktop systems engineer"
        assert job.category == "information technology software"
        assert job.city == "Chicago, IL"
        assert job.source == "indeed"
        assert job.company == "UChicago Medicine"
        assert job.link == "https://www.indeed.com/viewjob?jk=83d4683581660e43&tk=1d237b4fragct802&from=serp&vjs=3"
        assert len(job.content) > 0
        assert isinstance(job.content[0][0], str)
        assert isinstance(job.content[0][1], int)



