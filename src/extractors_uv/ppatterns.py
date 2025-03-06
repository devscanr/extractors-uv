import re

# Parse `wordA-wordB`, `wordA-wordB-wordC`, `wordA=wordB`, etc. to ppatterns
def expand_dashes(phrase: str) -> list[str]:
  if not phrase:
    return []
  dotequal_i, equal_i, dash_i = phrase.find(".="), phrase.find("="), phrase.find("-")
  l = len(phrase)
  first_cc = min(l, l, *[i for i in [dotequal_i, equal_i, dash_i] if i != -1])
  if first_cc == dotequal_i:
    # TODO support also "/=" ?
    # Handling ".="s
    head, tail = phrase[0:dotequal_i], phrase[dotequal_i + 2:]
    tail_patterns = expand_dashes(tail)
    return [
      head + "." + pattern for pattern in tail_patterns
    ] + [
      head + "-" + pattern for pattern in tail_patterns
    ] + [
      head + " " + pattern for pattern in tail_patterns
    ] + [
      head + pattern for pattern in tail_patterns
    ]
  elif first_cc == equal_i:
    # Handling "="s
    head, tail = phrase[0:equal_i], phrase[equal_i + 1:]
    tail_patterns = expand_dashes(tail)
    return [
      head + "-" + pattern for pattern in tail_patterns
    ] + [
      head + " " + pattern for pattern in tail_patterns
    ] + [
      head + pattern for pattern in tail_patterns
    ]
  elif first_cc == dash_i:
    # Handling "-"s
    head, tail = phrase[0:dash_i], phrase[dash_i + 1:]
    tail_patterns = expand_dashes(tail)
    return [
      head + "-" + pattern for pattern in tail_patterns
    ] + [
      head + " " + pattern for pattern in tail_patterns
    ]
  else:
    return [phrase]

# Parse `word(suffix)`, `(prefix)word`, etc. to patterns
def expand_parens(phrase: str) -> list[str]:
  drop = lambda text: re.sub(r"\([^)]*\)", "", text)
  open = lambda text: re.sub(r"\(|\)", "", text)
  return [
    patt for patt in ([drop(phrase), open(phrase)]
    if "(" in phrase else [phrase])
  ]

def expandlist_parens(phrases: list[str]) -> list[str]:
  return [
    patt
    for phrase in phrases
    for patt in expand_parens(phrase)
  ]

# Chain expand_dashes over phrases
def expandlist_dashes(phrases: list[str]) -> list[str]:
  return [
    patt
    for phrase in phrases
    for patt in expand_dashes(phrase)
  ]


# Chain expand_dashes and expand_parens over phrases
def to_ppatterns(phrases: list[str]) -> list[str]:
  return [
    patt2
    for phrase in phrases
    for patt1 in expand_dashes(phrase)
    for patt2 in expand_parens(patt1)
  ]
