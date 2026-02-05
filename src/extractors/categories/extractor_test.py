# mypy: disable-error-code=no-untyped-def
from dataclasses import dataclass
import pytest
from spacy import Language
from ..utils import fix_grammar, normalize
from .data import TAGS
from .extractor import Categorized, CategoryExtractor, CategorizedRole

@dataclass
class Cats(Categorized):
  role: CategorizedRole | None = None
  is_freelancer: bool | None = None
  is_lead: bool | None = None
  is_remote: bool | None = None
  is_hireable: bool | None = None

class Test_CategoryExtractor:
  @pytest.fixture(scope="class")
  def extract(self, nlp: Language):
    ex = CategoryExtractor(nlp, TAGS)
    def do(text: str) -> Categorized:
      cats = ex.extract(fix_grammar(normalize(text)))
      return Cats(
        role = cats.role,
        is_freelancer = cats.is_freelancer,
        is_lead = cats.is_lead,
        is_remote = cats.is_remote,
        is_hireable = cats.is_hireable
      )
    return do

  def test_extract_smoke(self, extract) -> None:
    assert extract("I'm a someone") == Cats()
    assert extract("I'm a student and a freelancer") == Cats("Student", is_freelancer=True)
    assert extract("I'm a lead engineer") == Cats("Dev", is_lead=True)
    assert extract("I'm a freelance manager") == Cats("Nondev", is_freelancer=True)
    assert extract("I'm an engineer and an MBA graduate") == Cats("Dev")
    assert extract("I'm a MIT graduate, soon to become an engineer") == Cats("Student")
    assert extract("I'm a freelance developer") == Cats("Dev", is_freelancer=True)
    # Testing overlaps
    assert extract("I'm a Dev") == Cats("Dev")
    assert extract("I'm an Ops") == Cats("Dev")
    assert extract("I'm an dev ops") == Cats("Dev")
    assert extract("I'm an devops") == Cats("Dev")

  def test_extract_remote1(self, extract) -> None:
    assert extract("Remote Software Engineer").is_remote is True
    assert extract("Machine Learning Engineer (Remote Worker)").is_remote is True
    assert extract("Looking for opportunities in remote startup").is_remote is True
    assert extract("work with remote sensing and photogrametry and GIS").is_remote is None
    assert extract("Professor, Remote Sensing").is_remote is None
    assert extract("Collaborative, remote project practice for early career developers").is_remote is True

  def test_extract_remote2(self, extract) -> None:
    assert extract("in search of a remote job").is_remote is True
    assert extract("remote job seeking...").is_remote is True
    assert extract("Android developer; remote worker. Based in Scotland").is_remote is True
    assert extract("Teaching code remote").is_remote is True
    assert extract("Writing code remotely").is_remote is True

  def test_extract_remote3(self, extract) -> None:
    assert extract("Accept Freelancer. Remote only!").is_remote is True
    assert extract("PHP & Laravel Developer. Open to remote.").is_remote is True
    assert extract("Remote Fullstack Software Engineer").is_remote is True
    assert extract("A list of semi to fully remote-friendly companies in tech").is_remote is True
    assert extract("The future of tech is Remote.").is_remote is True

  def test_extract_remote4(self, extract) -> None:
    assert extract("Remote Software Engineer @ Resilience").is_remote is True
    assert extract("Software Engineer | Flutter Developer | IoT Researcher | Open for Remote Job").is_remote is True
    assert extract("iOS Developer | Remote").is_remote is True
    assert extract("17yo dev; @dotcute & @remote-kakao").is_remote is None
    assert extract("# FE Engineer @ remote.com Prev: Panalyt.com").is_remote is None
    assert extract("EE,PhD,Remote Sensing and GIS developer").is_remote is None

  def test_extract_remote5(self, extract) -> None:
    assert extract("baby girl's father. Looking for a remote work opportunity").is_remote is True
    assert extract("remote haskell developer").is_remote is True
    assert extract("Blockchain Developer Remote/Online").is_remote is True
    assert extract("Remote @ShadowShahriar").is_remote is True
    assert extract("Hacker. Pioneered BlindXSS, Remote git/hg/bzr Pillaging").is_remote is None
    assert extract("0fficial_BlackHat13 Remote_Code_Execution 0day Exploit").is_remote is None

  def test_extract_remote6(self, extract) -> None:
    assert extract("With great responsibility comes great power | Remote working").is_remote is True
    assert extract("Head of Mobile, #Android, #Engineer, #CS, #GO, #Consultant, #Remote").is_remote is True
    # assert extract("IT CONSULTANT | REMOTE SENIOR JAVA SOFTWARE ENGINEER").is_remote is True
    # TODO
    assert extract("CEO/co-founder of Tuple, a tool for remote pair programming").is_remote is None
    assert extract("Principal Engineer working on remote management software").is_remote is None

  def test_extract_remote7(self, extract) -> None:
    assert extract("CTO | Senior Systems Analyst | Hybrid Remote").is_remote is True
    assert extract("Did learn coding remotely. Now Looking for a remote job").is_remote is True
    assert extract("Remote access everywhere").is_remote is None
    assert extract("Access remotely everywhere").is_remote is None

  def test_extract_remote8(self, extract) -> None:
    assert extract("Remote. Building stuff with Typescript, Lua, and Swift.").is_remote
    assert extract("Remote iOS Developer").is_remote
    assert extract("Senior Android Developer(Looking for Remote Role)").is_remote
    assert extract("Remote tech").is_remote is None
    assert extract("Remotely possible").is_remote is None

  def test_extract_remote9(self, extract) -> None:
    assert extract("Full Stack Web Developer | Remote enthusiast | Associate").is_remote
    assert extract("Software Developer, React JS lover. Looking for new challenges in remote projects.").is_remote
    assert extract("Want to join a remote project.").is_remote
    assert extract("Wish to lead a remote position.").is_remote

  def test_extract_remote10(self, extract) -> None:
    assert extract("Open for new opportunities").is_hireable is True
    assert extract("Open for hiring").is_hireable is True
    assert extract("Hireable").is_hireable is True
    assert extract("#Hireable").is_hireable is True
    assert extract("Open to work").is_hireable is True
    assert extract("=OpenToWork=").is_hireable is True
    assert extract("Not open for new opportunities").is_hireable is False
    assert extract("Not hireable").is_hireable is False
    assert extract("Not #Hireable").is_hireable is True # by design
    assert extract("Not open to work").is_hireable is False
    assert extract("Foo bar open").is_hireable is None

  def test_extract_hireable1(self, extract) -> None:
    assert extract("Blah. Hireable. Blah").is_hireable is True
    assert extract("I'm hireable").is_hireable is True
    assert extract("She is hireable").is_hireable is True
    assert extract("hire-able").is_hireable is True
    assert extract("not hire able").is_hireable is False
    assert extract("This tool is to make everyone hireable").is_hireable is True # known FP

  def test_extract_hireable2(self, extract) -> None:
    assert extract("open to future challenges").is_hireable is True
    assert extract("not open to future challenges").is_hireable is False
    assert extract("always open to work").is_hireable is True
    assert extract("not open to work").is_hireable is False
    assert extract("open for hire").is_hireable is True
    assert extract("not open for hire").is_hireable is False

  def test_extract_hireable3(self, extract) -> None:
    assert extract("hire-able").is_hireable is True
    assert extract("not hire able").is_hireable is False
    assert extract("This tool is to make everyone hireable").is_hireable is True # known FP
    assert extract("Open to hiring").is_hireable is True
    assert extract("Open to new ideas").is_hireable is True
    assert extract("Open to job offers").is_hireable is True
    assert extract("Open to work proposal").is_hireable is True
    assert extract("Open to proposals").is_hireable is True
    assert extract("Open to something").is_hireable is None

  def test_extract_hireable4(self, extract) -> None:
    assert extract("Open to opportunities").is_hireable is True
    assert extract("Open to new opportunities").is_hireable is True
    assert extract("Open for interesting opportunities").is_hireable is True
    assert extract("Open to collaborations").is_hireable is True
    assert extract("Open to future challenges").is_hireable is True
    assert extract("Open to future enquiries").is_hireable is True
    assert extract("Open for professional project enquiry").is_hireable is True
    assert extract("Currently open to an opportunity").is_hireable is True
    assert extract("Currently not open to an opportunity").is_hireable is False

  def test_extract_hireable5(self, extract) -> None:
    assert extract("ready to be hired").is_hireable is True
    assert extract("not ready to be hired").is_hireable is False
    assert extract("She is hireable").is_hireable is True
    assert extract("She is not hireable").is_hireable is False
    assert extract("Open for relocation").is_hireable is True
    assert extract("Open for something").is_hireable is None
    assert extract("Not open for relocation").is_hireable is False
    assert extract("Open to internship and job").is_hireable is True

  def test_extract_hireable6(self, extract) -> None:
    assert extract("#hireme").is_hireable is True
    assert extract("please hire me").is_hireable is True
    assert extract("Interested in hiring me?").is_hireable is True
    assert extract("Whether you hire me or not, I am overly committed").is_hireable is True

  def test_extract_hireabl7(self, extract) -> None:
    assert extract("Seeking new job opportunities").is_hireable is True
    assert extract("Seeking new work possibilities").is_hireable is True
    assert extract("Seeking well paid job options").is_hireable is True
    assert extract("not seeking a job").is_hireable is False
    assert extract("not seeking an work").is_hireable is False
    assert extract("not seeking anything").is_hireable is None

  def test_extract_hireable8(self, extract) -> None:
    assert extract("looking for job opportunities").is_hireable is True
    assert extract("looking for new options").is_hireable is True
    assert extract("looking for a position").is_hireable is True
    assert extract("not looking for opportunities").is_hireable is False
    assert extract("looking for something").is_hireable is None

  def test_extract_hireable9(self, extract) -> None:
    assert extract("looking for job opportunities").is_hireable is True
    assert extract("looking for new options").is_hireable is True
    assert extract("looking for a position").is_hireable is True
    assert extract("Looking for a job now.").is_hireable is True
    assert extract("not looking for opportunities").is_hireable is False
    assert extract("looking for something").is_hireable is None

  def test_extract_hireable10(self, extract) -> None:
    assert extract("jobseeker").is_hireable is True
    assert extract("job seeker").is_hireable is True
    assert extract("job-seeker").is_hireable is True
    assert extract("not jobseeker").is_hireable is False
    assert extract("not a job seeker").is_hireable is False
    assert extract("not a job-seeker").is_hireable is False
    # assert extract("jobseeking").is_hireable is True
    # assert extract("job seeking").is_hireable is True
    # assert extract("job-seeking").is_hireable is True
    # assert extract("not jobseeking").is_hireable is False
    # assert extract("not job seeking").is_hireable is False
    # assert extract("not job-seeking").is_hireable is False

  def test_extract_hireable11(self, extract) -> None:
    assert extract("Open to AI/ML Roles").is_hireable is True
    assert extract("Open to a leadership role").is_hireable is True
    assert extract("JS, React, Angular; open to relocation").is_hireable is True
    assert extract("Open to new challenges💻").is_hireable is True
    assert extract("looking for job options intern etc.").is_hireable is True
    assert extract("Digital Entrepreneur | Code Lover | Open for New Opportunities").is_hireable is True
    assert extract("Open for Hire - Full-Stack Software Developer | building railsinit.org").is_hireable is True

  def test_extract_hireable12(self, extract) -> None:
    assert extract("you can hire me if you want").is_hireable is True
    assert extract("Software Developer, seeking new employment possibilities").is_hireable is True
    assert extract("Seeking challenging employment opportunities").is_hireable is True
    assert extract("Looking for new #rstats opportunities").is_hireable is True
    assert extract("Student. Looking for internships.").is_hireable is True

  def test_extract_hireable13(self, extract) -> None:
    assert extract("Computer Engineer. Seeking remote contract work.").is_hireable is True
    assert extract("Web developer. Always seeking contract work. Available via Telegram").is_hireable is True
    assert extract("Professional UI/UX Designer, I Am Ready for hire.").is_hireable is True
    assert extract("Mobile Apps & Web Developer | Freelancer | Ready for Hire").is_hireable is True
    assert extract("Don't try to hire me").is_hireable is False
    assert extract("You can not hire me.").is_hireable is False

  def test_extract_hireable14(self, extract) -> None:
    assert extract("See this: I AM NOT HIREABLE").is_hireable is False
    assert extract("If you enjoy my open source work...").is_hireable is None
    assert extract("Open to interpretation").is_hireable is None
    assert extract("An open source ecosystem to liberate the work").is_hireable is None
    assert extract("A tool to hire best developers. Myself included ;").is_hireable is None
    assert extract("🚀Open To You! 🚀").is_hireable is None

  def test_extract_hireable15(self, extract) -> None:
    assert extract("I am non hireable").is_hireable is False
    assert extract("always seeking for a job").is_hireable is True
    assert extract("Open to Organizations !").is_hireable is None
    assert extract("🈺 open for business! 🈺").is_hireable is None
    assert extract("🏻 Web Developer | JS ❤ ~ Always open to learn").is_hireable is None
    assert extract("Connect the world of science. Make research open to all.").is_hireable is None
    assert extract("Looking for teleportation").is_hireable is None

  def test_extract_hireable16(self, extract) -> None:
    assert extract("What are you looking for and what am I looking for?").is_hireable is None
    assert extract("Looking for the next big thing.").is_hireable is None
    assert extract("I'm looking for: Ruby Ninjas,Ember.js Masters, Python Dev, QAs ...if you're one of them, just let me know!").is_hireable is None
    assert extract("I'm a highly motivated Ninja. Always looking for new things to learn.").is_hireable is None

  def test_extract_hireable17(self, extract) -> None:
    assert extract("Just for fun. Not hirable.").is_hireable is False
    assert extract("I'm not for hire. Thank you for your cooperation").is_hireable is False
    assert extract("Freelance Programmer | Not for Hire").is_hireable is False
    assert extract("@ zhakky studios not hire able.").is_hireable is False
    assert extract("Looking for a PhD position!").is_hireable is True
    assert extract("Working on VR Game w/kobugindustries (Not an expert) NOT FOR HIRE").is_hireable is False

  def test_extract_lead1(self, extract) -> None:
    assert extract("#teamlead").is_lead is True
    assert extract("Engineering Leader").is_lead is True
    assert extract("AI Thought Leader | Cognitive Architecture | Heuristic Imperatives").is_lead is True
    assert extract("Tech leader").is_lead is True
    assert extract("Open Source Enthusiast, Project Leader @OWASP Chapter Leader @OWASP").is_lead is True
    assert extract("Mobile Platform Technical Leader - iOS Engineer").is_lead is True
    assert extract("Team Leader Manager").is_lead is True
    assert extract("People first leader and indie hacker.").is_lead is True
    assert extract("Leader of Ukrainian Rust Community").is_lead is True

  def test_extract_lead2(self, extract) -> None:
    assert extract("Leading anti-cheat @ someplace.").is_lead is True
    assert extract("Software Engineer at @microsoft leading the Copilot UX team").is_lead is True
    assert extract("Designer Developer from Ireland, leading design and dev teams in SF.").is_lead is True
    assert extract("Into kubernetes, typescript, golang, microservices, and leading teams.").is_lead is True
    assert extract("Tech stuff at Leadingly LLC").is_lead is None
    # assert extract("mechanical engineer with leading skills").is_lead is None -- TODO another Spacy post-norm, dep. mistake, retrain!
    assert extract("Building leading data science tools and state-of-the-art ML models").is_lead is None

  def test_extract_lead3(self, extract) -> None:
    assert extract("CTO at entro.solutions").is_lead is None
    assert extract("CEO at Microsoft").is_lead is None
    assert extract("VP at Facebook").is_lead is None
    assert extract("SVP at Netflix").is_lead is None
    assert extract("Not a lead").is_lead is False
    assert extract("ex-lead of GitHub QA team").is_lead is False

  def test_extract_lead4(self, extract) -> None:
    assert extract("Creating market-leading software products").is_lead is None
    assert extract("All roads leading to humanoids").is_lead is None
    assert extract("Leading a life long learning expedition").is_lead is None
    # FPs
    assert extract("Leading talent to expertise").is_lead is True
    assert extract("Captain leading from the front!").is_lead is True

  def test_extract_lead5(self, extract) -> None:
    assert extract("TL, JavaScript Developer").is_lead is True
    assert extract("CTO, TL") .is_lead is True
    assert extract("Typographer, Tech Lead").is_lead is True
    assert extract("Senior Site Reliability Engineer, TL").is_lead is True
    assert extract("TL;DR : DJ turned software engineer").is_lead is None
    assert extract("Founder and SVP Creative at Frac.tl").is_lead is None

  # FREELANCER
  def test_extract_freelancer1(self, extract) -> None:
    assert extract("freelance").is_freelancer is True
    assert extract("free lance").is_freelancer is True
    assert extract("free-lance").is_freelancer is True
    assert extract("freelancer").is_freelancer is True
    assert extract("free lancer").is_freelancer is True
    assert extract("free-lancer").is_freelancer is True
    assert extract("I am freelancer").is_freelancer is True
    assert extract("I am a free-lancer").is_freelancer is True
    assert extract("#java #freelancer").is_freelancer is True

  def test_extract_freelancer2(self, extract) -> None:
    assert extract("Junior Dev @ free lance").is_freelancer is True
    assert extract("open to freelance work").is_freelancer is True
    assert extract("seeking remote freelance jobs").is_freelancer is True
    assert extract("ready to freelance opportunities").is_freelancer is True
    assert extract("considering projects as a freelancer").is_freelancer is True

  def test_extract_freelancer3(self, extract) -> None:
    assert extract("Weblancer").is_freelancer is None
    assert extract("freelancim").is_freelancer is None
    assert extract("freelancing").is_freelancer is True

  # ROLE
  def test_extract_role1(self, extract) -> None:
    assert extract("I'm learning Python at the moment").role == "Student"
    assert extract("Learning PHP at the moment").role == "Student"
    assert extract("Carl is studying Django this month").role == "Student"
    assert extract("Adapt is a global, open-source e-learning project aiming to...").role is None
    assert extract("Deep learning resources, including pretrained...").role is None
    assert extract("Making developers awesome at machine learning").role is None

  def test_extract_role2(self, extract) -> None:
    assert extract("Studying to become a therapist.").role == "Student"
    assert extract("Learning the things.").role == "Student"
    assert extract("Currently studying React Ecosystem").role == "Student"
    assert extract("MIT CSAIL's Learning and Intelligent Systems Group").role is None
    assert extract("the Learning&Training Hub of OS Kernel for Students & Developers").role is None
    assert extract("Great Learning is an online learning platform designed to...").role == "Org"
    assert extract("The GitHub repo for Learning Go by Jon Bodner").role is None

  def test_extract_role3(self, extract) -> None:
    assert extract("Studying Bio-medical engineering at Cairo University").role == "Student"
    assert extract("17, studying CS.").role == "Student"
    assert extract("Studying Software Engineering at Yunnan University China").role == "Student"
    assert extract("Studying cybersecurity").role == "Student"
    assert extract("frantically studying the world").role is None
    assert extract("Machine Learning Nut.").role is None
    assert extract("Forever learning").role is None
    assert extract("Always studying").role is None
    assert extract("Never stop studying.").role is None

  def test_extract_role4(self, extract) -> None:
    assert extract("Eternal student").role is None
    assert extract("Future student").role == "Student"
    assert extract("Aspiring Analyst").role == "Student"
    assert extract("Future engineer").role == "Student"
    assert extract("Front-end Developer 👩‍💻 \nPlatzi Student 💚 \nSoftware Engineer").role == "Dev"
    assert extract("Frontend dev by day, backend student by night").role == "Dev"

  def test_extract_role5(self, extract) -> None:
    assert extract("Formerly a student at Something").role is None
    assert extract("A former student at Something").role is None
    assert extract("Programming newbie").role == "Student"
    assert extract("Just a noob").role == "Student"
    assert extract("Just a beginner").role == "Student"
    assert extract("Mobile novice").role == "Student"
    assert extract("Blockchain noob").role == "Student"

  def test_extract_role6(self, extract) -> None:
    assert extract("Computer Engineer & MSc Student").role == "Dev"
    assert extract("Bachelor student of Comp Sci @ Concordia University").role == "Student"
    assert extract("Bachelor of Comp Sci student @ Concordia University").role == "Student"
    assert extract("Private Pilot | Bachelor of Science").role == "Student"
    assert extract("MSCS Student").role == "Student"

  def test_extract_role7(self, extract) -> None:
    assert extract("Computer science masters graduate with a specialization in Data Science.").role == "Student"
    assert extract("Data science undergraduate, proficient in Computer Science.").role == "Student"
    assert extract("I am a passionate student who loves to learn and explore").role == "Student"
    assert extract("undergraduate student of Tongji university").role == "Student"
    assert extract("Undergraduate at UC Berkeley, double major in CS and Math.").role == "Student"
    assert extract("Formerly Stanford CS PhD Student.").role is None

  def test_extract_role8(self, extract) -> None:
    assert extract("A 2nd year studxnt of the Higher IT School.").role is None
    assert extract("Currently looking for an ML internship").role == "Student"
    assert extract("I want to be a data analyst").role == "Student"
    assert extract("I want to become a computer scientist").role == "Student"
    assert extract("Computer Science Major at NAU").role == "Student"
    assert extract("Computer science major at Stockton university").role == "Student"

  def test_extract_role9(self, extract) -> None:
    assert extract("Technical Artist. Founder of @Golden-Ram-Studio").role == "Nondev"
    assert extract("Manager, developer, and designer walk into bar").role == "Nondev"
    assert extract("A student of life, working as a QA at a Bay Area").role == "Dev"
    assert extract("Life-long student").role is None
    assert extract("Perpetual student").role is None

  def test_extract_role10(self, extract) -> None:
    assert extract("UI/UX designer -  Front Stack - iOS/SwiftUI developer").role == "Nondev"
    assert extract("iOS/SwiftUI developer and UI/UX designer").role == "Dev"
    assert extract("Business Analyst | MBA Student").role == "Dev"
    assert extract("Constant student").role is None
    assert extract("I was a student").role is None

  def test_extract_role11(self, extract) -> None:
    assert extract("Marketing/Data Analyst").role == "Dev"
    assert extract("Yet another software dev").role == "Dev"
    assert extract("community").role == "Org"
    assert extract("community contributor").role is None
    assert extract("Software development done right").role is None

  def test_extract_role12(self, extract) -> None:
    assert extract("Intern at Microsoft").role == "Student"
    assert extract("Internship at Netflix").role == "Student"
    assert extract("Solidity developer with 10+ years experience. CTO at entro.solutions").role == "Dev"
    assert extract("company founder at 18yo, programmer, game developer, VR enthusiast").role == "Nondev"
    assert extract("Fullstack web design agency").role == "Org"

  def test_extract_role13(self, extract) -> None:
    assert extract("✒️ Co-founder of CollBoard.com").role == "Nondev"
    assert extract("Founder").role == "Nondev"
    assert extract("Cofounder").role == "Nondev"
    assert extract("Co founder").role == "Nondev"
    assert extract("Co-founder").role == "Nondev"
    assert extract("Engineer").role == "Dev"
    assert extract("Developer").role == "Dev"

  def test_extract_role14(self, extract) -> None:
    assert extract("Dev").role == "Dev"
    assert extract("Programmer").role == "Dev"
    assert extract("Coder").role == "Dev"
    assert extract("Mentor").role == "Nondev"
    assert extract("Teacher").role == "Nondev"
    assert extract("Lecturer").role == "Nondev"
    assert extract("Mathematician").role == "Dev"

  def test_extract_role15(self, extract) -> None:
    assert extract("Agency").role == "Org"
    assert extract("Company").role == "Org"
    assert extract("Group").role == "Org"
    assert extract("Organization").role == "Org"

  def test_extract_role16(self, extract) -> None:
    assert extract("Head of Design @github.").role == "Nondev"
    assert extract("Growth Head").role == "Nondev"
    assert extract("permanent head damage").role is None
    assert extract("Author of Head First Ruby").role is None
    assert extract("head in ☁️").role is None

  def test_extract_set17(self, extract) -> None:
    assert extract("Bachelor").role == "Student"
    assert extract("Bachelor student").role == "Student"
    assert extract("Bachelor student engineer").role == "Student"
    assert extract("Bachelor engineer student").role == "Student"
    assert extract("Bachelor engineering student").role == "Student"
    assert extract("BS engineering student").role == "Student"
    assert extract("B.S engineering student").role == "Student"
    assert extract("B.Sc engineering student").role == "Student"
    assert extract("Master-of-Science engineering student").role == "Student"
    assert extract("MS engineering student").role == "Student"
    assert extract("M.S engineering student").role == "Student"
    assert extract("M.Sc engineering student").role == "Student"

  def test_extract_adhoc1(self, extract) -> None:
    assert extract("Software Engineering student") == Cats("Student")
    assert extract("Eng student") == Cats("Student")
    assert extract("Software Engineer student") == Cats("Student")
    assert extract("Project management is not for everyone") == Cats()

  def test_extract_adhoc2(self, extract) -> None:
    assert extract("Engineering leadership at Square") == Cats(is_lead=True)
    assert extract("open to freelance remote work") == Cats(is_remote=True, is_hireable=True, is_freelancer=True)
    assert extract("ex-Facebook BFDL. Now tech-lead at @AWS") == Cats(is_lead=True)
    assert extract("ex-Yandex padavan. Now teamlead at @Google") == Cats(is_lead = True)
    assert extract("Formerly a manager at Foo. Now a student at Bar") == Cats("Student")

  def test_extract_adhoc3(self, extract) -> None:
    assert extract("Opened to remote job offers") == Cats(is_remote=True, is_hireable=True)
    assert extract("Currently open to remote / relocated job offers.") == Cats(is_remote=True, is_hireable=True)
    assert extract("Deep learning ftw") == Cats()

  def test_extract_adhoc4(self, extract) -> None:
    assert extract("Former Dev Student") == Cats()
    assert extract("Ex Engineer Student") == Cats()
    assert extract("Former Eng VP") == Cats()
    assert extract("Ex Dev President") == Cats()

  # BIOs
  def test_extract_bios1(self, extract) -> None:
    assert extract("""
      Full stack software engineer. Freelance. Some time ago: CTO & co-founder at Nightset
    """) == Cats("Dev", is_freelancer=True)
    assert extract("""
    Freelance. Some time ago: CTO & co-founder at Nightset
    """) == Cats(is_freelancer = True)
    assert extract("""
      Game developer, programmer, bit of an artist; C++, Unreal
    """) == Cats("Dev")

  def test_extract_bios2(self, extract) -> None:
    assert extract("Environmental student, Unreal Engine developer") == Cats("Student")
    assert extract("""
      Software engineer working on games, and tools. Currently leading UI on Clip It @ Neura Studios.
    """) == Cats("Dev", is_lead=True)
    assert extract("""
      Founder and CEO of @rangle , the leading lean/agile JavaScript consulting firm.
    """) == Cats("Nondev")

  def test_extract_bios3(self, extract) -> None:
    assert extract("Machine learning engineer") == Cats("Dev")
    assert extract("Just learning here...") == Cats("Student")
    assert extract("Studying devops for fun and profit.") == Cats("Student")
    assert extract("Peter is a remote jobseeker") == Cats(is_remote=True, is_hireable=True)
    assert extract("Freelance Programmer | Not for Hire") == Cats("Dev", is_freelancer=True, is_hireable=False)

  def test_extract_bios4(self, extract) -> None:
    assert extract("""
      Freelance open source developer. Hire me!
    """) == Cats("Dev", is_freelancer=True, is_hireable=True)
    assert extract("""
      I am a freelance front-end developer. you can hire me
    """) == Cats("Dev", is_freelancer=True, is_hireable=True)
    assert extract("""
      Mobile Apps & Web Developer | Freelancer | Ready for Hire
    """) == Cats("Dev", is_freelancer=True, is_hireable=True)
    assert extract("Remote tech hiring, everywhere.") == Cats()

  def test_extract_bios5(self, extract) -> None:
    assert extract("""
      Frontend + DevOp! web3 / DeFi, TypeScript, React/Next/Nest, ex. freelancer
    """) == Cats("Dev", is_freelancer=False)
    assert extract("Ex freelancer at Bay, forever student") == Cats(is_freelancer=False)

  def test_extract_bios6(self, extract) -> None:
    assert extract("Yandex.Fintech | ITMO SWE '25") == Cats("Dev")
    assert extract("Retired backend engineer") == Cats()
    assert extract("I am a data scientist with a passion for learning") == Cats("Dev")
    assert extract("Computer science newbie") == Cats("Student")
    assert extract("CMC MSU bachelor's degree, FCS HSE master student, ex-Data Scientist at Tinkoff bank") == Cats("Student")

  def test_extract_bios7(self, extract) -> None:
    assert extract("Working as a Technical Recruiter!") == Cats("Nondev")
    assert extract("New software developer.") == Cats("Dev")
    assert extract("I'm studying data analytics and here are my first projects") == Cats("Student")
    assert extract("Hello. I'am Vadim Tikhonov. I study code, data analysis and data science.") == Cats("Student")
    assert extract("I am new to ML & DL") == Cats("Student")
    assert extract("Romero is seeking new opportunities;") == Cats(is_hireable=True)

  def test_extract_bios8(self, extract) -> None:
    assert extract("Aspiring Python Data Analyst") == Cats("Student")
    assert extract("CS Undergrad at New Jersey Institute of Technology") == Cats("Student")
    assert extract("Game developer from New Orlean") == Cats("Dev")
    assert extract("Financial University under the government of Russia") == Cats()
    assert extract("Gopher. Former TL of Go CDK and author of Wire.") == Cats("Dev", is_lead=False)

  def test_extract_bios9(self, extract) -> None:
    assert extract("""
      Master of Science in Information Systems student at Stevens Institute of Technology, NJ, USA.
    """) == Cats("Student")
    assert extract("Web developer studying to become a therapist") == Cats("Dev")
    assert extract("Full time Architect, Consultant, Learner, Author") == Cats("Dev", is_freelancer=True)
    assert extract("Engineer, learning PHP at the moment") == Cats("Dev")
    assert extract("I've just learned a bit of HTML & CSS") == Cats() # too contextual

  def test_extract_bios10(self, extract) -> None:
    assert extract("Software Developer learning Systems Analysis and Development.") == Cats("Dev")
    assert extract("Software engineer studying mathematics") == Cats("Dev")
    assert extract("Aspiring engineer studying networking & security.") == Cats("Student")
    # ^ OK "aspiring" cancels "engineer", then "studying" is captured
    # assert is_student("Aspiring 16 y/o software engineer studying networking & security.")
    # ^ Spacy model fails to parse such a long noun phrase properly, needs to be retrained
    assert extract("iOS architect, studying Rust") == Cats("Dev")
    assert extract("Frontend dev who currently learning Rust & Elixir") == Cats("Dev")
    assert extract("Teenager, freelancer, backend developer (TypeScript, C++)") == Cats(
      "Student", is_freelancer = True
    )

  def test_extract_bios11(self, extract) -> None:
    assert extract("""
      daily.dev is a professional network for developers to learn, collaborate, and grow together.
    """) == Cats("Org")
    assert extract("""
      participated in incubating many projects about zero trust and Web3 organization
    """) == Cats()
    assert extract("""
      I am Viktor Klang, a finder, researcher, problem solver, improver of things,
      life-long student, developer/programmer, leader, mentor/advisor, public speaker…
    """) == Cats("Dev", is_lead=True)
    assert extract("""
      Specializing generalist. CS PhD, student of life. Lover of words and hyperbole. Remote.
    """) == Cats("Dev", is_remote=True)

  def test_extract_bios12(self, extract) -> None:
    assert extract("music student java elasticsearch ai subversion git node") == Cats("Student")
    assert extract("Back-End Developer | Information Systems bachelor") == Cats("Dev")
    assert extract("CS Bachelor student at USI") == Cats("Student")
    assert extract("CS Bachelor at USI") == Cats("Student")
    assert extract("""
      Professor of the Practice in Computer Science, Program Director
      for the Fundamentals of Computing Undergraduate Certificate Program
    """) == Cats("Nondev")

  def test_extract_bios13(self, extract) -> None:
    assert extract("""
      NET Developer with front-end skills, Freelancer, Photographer and Science Lover
    """) == Cats("Dev", is_freelancer=True)
    assert extract("Biotech student and sometimes software developer") == Cats("Student")
    assert extract("Software developer and sometimes biotech student") == Cats("Dev")
    assert extract("Everlasting student · Freelance · Life lover") == Cats(is_freelancer=True)
    assert extract("rookie front-end developer") == Cats("Student")

  def test_extract_bios14(self, extract) -> None:
    assert extract("""
      Arman is a full-stack developer who mainly focuses on web development
    """) == Cats("Dev")
    assert extract("""
      Teenager, freelancer, backend developer (TypeScript, C++17)
    """) == Cats("Student", is_freelancer=True)
    assert extract("""
      Game Producer & Lead Development | Network & Systems Admin
    """) == Cats("Nondev", is_lead=True)
    assert extract("""
      Oleg Rybnikov - a freelancing web artisan specializing in Vite
    """) == Cats(is_freelancer=True)

  def test_extract_bios15(self, extract) -> None:
    assert extract("""
      applied artificial intelligence student, free to relocate
    """) == Cats("Student")
    assert extract("""
      🇸🇰 Freelancer full-stack developer. #React #ReactNative
    """) == Cats("Dev", is_freelancer=True)
    assert extract("""
      Full stack software engineer at dextra | Freelancer
    """) == Cats("Dev", is_freelancer=True)
    assert extract("""
      Self-taught Developer graded in Back-end Development. -Freelancer
    """) == Cats("Dev", is_freelancer=True)

  def test_extract_bios16(self, extract) -> None:
    assert extract("indie dev • iOS & macOS • freelance") == Cats("Dev", is_freelancer=True)
    assert extract("Freelancer Jedi Padawan") == Cats(is_freelancer=True)
    assert extract("freelance math teacher, freelance front-end developer") == Cats("Nondev", is_freelancer=True)
    assert extract("I'm a Software Engineer, Ethical Hacker, and security enthusiast") == Cats("Dev")
    assert extract("⭐️ Senior Software Developer ⭐️ Blockchain / Backend / ETL") == Cats("Dev")

  def test_extract_bios17(self, extract) -> None:
    assert extract("AWESOME Developer/Lead") == Cats("Dev", is_lead=True)
    assert extract("Software Dev & Tech Lead") == Cats("Dev", is_lead=True)
    assert extract("Lead Cloud Engineer @ Namecheap") == Cats("Dev", is_lead=True)
    assert extract("Horizon 2020 Project LEAD: Low-Emission logistics") == Cats(is_lead=True)

  def test_extract_bios18(self, extract) -> None:
    assert extract("Technical Content Lead") == Cats(is_lead=True)
    assert extract("IT Sec guy, @zaproxy co-lead") == Cats("Dev", is_lead=True)
    assert extract("Raising the bar for leadership in tech.") == Cats(is_lead=True)
    assert extract("The leading platform for local cloud development") == Cats("Org")

  def test_extract_bios19(self, extract) -> None:
    assert extract("Founder & CEO @QualiSage | Team Lead | Senior Full-Stack Developer") == Cats("Nondev", is_lead=True)
    assert extract("Junior Programmer @BohemiaInteractive | Founder @QX-Interactive") == Cats("Dev")
    assert extract("Lecturer at Rowan University") == Cats("Nondev")
    assert extract("freshman at Rowan University") == Cats("Student")

  def test_extract_bios20(self, extract) -> None:
    assert extract("sophomore at Rowan University") == Cats("Student")
    assert extract("""
      My name is Devin and I am a Senior Gameplay Designer at
      CD Projekt Red working on the next Witcher.
    """) == Cats("Nondev")
    assert extract("""
      Striving to become a front-end developer. Formerly climbing gym founder and co-owner
    """) == Cats("Student")
    assert extract("""
     Founder, CBB Analytics. Sports Data Scientist and Web Developer.
   """) == Cats("Nondev")

  def test_extract_bios21(self, extract) -> None:
    assert extract("""
      Twas brillig, and the slithy toves
      Did gyre and gimble in the wabe
    """) == Cats()
    assert extract("Associate Professor of CS at Augusta University.") == Cats("Nondev")
    assert extract("Head of developer advocacy @pieces-app") == Cats("Nondev")
    assert extract("""
      👨‍💻 developer of 🌐 coora-ai.com 🧭 igapo.xyz / tech enthusiast / applied artificial intelligence student
    """) == Cats("Dev")

  def test_extract_bios22(self, extract) -> None:
    assert extract("""
      👨 VP Eng. at MedScout, storyteller, student of disasters.
    """) == Cats("Nondev")
    assert extract("Freelance ⠁⣿⣿ ⣿⣿⣿ ⣿⣿⣿") == Cats(is_freelancer=True)
    assert extract("SE @ SJSU") == Cats("Dev")
    assert extract("Senior SE") == Cats("Dev")

  def test_extract_known_issues1(self, extract):
    assert extract("Ex-engineer, freelancer") == Cats(is_freelancer=False)
    # (ex) < (freelancer)

  # def test_extract_set37() -> None:
  #   assert extract("Code samples from the book Head First Go").role is None
  #   assert extract("Head Coach @nashville-software-school").role == "Nondev"
  #   assert extract("Head of Engineering @gigs").role == "Nondev"
  #   assert extract("Head of OSS @huggingface. Open Source developer.").role == "Nondev"
  #   assert extract("MY HEAD IS IN THE CLOUD!!").role is None
  #   assert extract("Head of India @lendsmartlabs").role == "Nondev"
  #   assert extract("Head of Technology").role == "Nondev"
  #   assert extract("Head down and build").role is None
  #   assert extract("Head Of Security Research @F5Networks").role == "Nondev"
  #   assert extract("Head of Flickr.").role == "Nondev"
  #
  # def test_extract_set38() -> None:
  #   assert extract("head hurts...").role is None
  #   assert extract("Research Head").role == "Nondev"
  #   assert extract("Hip-hop head... ancora imparo...").role is None
  #   assert extract("Head of DevOps").role == "Nondev"
  #   assert extract("Senior Mentor and Java practice Head, Coding Blocks").role == "Nondev"
  #   assert extract("Head @ Payments by Wix").role == "Nondev"
  #   assert extract("A small baby head with huge headphones.").role is None
  #   assert extract("Batfish @ AWS Former head of engineering @ Intentionet").role is None
  #   assert extract("Physics research head at nvidia").role == "Nondev"
  #   assert extract("Head of Teaching at SALT").role == "Nondev"
  #   assert extract("Head of SRE @Billhop").role == "Nondev"
  #   assert extract("Head of DS @UW").role == "Nondev"
  #   assert extract("Co-Founder and Training Head @AltCampus").role == "Nondev"
  #   assert extract("Hot Headed & Stubborn Programmer").role == "Dev"
  #   assert extract("git reset HEAD~1").role is None
  #   assert extract("Head of Oxford Research Software Engineering").role == "Nondev"
  #
  # def test_extract_set39() -> None:
  #   assert extract("Freelancer and video editor").is_freelancer
  #   assert extract("Full stack developer, tech consultant").is_freelancer
  #   assert extract("Backend SWE & consulting").is_freelancer
  #   assert extract("Java Full-stack Developer at j-labs.pl Crif consultant").is_freelancer
  #   assert extract("Front-end & WordPress developer, UX consultant. Making stuff for the web since 2005").is_freelancer
  #
  # def test_extract_set40() -> None:
  #   assert extract("Frontend Consultant; Web, Mobile and Desktop Applications Developer").is_freelancer
  #   assert extract("My name is Jorens, I'm a Full Stack developer, currently freelancing").is_freelancer
  #   assert extract("WebGL, WebXR, full-stack, consulting").is_freelancer
  #   assert extract("Full-stack junior software developer, system administrator and IT consultant.").is_freelancer
  #   assert extract("I have transformed years of freelancing into a full-time career").is_freelancer
  #   assert extract("Something @ devlance").is_freelancer is None
  #
  # def test_extract_set41() -> None:
  #   assert extract("Freelancer Nasim is a Web Application Developer.").is_freelancer
  #   assert extract("Opensource enthusiast, Skillbox teacher, Blogger").is_freelancer is None
  #   assert extract("Free-lancer @ BYTESADMIN • Security Researcher").is_freelancer
  #   assert extract("Freelance Clojure programmer").is_freelancer
  #
  # def test_extract_set43() -> None:
  #   assert extract("👨 tech enthusiast / applied ai student").role == "Student"
  #   assert extract("A Ph.D. student in statistical science.").role == "Student"
  #   assert extract("PhD student at MIT Brain and Cognitive Sciences").role == "Student"
  #   assert extract("A strong conceptual thinker and a constant student").role is None
  #
  # def test_extract_set44() -> None:
  #   assert extract("Postgraduate student at Lund University.").role == "Student"
  #   assert extract("Student of Chinese medicine, dance teacher, rare soul & funk music digger").role == "Student"
  #   assert extract("Graduate Diploma in IT graduate with an undergraduate degree in Bachelor of Laws").role == "Student"
  #   assert extract("I engineer 'learn by doing' experiences for uni students with lean...").role == "Dev"
  #
  # def test_extract_set45() -> None:
  #   assert extract("My name is Harold Bogg, I am a college student").role == "Student"
  #   assert extract("Vice Dean for Undergraduate Studies").role == "Nondev"
  #   assert extract("My name is Josh Student").role == "Student"
  #   # ^ known false positive. Can't fix due to Spacy model limitations,
  #
  # def test_extract_mixed51() -> None:
  #   assert extract("""
  #     Technology leader at Gartner (Managing Vice President).
  #     Graduate student at University of Illinois getting my MBA. Forever an engineer.
  #   """) == Cats("Nondev", is_lead=True)
  #   assert extract("""
  #     Technology entrepreneur, sports lover, network security student.
  #   """) == Cats("Nondev")
  #   assert extract("""
  #     Lawyer. Lecturer. Researcher. Student
  #   """) == Cats("Nondev")
  #
  # def test_extract_mixed52() -> None:
  #   assert extract("""
  #     Blockchain student. Crypto investor.
  #   """) == Cats("Student")
  #   assert extract("""
  #     Technology entrepreneur, sports lover, network security student.
  #   """) == Cats("Nondev")
  #   assert extract("""
  #     Hi, I am 22 years old freelance full-stack developer from Czech Republic.
  #   """) == Cats("Dev", is_freelancer=True)
  #   assert extract("""
  #     As a Klingon code warrior, I take seriously the old proverb:
  #     "ghojwI'pu'lI' tISaH" ('Care about your students').
  #   """) == Cats()
  #   assert extract("""
  #     Dad | Runner | Aviation Student | Dog Lover | Builder of cool shit"
  #   """) == Cats("Student")
  #
  # def test_extract_mixed53() -> None:
  #   assert extract("""
  #     On a mission to help every student to reach their potential with technologies")
  #   """) == Cats("Student") # known issue
  #   assert extract("""
  #     TOGAF 9 Certified Enterprise Architect, Pragmatist, Economic Student, Biker,
  #   """) == Cats("Dev")
  #   assert extract("""
  #     Currently a Computer Science graduate student at University
  #     of the Philippines Diliman working on quantum algorithms.
  #   """) == Cats("Student")
  #   assert extract("""
  #     Over 30 years of experience working with diverse teams of researchers and
  #     students developing interactive software and hardware for science inquiry.
  #   """) == Cats("Dev") # because of "developing"
  #   assert extract("""
  #     B.Sc. in C.S. and M.Eng. student at the University of Bologna.
  #   """) == Cats("Student")
  #
  # def test_extract_mixed54() -> None:
  #   assert extract("""
  #     Software engineer at @GRID-is. Fellow of the Royal Geographical Society.
  #     Postgraduate student at Lund University.
  #   """) == Cats("Dev")
  #   assert extract("""
  #     Lead AI/ML Engineer at MITRE. Graduate student in Statistics at George Mason University.
  #     Officer emeritus of @srct, @gmuthetatau, @masonlug
  #   """) == Cats("Dev", is_lead=True)
  #   assert extract("""
  #     Developer at Sky and undergraduated in C.S. in Federal University of South Frontier
  #   """) == Cats("Dev")
  #   assert extract("""
  #     Undergraduate studying 'Software and Information Engineering' at the Vienna University of Technology
  #   """) == Cats("Student")
  #   assert extract("""
  #     Junior UI Designer @ Section BFA Design Art Undergraduate from NTU ADM, Singapore
  #   """) == Cats("Nondev")
  #
  # def test_extract_mixed55() -> None:
  #   assert extract("""
  #     Senior Software Engineer at @pagarme | Computer Science undergraduate at Pontifical Catholic University of Paraná
  #   """) == Cats("Dev")
  #   assert extract("""
  #     Full-time software developer and student. Spare-time Japan fan and gamer
  #   """) == Cats("Dev")
  #
  # def test_extract_mixed56() -> None:
  #   assert extract("""
  #     Founder & CEO @QualiSage | Team Lead | Senior Full-Stack Developer | 10+ Years
  #   """) == Cats("Nondev", is_lead=True)
  #   assert extract("Junior Programmer @BohemiaInteractive | Founder @QX-Interactive") == Cats("Dev")
  #   assert extract("""
  #     Full-stack web developer and Zend Certified PHP Engineer. Lead dev @Web3Box and freelancer @toptal
  #   """) == Cats(
  #     "Dev", is_freelancer = True, is_lead=True
  #   )
