from ..extractor import Tag
from .roletag import RoleTag

TAGS: list[Tag] = [
  # TODO consider verbs like programming, studying, leading, etc.
  RoleTag("Human:Administrator", [
    "administrator", "admin",
    "dbadmin", "dba",
    "systemadministrator", "sysadmin",
  ]),
  RoleTag("Human:Analyst", [
    "analyst",
    "businessanalyst",
    "dataanalyst",
  ]),
  RoleTag("Human:Architect", [
    "architect",
    "dataarchitect",
    "dbarchitect",
  ]),
  RoleTag("Human:Developer", [
    "developer", "dev",
    "gamedeveloper", "gamedev",
    "godev", "gopher",
    "mobiledeveloper", "mobiledev",
    "phpdeveloper", "phpdev", "phper",
    "pydev", "pythonist(a)",
    "rubydev", "rubyist", "rubist",
    "rustacean",
    "softwaredeveloper", "softwaredev",
    "systemdeveloper",
    "webdeveloper", "webdev",
  ]),
  RoleTag("Human:Engineer", [
    "engineer", "eng",
    "dataengineer",
    "mlengineer",
    "softwareengineer", "swe", "sde", # TODO SE with disambig.
    "ms=cs", "bs=cs", "m.s=cs", "b.s=cs",
    "ms=ds", "bs=ds", "m.s=ds", "b.s=ds",
    "systemengineer",
    "webengineer",
  ]),
  RoleTag("Human:Programmer", [
    "programmer", "coder",
    "gameprogrammer",
    "phpcoder",
    "webprogrammer", "webcoder",
  ]),
  RoleTag("Human:Ops", [
    "operations", "op(s)",
  ]),
  RoleTag("Human:DevOps", [
    "dev=op(s)",
  ]),
  RoleTag("Human:DataOps", [
    "ai=op(s)",
    "dataop(s)",
    "ml=op(s)",
  ]),
  RoleTag("Human:NetOps", [
    "net=op(s)",
  ]),
  RoleTag("Human:DevSecOps", [
    "dev/sec=op(s)", "sec/dev=op(s)",
    "devsecop(s)", "secdevop(s)",
    "devop(s)sec", "secop(s)dev",
  ]),
  RoleTag("Human:SecOps", [
    "sec=op(s)",
  ]),
  RoleTag("Human:SysOps", [
    "sysop(s)",
  ]),
  RoleTag("Human:Security", [
    "security", "sec",
  ]),
  RoleTag("Human:Tester/QA", [
    "qa",
    "tester",
    "pentester",
    "qatester",
  ]),
  RoleTag("Human:Education", [
    "dean",
    "coach",
    "educator",
    "lecturer",
    "mentor",
    "professor", "prof",
    "teacher",
    "trainer",
  ]),
  RoleTag("Human:Science", [
    "academic",
    "biologist",
    "chemist",
    "informatician",
    "mathematician",
    "ph.d candidate",
    "ph.d",
    "physicist",
    "researcher",
    "scientist",
    "statistician",
  ]),
  RoleTag("Human:Business", [
    "businessman",
    "ceo",
    "cto",
    "director",
    "entrepreneur",
    "founder", "co=founder",
    "investor",
    "head",
    "manager",
    "owner",
    "president", "vice=president",
    "vp", "svp",
  ]),
  RoleTag("-Human:Business", [
    "head-first",
  ]),
  RoleTag("Human:Other", [
    "animator",
    "artist",
    "auditor",
    "author",
    "employee",
    "enthusiast",
    "expert",
    "generalist",
    "guru",
    "hacker",
    "investigator",
    "lawyer",
    "musician",
    "ninja",
    "producer",
    "professional",
    "recruiter",
    "specialist",
    "wizard",
  ]),
  RoleTag("Human:Freelancer", [
    "free=lancer",
    "consultant",
  ]),
  RoleTag("Human:Lead", [
    # TODO add human roots like lead << developer? How to default to human, then?
    "lead",
    "leader",
    "teamlead", "tl",
    "techlead",
  ]),
  RoleTag("Human:Designer", [
    "designer",
    "gamedesigner",
    "uidesigner",
    "webdesigner",
  ]),
  RoleTag("Human:Student", [
    "alumni", "alumnus", "alum",
    "amateur",
    "beginner",
    "bachelor",
    "bachelor of science", "b.s",
    "freshman",
    "graduate",
    "intern",
    "master of science", "m.s",
    "major",
    "learner",
    "newbie", "noob",
    "new to",
    "novice",
    "rookie",
    "sophomore",
    "student",
    "teenager",
    "undergrad(uate)",
  ]),
  RoleTag("-Human:Student", [
    "constant student",
    "every student",
    "eternal student",
    "everlasting student",
    "forever student",
    "life=long student",
    "perpetual student",
    "student of life",
    *[
      f"{anchor}>>{target}"
      for anchor in ["learning", "studying"]
      for target in ["always", "forever", "world"]
    ],
  ]),
  RoleTag("Org", [
    "agency",
    "company",
    "community",
    "firm",
    "organization", "org",
    "platform",
    "professional network",
    "social network",
    "team",
  ]),
]

# doc? dr? doctor? postdoc?

# TODO consider to resolve "Frontender" and other rare words during normalization phase
# to not duplicate all that mess in rules. The downside is that more regexes will be searched for
# in normalization. But less regexes will be compared with during pattern matchings. The major win
# is that we'll have less terms to train Spacy.
