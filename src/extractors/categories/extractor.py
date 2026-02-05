from collections.abc import Sequence
from spacy.tokens import Doc, Token
from typing import cast, Literal
from ..extractor import BaseExtractor, UMatch
from ..markers import is_future, is_hashtagged, is_negated, is_past
from ..spacyhelpers import ancestors, is_word, left_tokens
from .categorized import Categorized, CategorizedRole
from .data import CANCELING_TAGS
from ..utils import includes

class CategoryExtractor(BaseExtractor):
  exclusive_tags = False

  def extract_many(self, text_or_docs: Sequence[str | Doc]) -> list[Categorized]:
    if not text_or_docs:
      return []
    docs = self.nlp.pipe(text_or_docs) if isinstance(text_or_docs[0], str) else text_or_docs
    # LATER: `n_process` for multiprocessing
    return [self.extract(doc) for doc in docs]

  def extract(self, text_or_doc: str | Doc) -> Categorized:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # pprint(list(self.nlp.tokenizer.explain(text_or_doc)))
    # pprint([{
    #   "token": tok, "pos": tok.pos_, "dep": tok.dep_, "head": tok.head}
    #   for tok in doc if not tok.is_punct
    # ])

    umatches, _ = self.find_umatches(doc)

    # Cancel certain roles by mathed ancestor roles
    umatches2: list[UMatch] = []
    for umatch in umatches:
      cancelingset = next((CANCELING_TAGS[uname] for uname in unfold_names(umatch.name) if uname in CANCELING_TAGS), set())
      ancs = set(ancestors(umatch.maintoken))
      if not any(
        maintok in ancs and set(unfold_names(nm)) & cancelingset and not is_distant(umatch.maintoken, maintok)
        for nm, _, maintok in umatches
      ):
        umatches2.append(umatch)
    # print("umatches2:", umatches2)

    # Extract roles
    role: CategorizedRole | None = None
    is_freelancer, is_lead, is_remote, is_hireable = None, None, None, None
    for name, _, maintoken in umatches2:
      if role is None:
        if name == "Dev" or name.startswith("Dev:"):
          role = self.check_dev(maintoken)
        elif name == "Nondev" or name.startswith("Nondev:"):
          role = self.check_nondev(maintoken)
        elif name == "Student":
          role = self.check_student(maintoken)
        elif name == "Org":
          role = self.check_organization(maintoken)
      if is_freelancer is None:
        if name == "Freelancer":
          is_freelancer = self.check_freelancer(maintoken)
      if is_lead is None:
        if name == "Lead":
          is_lead = self.check_lead(maintoken)
      if is_remote is None:
        if name == "Remote":
          is_remote = self.check_remote(maintoken)
      if is_hireable is None:
        if name == "Hireable":
          is_hireable = self.check_hireable(maintoken)
    return Categorized(
      role = role,
      is_freelancer = is_freelancer,
      is_lead = is_lead,
      is_remote = is_remote,
      is_hireable = is_hireable,
    )

  def check_dev(self, token: Token) -> Literal["Student", "Dev", None]:
    if is_hashtagged(token):
      return "Dev"
    elif is_negated(token):
      return None
    elif is_past(token):
      return None
    elif is_future(token):
      return "Student"
    return "Dev"

  def check_nondev(self, token: Token) -> Literal["Student", "Nondev", None]:
    if is_hashtagged(token):
      return "Nondev"
    elif is_negated(token):
      return None
    elif is_past(token):
      return None
    elif is_future(token):
      return "Student"
    if token.lower_ == "head":
      sent = token.sent
      j = cast(int, token._.i)
      if j < sent.end and sent[j + 1].lower_ in {"@", "at", "of"}:
        return "Nondev"
      lwords = [tok.lower_ for tok in left_tokens(token) if is_word(tok)]
      if any(word in HEAD_MARKERS for word in lwords):
        return "Nondev"
      return None
    return "Nondev"

  def check_student(self, token: Token) -> Literal["Student", None]:
    if is_hashtagged(token):
      return "Student"
    elif is_negated(token):
      return None
    elif is_past(token):
      return None
    # elif is_future(token): -- in our domain we treat future students as also students
    #   return None
    return "Student"

  def check_organization(self, token: Token) -> Literal["Org", None]:
    root = token.sent.root
    if root == token or root.lower_ in {"are", "'re", "is", "'s"}:
      return "Org"
    return None

  def check_freelancer(self, token: Token) -> bool | None:
    if is_hashtagged(token):
      return True
    elif is_negated(token):
      return False
    elif is_past(token):
      return False
    return True

  def check_lead(self, token: Token) -> bool | None:
    if is_hashtagged(token):
      return True
    elif is_negated(token):
      return False
    elif is_past(token):
      return False
    elif is_future(token):
      return False
    return True

  def check_remote(self, token: Token) -> bool | None:
    if is_hashtagged(token):
      return True
    elif is_negated(token):
      return False
    lowers = [tok.lower_ for tok in token.sent]
    for marker in [("tool", "for"), ("working", "on")]:
      if includes(lowers, marker):
        return None
    return True

  def check_hireable(self, token: Token) -> bool | None:
    if is_hashtagged(token):
      return True
    elif is_negated(token):
      return False
    return True

# REMOTE_JOB_MARKERS = {
#   "coder",
#   "company",
#   "consultant", "consultancy", "consulting",
#   "collaboration", "collaborations",
#   "developer", "engineer",
#   "enthusiast", "freelancer",
#   "job", "jobs", "jobseeker",
#   "mentor", "mentoring", "mentorship",
#   "online",
#   "opportunity", "opportunities",
#   "position", "positions",
#   "programmer",
#   "project", "projects",
#   "remote", "remotely",
#   "role", "roles",
#   "seeking", "seeker",
#   "startup",
#   "teacher",
#   "team",
#   "work", "worker", "working",
# }
HEAD_MARKERS = {
  "design", "devops", "ds", "engineering", "development",
  "growth", "research", "security", "sre", "swe",
  "technology", "training",
}
# PROPOSAL_MARKERS = {
#   "challenge", "challenges",
#   "collaboration", "collaborations",
#   "consulting", "consultancy",
#   "enquiry", "enquiries",
#   "hire", "hiring", "hired",
#   "idea", "ideas",
#   "internship", "internships",
#   "job", "jobs",
#   "offer", "offers",
#   "opportunity", "opportunities",
#   "option", "options",
#   "position", "positions",
#   "possibility", "possibilities",
#   "project", "projects",
#   "proposal", "proposals",
#   "relocation",
#   "role", "roles",
#   "work",
# }

def is_distant(token1: Token, token2: Token) -> bool:
  mini = min(token1.i, token2.i)
  maxi = max(token1.i, token2.i)
  distance: float = 0
  for tok in token1.doc[mini+1:maxi]:
    if tok.text in {";", "|", "·"}:
      distance += 3
    elif tok.text in {"-", ",", "("}:
      distance += 2
    else:
      distance += 0.5
  return distance >= 3

def getprefix(name: str) -> str:
  return name.split(":")[0]

def unfold_names(name: str) -> list[str]:
  # "Nondev:Business:Other" -> ["Nondev:Business:Other", "Nondev:Business", "Nondev"]
  result: list[str] = []
  parts = name.split(":")
  while parts:
    result.append(":".join(parts))
    parts.pop()
  return result
