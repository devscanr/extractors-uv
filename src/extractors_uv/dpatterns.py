import re
from typing import Any
from .ppatterns import to_ppatterns
from .xpatterns import IN, LOWER, ORTH, XPattern, x_orthlower, x_nounlike

(LEFT_ID, REL_OP, RIGHT_ID, RIGHT_ATTRS, PHANTOM) = (
  "LEFT_ID", "REL_OP", "RIGHT_ID", "RIGHT_ATTRS", "PHANTOM"
)

type DToken = dict[str, Any]
type DPattern = list[DToken]

def clean(word: str) -> str:
  return word.strip("*")

# EXPS ---------------------------------------------------------------------------------------------

def exp_concat(lword: str, rword: str) -> DPattern:
  # (lword_rword)
  return [{
    RIGHT_ID: lword + rword,
    RIGHT_ATTRS: x_orthlower(lword + rword),
  }]

def exp_dash(lword: str, rword: str) -> DPattern:
  # (lword) . (-) . (rword)
  return [{
    RIGHT_ID: lword,
    RIGHT_ATTRS: x_orthlower(lword),
  }, {
    LEFT_ID: lword,
    REL_OP: ".",
    RIGHT_ID: "-",
    RIGHT_ATTRS: {ORTH: "-"},
  }, {
    LEFT_ID: "-",
    REL_OP: ".",
    RIGHT_ID: rword,
    RIGHT_ATTRS: x_orthlower(rword),
  }]

def exp_sequence(lword: str, rword: str, rev: bool=False) -> DPattern:
  if rev:
    # (rword) ; (lword)
    return [{
      RIGHT_ID: rword,
      RIGHT_ATTRS: x_orthlower(rword),
    }, {
      LEFT_ID: rword,
      REL_OP: ";",
      RIGHT_ID: lword,
      RIGHT_ATTRS: x_orthlower(lword),
    }]
  # (lword) . (rword)
  return [{
    RIGHT_ID: lword,
    RIGHT_ATTRS: x_orthlower(lword),
  }, {
    LEFT_ID: lword,
    REL_OP: ".",
    RIGHT_ID: rword,
    RIGHT_ATTRS: x_orthlower(rword),
  }]

def exp_parent(lword: str, rword: str) -> DPattern:
  # (lword) < (rword)
  return [{
    RIGHT_ID: lword,
    RIGHT_ATTRS: x_orthlower(lword),
  }, {
    LEFT_ID: lword,
    REL_OP: "<",
    RIGHT_ID: rword,
    RIGHT_ATTRS: x_orthlower(rword),
  }]

def exp_ancestor(lword: str, rword: str, rev: bool=False) -> DPattern:
  if rev:
    # (rword) >> (lword)
    return [{
      RIGHT_ID: rword,
      RIGHT_ATTRS: x_orthlower(rword),
    }, {
      LEFT_ID: rword,
      REL_OP: ">>",
      RIGHT_ID: lword,
      RIGHT_ATTRS: x_orthlower(lword),
    }]
  # (lword) << (rword)
  return [{
    RIGHT_ID: rword,
    RIGHT_ATTRS: x_orthlower(rword),
  }, {
    LEFT_ID: rword,
    REL_OP: ">>",
    RIGHT_ID: lword,
    RIGHT_ATTRS: x_orthlower(lword),
  }]

def exp_cc_parent(lword: str, rword: str) -> DPattern:
  # (lword) . (cc) . (noun) < (rword) where (cc=/,and...)
  return [{
    RIGHT_ID: lword,
    RIGHT_ATTRS: x_orthlower(lword),
  }, {
    LEFT_ID: lword,
    REL_OP: ".",
    RIGHT_ID: "cc",
    RIGHT_ATTRS: {LOWER: {IN: ["/", "and"]}},
    PHANTOM: True,
  }, {
    LEFT_ID: "cc",
    REL_OP: ".",
    RIGHT_ID: "$noun",
    RIGHT_ATTRS: x_nounlike(),
    PHANTOM: True,
  }, {
    LEFT_ID: "$noun",
    REL_OP: "<",
    RIGHT_ID: rword,
    RIGHT_ATTRS: x_orthlower(rword),
  }]

def exp_parent_cc(lword: str, rword: str) -> DPattern:
  # (lword) < (noun) . (cc) . (rword) where (cc=/,and...)
  return [{
    RIGHT_ID: lword,
    RIGHT_ATTRS: x_orthlower(lword),
  }, {
    LEFT_ID: lword,
    REL_OP: "<",
    RIGHT_ID: "$noun",
    RIGHT_ATTRS: x_nounlike(),
    PHANTOM: True,
  }, {
    LEFT_ID: "$noun",
    REL_OP: ".",
    RIGHT_ID: "cc",
    RIGHT_ATTRS: {LOWER: {IN: ["/", "and"]}},
    PHANTOM: True,
  }, {
    LEFT_ID: "cc",
    REL_OP: ".",
    RIGHT_ID: rword,
    RIGHT_ATTRS: x_orthlower(rword),
  }]

def exp_of_parent(lword: str, rword: str) -> DPattern:
  # (rword) > of > (lword)
  return [{
    RIGHT_ID: rword,
    RIGHT_ATTRS: x_orthlower(rword),
  }, {
    LEFT_ID: rword,
    REL_OP: ">",
    RIGHT_ID: "of",
    RIGHT_ATTRS: {LOWER: "of"},
    PHANTOM: True,
  }, {
    LEFT_ID: "of",
    REL_OP: ">",
    RIGHT_ID: lword,
    RIGHT_ATTRS: x_orthlower(lword),
  }]

def exp_of_sequence(lword: str, rword: str) -> DPattern:
  # (rword) . of . (lword)
  return [{
    RIGHT_ID: rword,
    RIGHT_ATTRS: x_orthlower(rword),
  }, {
    LEFT_ID: rword,
    REL_OP: ".",
    RIGHT_ID: "of",
    RIGHT_ATTRS: {LOWER: "of"},
    PHANTOM: True,
  }, {
    LEFT_ID: "of",
    REL_OP: ".",
    RIGHT_ID: lword,
    RIGHT_ATTRS: x_orthlower(lword),
  }]

def exp_of_parent_cc(lword: str, rword: str) -> DPattern:
  # (rword) > of > (noun) . (cc) . (lword) where (cc=/,and...)
  return [{
    RIGHT_ID: rword,
    RIGHT_ATTRS: x_orthlower(rword),
  }, {
    LEFT_ID: rword,
    REL_OP: ">",
    RIGHT_ID: "of",
    RIGHT_ATTRS: {LOWER: "of"},
    PHANTOM: True,
  }, {
    LEFT_ID: "of",
    REL_OP: ">",
    RIGHT_ID: "$noun",
    RIGHT_ATTRS: x_nounlike(),
    PHANTOM: True,
  }, {
    LEFT_ID: "$noun",
    REL_OP: ".",
    RIGHT_ID: "cc",
    RIGHT_ATTRS: {LOWER: {IN: ["/", "and"]}},
    PHANTOM: True,
  }, {
    LEFT_ID: "cc",
    REL_OP: ".",
    RIGHT_ID: lword,
    RIGHT_ATTRS: x_orthlower(lword),
  }]

# EXPANDS ------------------------------------------------------------------------------------------

# Parse `(lword) (rword)` to dpatterns
def expand_space(phrase: str) -> list[DPattern]:
  parts = phrase.partition(" ")
  assert len(parts) == 3
  lword, _, rword = parts
  return [
    exp_sequence(lword, rword),
  ]

# Parse `(anchor)>>(modifier)` to dpatterns
def expand_gtgt(phrase: str) -> list[DPattern]:
  parts = phrase.partition(">>")
  assert len(parts) == 3
  anchor, _, modifier = parts
  # print("?? anchor", anchor)
  # print("?? modifier", modifier)
  return [
    exp_ancestor(modifier, anchor, rev=True),
  ]

# Parse `(modifier)<(anchor)` to dpatterns
def expand_lt(phrase: str) -> list[DPattern]:
  parts = phrase.partition("<")
  assert len(parts) == 3
  modifier, _, anchor = parts
  return [
    exp_concat(modifier, anchor),   # (modifier)
    exp_dash(modifier, anchor),     # (modifier) . (-) . (anchor)
    exp_sequence(modifier, anchor), # (modifier) . (anchor)
    exp_parent(modifier, anchor),   # (modifier) < (anchor)
  ]

# Parse `(modifier)<~(anchor)` to dpatterns
def expand_lttilda(phrase: str) -> list[DPattern]:
  parts = phrase.partition("<~")
  assert len(parts) == 3
  modifier, _, anchor = parts
  return [
    exp_concat(modifier, anchor),       # (modifier)
    exp_dash(modifier, anchor),         # (modifier) . (-) . (anchor)
    exp_sequence(modifier, anchor),     # (modifier) . (anchor)
    exp_parent(modifier, anchor),       # (modifier) < (anchor)
    exp_cc_parent(modifier, anchor),    # (modifier) . (cc) . (noun) < (anchor) where (cc=/,and...)
    exp_parent_cc(modifier, anchor),    # (modifier) < (noun) . (cc) . (anchor) where (cc=/,and...)
    exp_of_sequence(modifier, anchor),  # (anchor) . of . (modifier)
    exp_of_parent(modifier, anchor),    # (anchor) > of > (modifier)
    exp_of_parent_cc(modifier, anchor), # (anchor) > of > (noun) . (cc) . (modifier) where (cc=/,and...)
  ]

####################################################################################################

# Parse `(lword)<<~(rword)` to dpatterns
# def expand_ltlttilda(phrase: str) -> list[DPattern]:
#   parts = phrase.partition("<<~")
#   assert len(parts) == 3
#   lword, _, rword = parts
#   return [
#     # (lword_rword) -- should we return PPattern (str) here?
#     [{
#       RIGHT_ID: lword + rword,
#       RIGHT_ATTRS: x_orthlower(lword + rword),
#     }],
#     # (lword) << (rword)
#     [{
#       RIGHT_ID: lword,
#       RIGHT_ATTRS: x_orthlower(lword),
#     }, {
#       LEFT_ID: lword,
#       REL_OP: "<<",
#       RIGHT_ID: rword,
#       RIGHT_ATTRS: x_orthlower(rword),
#     }],
#     # # (lword) << (noun) > (rword)
#     # [{
#     #   RIGHT_ID: rword,
#     #   RIGHT_ATTRS: x_orthlower(rword)
#     # }, {
#     #   LEFT_ID: lword,
#     #   REL_OP: "<<",
#     #   RIGHT_ID: "noun",
#     #   RIGHT_ATTRS: x_nounlike(),
#     # }, {
#     #   LEFT_ID: "noun",
#     #   REL_OP: ">",
#     #   RIGHT_ID: rword,
#     #   RIGHT_ATTRS: x_orthlower(rword)
#     # }],
#     # # (lword) < (noun) >> (rword)
#     # [{
#     #   RIGHT_ID: lword,
#     #   RIGHT_ATTRS: x_orthlower(lword)
#     # }, {
#     #   LEFT_ID: lword,
#     #   REL_OP: "<",
#     #   RIGHT_ID: "noun",
#     #   RIGHT_ATTRS: x_nounlike(),
#     # }, {
#     #   LEFT_ID: "noun",
#     #   REL_OP: ">>",
#     #   RIGHT_ID: rword,
#     #   RIGHT_ATTRS: x_orthlower(rword)
#     # }]
#   ]

WORD = r"\w+[+.#]?"
OP_RE = r">>|<~|<| "
# DPHRASE_RE = re.compile(rf"(\w+(?: {WORD})?)({OP_RE})(\w+(?: {WORD})?)")
DPHRASE_RE = re.compile(rf"({WORD})({OP_RE})({WORD})")

def expand_dphrase(phrase: str) -> list[DPattern]:
  # Can probably support N spaces on each side, but it's not done yet for simplicity.
  m = re.fullmatch(DPHRASE_RE, phrase)
  # print("@ expand_dphrase", repr(phrase))
  if not m:
    raise ValueError(f"bad dphrase {phrase!r}")
  _left, op, _right = m.group(1), m.group(2), m.group(3)
  # print("left:", left)
  # print("op:", op)
  # print("right:", right)
  match op:
    case ">>" if " " in phrase:
      raise ValueError("space support for >> operation is not implemented yet")
      # print(">>> phrase", repr(phrase))
      # left, right = phrase.split(op)
      # print(">>> left", repr(left))
      # print(">>> right", repr(right))
      # # if " " not in left: left = left.replace("*", "")
      # # if " " not in right: right = right.replace("*", "")
      # lwords = [word for word in left.split(" ")]
      # rwords = [word for word in right.split(" ")]
      # print(">>> lwords", repr(lwords))
      # print(">>> rwords", repr(rwords))
      # lmain = next((word[0:-1] for word in lwords if word[-1] == "*"), lwords[-1])
      # rmain = next((word[0:-1] for word in rwords if word[-1] == "*"), rwords[0])
      # print(">>> lmain", repr(lmain))
      # print(">>> rmain", repr(rmain))
      # patterns = expand_lttilda(f"{lmain}{op}{rmain}")
      # print(">>>", patterns)
      # # if len(lwords) == 2:
      # #   print("???", (
      # #     expand_space(f"{clean(lwords[0])} {lwords[1]}")[0]
      # #     if clean(left) == lmain else
      # #     expand_space(f"{lwords[0]} {clean(lwords[1])}", rev=True)[0]
      # #   ))
      # #   patterns.append(
      # #     expand_space(f"{clean(lwords[0])} {lwords[1]}")[0]
      # #     if clean(left) == lmain else
      # #     expand_space(f"{lwords[0]} {clean(lwords[1])}", rev=True)[0]
      # #   )
      # # if len(rwords) == 2:
      # #   print("???", (
      # #     expand_space(f"{rwords[0].strip("*")} {rwords[1]}")[0]
      # #     if clean(right) == rmain else
      # #     expand_space(f"{rwords[0]} {rwords[1].strip("*")}", rev=True)[0]
      # #   ))
      # #   patterns.append(
      # #     expand_space(f"{rwords[0].strip("*")} {rwords[1]}")[0]
      # #     if clean(right) == rmain else
      # #     expand_space(f"{rwords[0]} {rwords[1].strip("*")}", rev=True)[0]
      # #   )
      # return patterns
    case ">>":
      # print("??", expand_gtgt(phrase))
      return expand_gtgt(phrase)
    case "<~" if " " in phrase:
      raise ValueError("space support for <~ operation is not implemented yet")
    case "<~":
      return expand_lttilda(phrase)
    case "<":
      return expand_lt(phrase)
    case " ":
      return expand_space(phrase)
    case _:
      raise ValueError("code error, must not go here")

def to_dpatterns(phrases: list[str]) -> list[DPattern]:
  return [
    pattern
    for phrase in phrases
    for pattern in expand_dphrase(phrase)
  ]

def to_dpatterns2(phrases: list[str]) -> list[DPattern]:
  return [
    patt
    for ppatt in to_ppatterns(phrases)
    for patt in to_dpatterns([ppatt])
  ]

# Computer/Data Science/Art
# (lword) . (rword)
# (lword) < (rword)
#
# (lword) . (/) . (noun) < (rword)  | Computer/Data Science
# (rword) > (noun) . (/) . (lword)  | Data/Computer Science
#
# (lword) < (noun) . (/) . (rword)
# (lword) < (rword) . (/) . (noun)

# lword / noun < rword | Computer/Data Science
# lword > noun / rword
# rword > noun / lword
# rword / noun < lword

def separate_xphantoms(pattern: XPattern) -> tuple[XPattern, list[int]]:
  newpattern: XPattern = []
  phantoms: list[int] = []
  for o, xtoken in enumerate(pattern):
    if "PHANTOM" in xtoken:
      phantoms.append(o)
      newtoken = {**xtoken}
      del newtoken["PHANTOM"]
      newpattern.append(newtoken)
    else:
      newpattern.append(xtoken)
  return newpattern, phantoms

def separate_dphantoms(pattern: DPattern) -> tuple[DPattern, list[int]]:
  newpattern: DPattern = []
  phantoms: list[int] = []
  for o, dtoken in enumerate(pattern):
    if "PHANTOM" in dtoken:
      phantoms.append(o)
      newtoken = {**dtoken}
      del newtoken["PHANTOM"]
      newpattern.append(newtoken)
    else:
      newpattern.append(dtoken)
  return newpattern, phantoms
