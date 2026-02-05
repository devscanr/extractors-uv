from ..extractor import Disambiguate, Tag
from ..xpatterns import XPattern
from ..dpatterns import DPattern

def RoleTag(
  name: str,
  phrases: list[
    str |      # Custom (converted to XPattern, DPattern or expanded)
    XPattern | # Matcher pattern
    DPattern   # DependencyMatcher pattern
  ],
  disambiguate: Disambiguate | list[Disambiguate] | None = None
) -> Tag:
  return Tag(
    name, phrases, "",
    exclusive = True,
    disambiguate = disambiguate
  )
