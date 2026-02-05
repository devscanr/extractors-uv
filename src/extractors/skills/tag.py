from collections.abc import Callable
from dataclasses import dataclass, field
from spacy.tokens import Token
from typing import Literal
from ..extractor import Disambiguate, Tag
from ..dpatterns import DPattern
from ..xpatterns import XPattern

type Group = Literal["Language", "Tech", "Topic", "Company", "Certificate"]
type Resolve = Callable[[Token], list[str]]

@dataclass
class Skill(Tag):
  exclusive: bool = field(default=True, kw_only=True)
  group: Group = field(kw_only=True)
  publicname: str | None = field(default=None, kw_only=True)
  resolve: Resolve | list[str] | None = field(default=None, kw_only=True)

def Tech(
  name: str,
  phrases: list[
    str |      # Custom (converted to XPattern, DPattern or expanded)
    XPattern | # Matcher pattern
    DPattern   # DependencyMatcher pattern
  ],
  descr: str = "Tech",
  exclusive: bool = True,
  disambiguate: Disambiguate | list[Disambiguate] | None = None,
  resolve: Resolve | list[str] | None = None
) -> Skill:
  return Skill(
    name, phrases, descr,
    exclusive = exclusive,
    disambiguate = disambiguate,
    group = "Tech",
    resolve = resolve
  )

def Topic(
  name: str,
  phrases: list[
    str |      # Custom (converted to XPattern, DPattern or expanded)
    XPattern | # Matcher pattern
    DPattern   # DependencyMatcher pattern
  ],
  descr: str = "Topic",
  exclusive: bool = True,
  disambiguate: Disambiguate | list[Disambiguate] | None = None,
  publicname: str | None = None,
  resolve: Resolve | list[str] | None = None
) -> Skill:
  return Skill(
    name, phrases, descr,
    exclusive = exclusive,
    disambiguate = disambiguate,
    group = "Topic",
    publicname = publicname,
    resolve = resolve
  )

def Language(
  name: str,
  phrases: list[
    str |    # Custom (converted to XPattern, DPattern or expanded)
    XPattern # Matcher pattern
  ],
  descr: str = "Language",
  disambiguate: Disambiguate | list[Disambiguate] | None = None
) -> Skill:
  return Skill(
    name, phrases, descr,
    disambiguate = disambiguate,
    group = "Language"
  )

def Company(
  name: str,
  phrases: list[
    str |    # Custom (converted to XPattern, DPattern or expanded)
    XPattern # Matcher pattern
  ],
  descr: str = "Company",
  disambiguate: Disambiguate | list[Disambiguate] | None = None
) -> Skill:
  return Skill(
    name, phrases, descr,
    disambiguate = disambiguate,
    group = "Company"
  )

def Certificate(
  name: str,
  phrases: list[
    str |    # Custom (converted to XPattern, DPattern or expanded)
    XPattern # Matcher pattern
  ],
  descr: str = "Certificate",
  disambiguate: Disambiguate | list[Disambiguate] | None = None
) -> Skill:
  return Skill(
    name, phrases, descr,
    disambiguate = disambiguate,
    group = "Certificate"
  )
