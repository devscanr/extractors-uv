import re
from typing import Any

(DEP, IN, IS_PUNCT, IS_SENT_START, LOWER, NOT_IN, OP, ORTH, POS, REGEX, TAG, TEXT) = (
  "DEP", "IN", "IS_PUNCT", "IS_SENT_START", "LOWER", "NOT_IN", "OP", "ORTH", "POS",
  "REGEX", "TAG", "TEXT"
)

type XToken = dict[str, Any]
type XPattern = list[XToken]

def x_regex(word: str) -> XToken:
  return {TEXT: {REGEX: word}}

def x_lower(words: str | list[str]) -> XToken:
  if isinstance(words, list):
    return {LOWER: {IN: words}}
  else:
    return {LOWER: words}

def x_orth(words: str | list[str]) -> XToken:
  if isinstance(words, list):
    return {ORTH: {IN: words}}
  else:
    return {ORTH: words}

def x_orthlower(word: str) -> XToken:
  return {ORTH: word} if re.search(r"[A-Z]", word) else {LOWER: word}

def x_nounlike() -> XToken:
  return {POS: {IN: ["NOUN", "PROPN", "ADJ"]}}

# no IS_SENT_END in Spacy, can't define `singleton`
dep_root = {DEP: "ROOT"}
tag_nn = {TAG: "NN", POS: "NOUN"}
tag_nnp = {TAG: "NNP", POS: "PROPN"} # POS is kinda of duplicate but it's required for the "attribute_ruler"
tag_jj = {TAG: "JJ", POS: "ADJ"}     # /

def ver1(word: str) -> XPattern:
  return [
    {LOWER: {REGEX: r"^" + word + r"[-\d.]{0,4}$"}}
  ]

def nounlike(word: str | None = None) -> XPattern:
  if not word:
    return [x_nounlike()]
  return [
    x_orthlower(word) | x_nounlike()
  ]

def propn(word: str | None = None) -> XPattern:
  if not word:
    return [{POS: "PROPN"}]
  return [
    x_orthlower(word) | {POS: "PROPN"}
  ]

def verb(word: str | None = None) -> XPattern:
  if not word:
    return [{POS: "VERB"}]
  return [
    x_orthlower(word) | {POS: "VERB"}
  ]

def literal(phrase: str) -> XPattern:
  return [
    {ORTH: word} for word in re.split(r"(?<=\W)(?=\w)|(?<=\w)(?=\W)", phrase)
    if word.strip()
  ]
