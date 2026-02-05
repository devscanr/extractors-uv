# mypy: disable-error-code=no-untyped-def
import pytest
from spacy import Language
from ..utils import fix_grammar, normalize
from .data import TAGS
from .experience import Experience
from .extractor import ExperienceExtractor

class Test_ExperienceExtractor:
  @pytest.fixture(scope="class")
  def extract(self, nlp: Language):
    ex = ExperienceExtractor(nlp, TAGS)
    def do(text: str) -> Experience | None:
      return ex.extract(fix_grammar(normalize(text)))
    return do

  @pytest.fixture(scope="class")
  def extract_many(self, nlp: Language):
    ex = ExperienceExtractor(nlp, TAGS)
    def do(texts: list[str]) -> list[Experience | None]:
      return ex.extract_many([fix_grammar(normalize(text)) for text in texts])
    return do

  def test_extract_many_smoke(self, extract_many) -> None:
    assert extract_many([
      "Senior dev",
      "1 month of experience",
      "Blah-blah",
    ]) == [Experience("Senior"), Experience("Exact", months=1), None]

  def test_extract_smoke(self, extract) -> None:
    # Exact months
    assert extract("1 month of experience") == Experience("Exact", months=1)
    assert extract("1+ month of experience") == Experience("Exact", months=1, over=True)
    assert extract("some months of experience") is None
    # Exact years
    assert extract("1 year of experience") == Experience("Exact", months=12)
    assert extract("one year experience") == Experience("Exact", months=12)
    assert extract("1+ year of experience") == Experience("Exact", months=12, over=True)
    assert extract("1.5 years of experience") == Experience("Exact", months=18)
    assert extract("some years of experience") is None
    # Other
    assert extract("Someone") is None
    assert extract("Junior engineer") == Experience("Junior")
    assert extract("Middle designer") is None
    assert extract("Senior developer") == Experience("Senior")
    assert extract("Senior student") is None
    # Multiple
    assert extract("Junior backend, middle frontend") is None

  def test_extract_adhoc1(self, extract) -> None:
    # Past markers don't affect the extractor
    assert extract("Former principal developer") is None
    assert extract("Ex middle developer") is None
    assert extract("Retired senior developer") is None

  def test_extract_adhoc2(self, extract) -> None:
    # Negations affect the behavior
    assert extract("Not a junior developer") is None
    assert extract("Not a senior engineer") is None

  def test_extract_adhoc3(self, extract) -> None:
    # Future markers affect the extractor
    assert extract("One day I will be a senior developer") is None
    assert extract("Middle developer wannabe") is None

  def test_extract_adhoc4(self, extract) -> None:
    # Plus should not be captured by mistake
    assert extract("Senior Backend + Frontend developer") == Experience("Senior", over=False)
    assert extract("Backend + Frontend: 2 years of experience") == Experience("Exact", months=24, over=False)

  def test_extract_adhoc5(self, extract) -> None:
    # Internship
    assert extract("Intern at Microsoft") == Experience("Intern")
    assert extract("Internship at Netflix") == Experience("Intern")
    assert extract("Looking for internship") is None
    assert extract("Open to internship opportunities") is None
    assert extract("Seeking internship") is None

  def test_extract_bios1(self, extract) -> None:
    assert extract("me is Senior fullstack developer") == Experience("Senior")
    assert extract("Full Stack Developer / Founder of Senior Be Hello World") is None
    assert extract("intermediate blockchain engineer") == Experience("Middle")
    assert extract("""
      🍔💻| 1+ year of experience in software development
    """) == Experience("Exact", months=12, over=True)
    assert extract("""
      Senior iOS Developer with more than 12 year of experience.
    """) == Experience("Exact", months=144, over=True)

  def test_extract_bios2(self, extract) -> None:
    assert extract("""
      I am an IT Pro with 30+ years of experience, a multi-year Microsoft MVP, 
      PowerShell author, teacher, and a member of the PowerShell Cmdlet Working Group.
    """) == Experience("Exact", months=360, over=True)
    assert extract("""
      my name kim i'm 15 year old i have many experience penetration testing
    """) is None
    assert extract("""
      IT CONSULTANT | REMOTE SENIOR JAVA SOFTWARE ENGINEER
    """) == Experience("Senior")
    assert extract("17yo dev; @dotcute & @remote-kakao") is None

  def test_extract_bios3(self, extract) -> None:
    assert extract("""
      Principal Engineer working on remote management software
    """) == Experience("Principal")
    assert extract("Head of Mobile, CTO, Founder, #Engineer, #Consultant, #Remote") is None
    assert extract("CTO | Senior Systems Analyst | Hybrid Remote") == Experience("Senior")
    assert extract("Middle+ Android Developer(Looking for Remote Role)") == Experience("Middle", over=True)
    assert extract("Intermediate Site Reliability Engineer, TL") == Experience("Middle")

  def test_extract_bios4(self, extract) -> None:
    assert extract("Junior Dev @ free lance") == Experience("Junior")
    assert extract("A former student at Something") is None
    assert extract("Just a noob") is None
    assert extract("Senior student of Comp Sci @ Concordia University") is None
    assert extract("A 2nd year studxnt of the Higher IT School.") is None
    assert extract("Currently looking for an ML internship") is None

  def test_extract_bios5(self, extract) -> None:
    assert extract("""
      Senior iOS Developer with more than 12 year of experience.
    """) == Experience("Exact", months=144, over=True)
    assert extract("""
      I have one year experience on GitHub
    """) == Experience("Exact", months=12)
    assert extract("""
      Year Up works to close the #OppDivide by providing young adults w/skills, experience, & support that empowers them to reach their potential
    """) is None

  def test_extract_bios6(self, extract) -> None:
    assert extract("""
      Solidity developer with 10+ years experience. CTO at entro.solutions
    """) == Experience("Exact", months=120, over=True)
    assert extract("""
      company founder at 18yo, programmer, game developer, VR enthusiast
    """) is None
    assert extract("""
      Full stack software engineer. Freelance. Some time ago: CTO & co-founder at Nightset
    """) is None
    assert extract("""
      3.5 + Year Experience Swift 4 iOS Developer
    """) == Experience("Exact", months=42, over=True)

  def test_extract_bios7(self, extract) -> None:
    assert extract("""
      Full-stack junior software developer, system administrator and IT consultant.
    """) == Experience("Junior")
    assert extract("""
      My name is Devin and I am a Senior Gameplay Designer at
      CD Projekt Red working on the next Witcher.
    """) is None # He's a "Senior Designer", we extract only DEV experience!
    assert extract("""
      rookie frontend developer
    """) is None
    assert extract("Middle aged man") is None

  def test_extract_bios8(self, extract) -> None:
    assert extract("""
      Senior Manager, Senior Program/Project Manager, Junior Developer wannabe
    """) is None
    assert extract("""
      This is Mishu Dhar Chando. Having More than 2 Year Experience at Data Science, 
      Machine Learning, Image Processing, Natural Language Processing
    """) == Experience("Exact", months=24, over=True)
    assert extract("""
      About I have 5-year experience in Android native app development 
      and 5-year experience in Flutter and 2-year experience in game development using Unity3D
    """) is None
    assert extract("""
      Front-end developer with a background in history and teaching, experience as an ESL tutor, 
      and 8-year experience in BNDES. Amateur musician
    """) == Experience("Exact", months=96)

  def test_extract_bios9(self, extract) -> None:
    assert extract("""
      WEB3 user and 3 Year+ Experience in crypto.
    """) == Experience("Exact", months=36, over=True)
    assert extract("""
      Front-end & WordPress developer, UX consultant. 
      Making stuff for the web since 2005
    """) is None # not capturing phrases like this
    assert extract("""
      I have transformed years of freelancing into a full-time career
    """) is None # not capturing phrases like this
    assert extract("""
      Hi, I am 22 years old freelance full-stack developer from Czech Republic.
    """) is None

  def test_extract_bios10(self, extract) -> None:
    assert extract("""
      Backend Developer 4 Year Experience
    """) == Experience("Exact", months=48)
    assert extract("""
      Application Developer(Android and Flutter ) || 3+ Year Experience
    """) == Experience("Exact", months=36, over=True)
    assert extract("Just a senior middle school student.") is None
    assert extract("I'm a senior at Middle Tennessee State University.") is None

  def test_extract_bios11(self, extract) -> None:
    assert extract("Senior Data Scientist at Capgemini Middle East") == Experience("Senior")
    assert extract("Cloud Platform Maintenance Senior System Administrator") == Experience("Senior")
    assert extract("Middle-Senior Infrastructure Engineer") == Experience("Middle", over=True)
    assert extract("I was an Middle-Senior Infrastructure Engineer") is None

  def test_extract_bios12(self, extract) -> None:
    assert extract("Middle 1C Developer. Junior DevOps") is None
    assert extract("Junior/Middle PHP coder, Laravel abuser") == Experience("Junior", over=True)
    assert extract("I'm a junior+/middle python developer") == Experience("Junior", over=True)
    assert extract("Senior @ Middle East Technical University") == Experience("Senior")
    # Hi! I am a PHP junior+/middle; C#, Python junior developer.

  def test_extract_bios13(self, extract) -> None:
    assert extract("""
      Middle Frontend developer and Junior Backend developer Node js :)
    """) is None
    assert extract("Junior/middle vue frontender") == Experience("Junior", over=True)
    # (Junior) < (frontender), (middle) < (vue) -- works despite this Spacy issue

  def test_extract_bios14(self, extract) -> None:
    assert extract("Middle 1C Developer. Junior DevOps") is None
    assert extract("""
      Senior Android (Kotlin and Java). - Middle IOS (Swift)
    """) is None
    assert extract("""
      I code JavaScript, TypeScript, React, Vue, Angular. Middle -> Senior
    """) == Experience("Middle", over=True)
    # assert extract("""
    #   Middle in Python, senior in Structured Data Analysis
    # """) is None TODO

  def test_extract_bios15(self, extract) -> None:
    assert extract("Senior Unity Game developer; Middle .NET Software Engineer;") is None
    assert extract("Middle Frontend developer and Senior Backend developer.") is None
    assert extract("Middle CV engineer and senior python lover") is None
    assert extract("Middle C#; Junior Asp.Net, Java") is None
    assert extract("Junior Researcher, Senior Lecturer.") == Experience("Junior")

  def test_extract_bios16(self, extract) -> None:
    assert extract("Junior Developer, Senior Project Manager") == Experience("Junior")
    assert extract("SysOps middle") == Experience("Middle")
    assert extract("Middle Software Engineer/Junior Data Scientist") is None
    assert extract("Junior Developer and Senior Deployment Analyst.") is None
    assert extract("Junior Full-Stack Web Developer • Senior Architect") is None

  def test_extract_bios17(self, extract) -> None:
    assert extract("""
      Roblox Studio Junior Developer / Middle Web Developer / UFAL - Computer Science
    """) is None
    assert extract("""
      Co-Founder @wedoappma # Senior Software Engineer | PHP Laravel & Symfony | Junior DevOps
    """) is None
    assert extract("""
      SourcePawn - Senior, Java/Android - Junior, Fullstack - Middle.
    """) is None
    assert extract("""
      General QA Engineer / Middle Python backend dev / Junior Kotlin mobile dev
    """) is None

  def test_extract_bios18(self, extract) -> None:
    # assert extract("SysOps middle / DevOps junior") is None
    # (junior) < (middle) -- Spacy issue
    assert extract("""
      Maxim, 28yo, Junior+/Middle-, React, Node JS developer
    """) == Experience("Junior", over=True)
    assert extract("Strong Junior | Middle developer") == Experience("Junior", over=True)
    assert extract("""
      Middle+/Senior Frontend Developer EdTech | FinTech | Web3"
    """) == Experience("Middle", over=True)

  def test_extract_known_issues1(self, extract) -> None:
    assert extract("Middle Software Engineer IUT Senior") is None
    # ^ Senior is ROOT

  # def test_extract_known_issues2(self, extract) -> None:
  #   pass

    # AR/VR/MR, Senior Unity .Net Developer, Junior C++ Unreal Dev, OpenGl, Shaders(HLSL/Cg)
    #
    # Senior Front-End Developer Junior Back-End Developer 2b || !2b

    # assert extract("""
    #   Working remotely for over 10 years
    # """)  == [Experience("Exact", months=120, over=True)]
    # 9 years of working experience as a software developer.
    # -> 9 years
    # (9) < (years*) > (of) > (experience)
    # I have been working with PHP/Laravel and JavaScript/Node.js, AWS and Firebase for +8 years.
    # (+8) < (years) < (for) < (working*)
    # Full Stack Developer for 25 years currently working for a private company that doesn't use Github.
    # (25) < (years) < (for) < (working*)
    # A font-end expert with 17 years working experience.
    # (17) < (years) < (with) < (expert*), (working) < (experience) < (expert*)
    # -- non-parsable?
    # DevOps Engineer with + 15 years working in startups and multinational companies
    # (+) < (with) < (engineer), (15) < (years) < (with) < (Engineer), (working) < (Engineer)
    # -- similar to above, hard to parse?!
    # I've been working for an internet service company 10+ years
    # (10) < (company), (+) < (years) < (working)
    # -- another somewhat tricky case, numbers are unrelated to years, likely a Spacy mistake
    # Talented Engineer with more than 9 years' experience in the Machine Learning and Data Science fields.
    # In addition to working as a web developer for 14 years.
    # -> 9+, 14 years
    # (14) < (years) < (for) < (working)

# TODO

# a) "10+ years in IT. Main fields: ML, Data Engineering. Also: MlOps, CI/CD, Cloud Platforms (AWS)"
# b) "I am in WordPress and Magento development since past 5 years."
# c) Senior Technical Consultant resided in the Big Apple
