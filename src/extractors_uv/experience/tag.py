from collections.abc import Sequence
from ..extractor import Disambiguate, Tag
from ..xpatterns import XPattern
from ..dpatterns import DPattern

def ExpTag(
  name: str,
  phrases: Sequence[
    str |      # Custom (converted to XPattern, DPattern or expanded)
    XPattern | # Matcher pattern
    DPattern   # DependencyMatcher pattern
  ],
  disambiguate: Disambiguate | list[Disambiguate] | None = None,
  exclusive: bool = True
) -> Tag:
  return Tag(
    name, phrases, "",
    exclusive=exclusive, disambiguate=disambiguate
  )
