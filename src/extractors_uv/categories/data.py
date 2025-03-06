from spacy.tokens import Token
from ..extractor import Tag
from ..ppatterns import expand_parens
from ..spacyhelpers import IN, POS, left_token, right_token
from ..xpatterns import LOWER, verb
from ..xpatterns import dep_root
from .tag import CatTag

def dis_se(token: Token) -> bool:
  rtoken = right_token(token)
  if rtoken and (rtoken.lower_ in {"at", "intern", "student"} or rtoken.text.startswith("@")):
    return True
  ltoken = left_token(token)
  if ltoken and (ltoken.lower_ in {"junior", "middle", "senior", "principal"}):
    return True
  return False

SEARCH_ANCHORS = [p for ph in [
  "open(ed)", # for # to
  "available", # for "available to",
  "consider(s)", "considering",
  "look(s)", "looking", # for # for
  "ready", "ready", # for # to
  "search(es)", "searching",
  "seek(s)", "seeking",
] for p in expand_parens(ph)]

ACTIVITY_ANCHORS = [p for ph in [
  "coding", "developing", "programming", "teaching", "working", "writing"
] for p in expand_parens(ph)]

REMOTE_TARGETS = [
  "agency", "agencies",
  "company", "companies",
  "consultant(s)", "consultancy", "consulting",
  "collaboration(s)",
  "coder(s)",
  "dev(s)",
  "developer(s)",
  "employee(s)",
  "employer(s)",
  "engineer(s)",
  "enthusiast(s)",
  "firm(s)",
  "freelancer(s)",
  "job(s)",
  "jobseeker",
  "mentor(s)", "mentoring", "mentorship",
  "offer(s)",
  "opportunity", "opportunities",
  "position(s)",
  "project(s)",
  "programmer(s)",
  "role(s)",
  "seeker(s)",
  "startup(s)",
  "teacher(s)",
  "team(s)",
  "work(s)",
  "worker(s)", # "working", # 2nd for mistakenly inverted deps
]

HIREABLE_TARGETS = [
  "challenge(s)",
  "collaborations(s)",
  "consulting", "consultancy",
  "enquiry", "enquiries",
  "hire", "hiring", "hired",
  "job(s)",
  "idea(s)",
  "internship(s)",
  "offer(s)",
  "opportunity", "opportunities",
  "option(s)",
  "position(s)",
  "possibility", "possibilities",
  "project(s)",
  "proposal(s)",
  "relocation",
  "role(s)",
  "work"
]

TAGS: list[Tag] = [
  # ROLES ---
  CatTag("Dev:Administrator", [
    "administrator", "admin",
    "dbadmin", "dba",
    "systemadministrator", "sysadmin",
  ]),
  CatTag("Dev:Analyst", [
    "analyst",
    "businessanalyst",
    "dataanalyst",
  ]),
  CatTag("Dev:Architect", [
    "architect",
    "dataarchitect",
    "dbarchitect",
  ]),
  CatTag("Dev:Developer", [
    verb("developing"),
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
  ]), # TODO disambiguate verbs here?
  CatTag("Dev:Engineer", [
    verb("engineering"),
    "engineer", "eng",
    "dataengineer",
    "mlengineer",
    "softwareengineer", "swe", "sde",
    "systemengineer",
    "webengineer",
  ]),
  CatTag("Dev:Engineer", ["se"], disambiguate=dis_se),

  # def disambiguate(token: Token) -> bool:
  #   ltoken = left_token(token)
  #   rtoken = right_token(token)
  #   ltoken2 = left_token(ltoken) if ltoken else None
  #   rtoken2 = right_token(rtoken) if rtoken else None
  #   if ltoken and ltoken.lower_ == "#":
  #     # Hashtagged
  #     return True
  #   elif re.match("[A-Z]", token.text):
  #     # Capitalized
  #     if ltoken and ltoken.text in {",", ")"} and ltoken2 and re.match("[A-Z#]", ltoken2.text):
  #       # And the prev word is capitalized or hashtagged
  #       return True
  #     elif rtoken and rtoken.text in {",", "("} and rtoken2 and re.match("[A-Z#]", rtoken2.text):
  #       # And the next word is capitalized or hashtagged
  #       return True
  #     elif ltoken and rtoken and ltoken.text == "(" and rtoken.text == ")":
  #       # And the token is within parentheses
  #       return True
  #   return False

  CatTag("Dev:Programmer", [
    verb("coding"),
    verb("programming"),
    "programmer", "coder",
    "gameprogrammer",
    "phpcoder",
    "webprogrammer", "webcoder",
  ]),
  CatTag("Dev:Ops", [
    "operations", "op(s)",
  ]),
  CatTag("Dev:DevOps", [
    "dev=op(s)",
  ]),
  CatTag("Dev:DataOps", [
    "ai=op(s)",
    "dataop(s)",
    "ml=op(s)",
  ]),
  CatTag("Dev:NetOps", [
    "net=op(s)",
  ]),
  CatTag("Dev:DevSecOps", [
    "dev/sec=op(s)", "sec/dev=op(s)",
    "devsecop(s)", "secdevop(s)",
    "devop(s)sec", "secop(s)dev",
  ]),
  CatTag("Dev:SecOps", [
    "sec=op(s)",
  ]),
  CatTag("Dev:SysOps", [
    "sysop(s)",
  ]),
  CatTag("Dev:Security", [
    "security", "sec",
  ]),
  CatTag("Dev:Science", [
    "academic",
    "biologist",
    "chemist",
    "informatician",
    "mathematician",
    "ph.d",
    "physicist",
    "researcher",
    "scientist",
    "statistician",
  ]),
  CatTag("Dev:Tester/QA", [
    "qa",
    "tester",
    "pentester",
    "qatester",
  ]),
  CatTag("Dev:Other", [
    # For non dev-first platforms, this can become just "Other" and be handled separately
    "expert",
    "generalist",
    "hacker",
    "investigator",
    "professional",
    "specialist",
  ]),
  CatTag("Nondev:Education", [
    "dean",
    "coach",
    "educator",
    "lecturer", # verb("lecturing")
    "mentor", # verb("mentoring")
    "professor", "prof",
    "teacher", # verb("teaching")
    "trainer",
  ]),
  CatTag("Nondev:Business", [
    # verb("founding"),
    "businessman",
    "ceo",
    "cto",
    "director",
    "entrepreneur",
    "founder", "co=founder",
    "investor",
    "head",
    "manager", # verb "managing"
    "owner",
    "president", "vice=president",
    "vp", "svp",
  ]),
  CatTag("-Nondev:Business", [
    "head-first",
  ]),
  CatTag("Nondev:Designer", [
    # verb("designing"),
    "designer",
    "gamedesigner",
    "uidesigner",
    "webdesigner",
  ]),
  CatTag("Nondev:Other", [
    "artist",
    "auditor",
    "producer", # verb("producing")
    "lawyer",
    "musician",
    "recruiter", # recruiters?, verb("hiring"), verb("recruiting")
  ]),
  CatTag("Student", [
    verb("learn"),
    verb("learning"),
    verb("study"),
    verb("studying"),
    "alumni", "alumnus", "alum",
    "amateur",
    "beginner",
    "bachelor",
    "b.s",
    "freshman",
    "graduate",
    "intern",
    "internship",
    "master of science", "m.s",
    "major",
    "learner",
    "newbie", "noob",
    "new to",
    "novice",
    "rookie",
    "sophomore",
    "student",
    "teenage",
    "teenager",
    "undergrad(uate)",
  ]),
  CatTag("-Student", [
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
  CatTag("Org", [
    "agency",
    "company",
    "community",
    "firm",
    "group",
    "organization", "org",
    "platform",
    "professional network",
    "social network",
    "team",
  ]),

  # FLAGS ---
  CatTag("Remote", [
    [{LOWER: "remote"} | dep_root],
    [{LOWER: "remote"} | {POS: {IN: ["NOUN", "PROPN"]}}],
    [{LOWER: "remotely"} | dep_root],
    "remote=friendly",
    "remote=only",
    "open=for=remote",
    "open=to=remote",
    "remote/online",
    *[
      # Hacks for imperfect "remote" parsing
      f"remote {competence}"
      for competence in ["backend", "blockchain", "frontend", "fullstack", "game", "mobile", "qa", "web"]
    ],
    *[
      # Note: 2+ simultaneous parentheses are not supported yet
      f"remote<~{target}"
      for target in REMOTE_TARGETS
    ],
    *[
      # 2+ simultaneous parentheses are not supported yet
      f"{anchor}>>{target}"
      for anchor in [*SEARCH_ANCHORS, *ACTIVITY_ANCHORS]
      for target in ["remote", "remotely"]
    ]
  ], exclusive=False),
  CatTag("Lead", [
    verb("leading"),
    "lead", "leader", "co-lead",
    "leadership",
    "teamlead", "tl",
    "techlead",
  ], exclusive=False),
  CatTag("-Lead", [
    # TODO maybe whitelist `(Leading)>>(target)` instead?
    "market-leading",
    "road(s)>>leading",
    "leading>>life",
  ]),
  CatTag("Hireable", [
    "for=hire",
    "hire=able",
    "hirable",
    "hire=me",
    "hire=us",
    "hiring=me",
    "job=seeker",
    "job=wanted",
    "open=to=work",
    *[
      # 2+ simultaneous parentheses are not supported yet
      f"{anchor}>>{target}"
      for anchor in SEARCH_ANCHORS
      for target in HIREABLE_TARGETS
    ],
  ], exclusive=False),
  CatTag("Freelancer", [
    "free=lance(r)",
    "free=lancing",
    "consultancy",
    "consultant",
    "consulting",
  ], exclusive=False),
]

# ("guru", "expert", "ninja", "magician", "wizard") were previously used
# to cancel "Student" role. Not applied yet, not sure...

CANCELING_TAGS = {
  "Dev": {"Dev", "Nondev", "Org", "Student"},
  "Nondev": {"Dev", "Nondev", "Org", "Student"},
  "Nondev:Business": {"Nondev", "Org", "Student"},
  "Student": {"Org", "Student"},
  "Org": {"Dev", "Nondev", "Org", "Student"},
  "Lead": {"Org", "Student"},
  "Freelancer": {"Freelancer", "Org"},
  "Hireable": {"Org"},
  "Remote": {"Org"},
} # TODO why don't we use the same approach in title extraction?!

# TODO "doctor", "postdoc", etc.
