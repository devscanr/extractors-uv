from collections.abc import Callable, Sequence
from spacy import Language
from spacy.tokens import Doc, Token
from ..extractor import BaseExtractor
from ..utils import uniq
from .tag import Skill

type Resolve = Callable[[Token], list[str]]

def create_resolve(ss: list[str]) -> Resolve:
  return lambda _: ss

class SkillExtractor(BaseExtractor):
  def __init__(self, nlp: Language, skills: Sequence[Skill]):
    super().__init__(nlp, skills)
    self.groups: dict[str, str] = {}
    self.publicnames: dict[str, str] = {}
    self.resolvers: dict[str, Resolve] = {}
    self.init_matchers2(skills)

  def init_matchers2(self, skills: Sequence[Skill]) -> None:
    for skill in skills:
      # Update groups
      if skill.name not in self.groups:
        self.groups[skill.name] = skill.group
      # Update publicnames
      if skill.publicname is not None:
        assert skill.name not in self.publicnames, f"duplicate `publicname` at {skill.name!r}"
        self.publicnames[skill.name] = skill.publicname
      # Update resolve fns
      if skill.resolve is not None:
        assert skill.name not in self.resolvers, f"duplicate `resolve` at {skill.name!r}"
        self.resolvers[skill.name] = create_resolve(skill.resolve) if isinstance(skill.resolve, list) else skill.resolve

  def extract_many(self, text_or_docs: Sequence[str | Doc]) -> list[list[str]]:
    if not text_or_docs:
      return []
    docs = self.nlp.pipe(text_or_docs) if isinstance(text_or_docs[0], str) else text_or_docs
    # LATER: `n_process` for multiprocessing
    return [self.extract(doc) for doc in docs]

  def extract(self, text_or_doc: str | Doc) -> list[str]:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # pprint(list(self.nlp.tokenizer.explain(text_or_doc)))
    # pprint([{
    #   "token": tok, "pos": tok.pos_, "dep": tok.dep_, "head": tok.head} for tok in doc
    # ]) # if not tok.is_punct
    umatches, _ = self.find_umatches(doc)
    # Resolve skills
    skills: list[str] = []
    for name, _, maintoken in umatches:
      if name in self.resolvers:
        skills += self.resolvers[name](maintoken)
      else:
        skills.append(name)
    # Uniquelize and dealias skills
    return [
      self.to_publicname(s)
      for s in uniq(skills)
    ]

  def to_publicname(self, name: str) -> str:
    if name in self.publicnames:
      return self.publicnames[name]
    return name
