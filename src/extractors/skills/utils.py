import re
from spacy.tokens import Token
from ..extractor import Disambiguate
from ..ppatterns import to_ppatterns
from ..spacyhelpers import left_token, right_token
from ..utils import lookslike

dis_punct = {".", ",", ";", ":", "|", "/", ")"}

def dis_precisely(*orths: str) -> Disambiguate:
  def disambiguate(token: Token) -> bool:
    return token.text in orths
  return disambiguate

def dis_incontext(*phrases: str) -> Disambiguate:
  # TODO use matchers to support multi-words combinations
  regmarkers = [
    re.compile(rf"{re.escape(marker)}", re.IGNORECASE)
    for marker in to_ppatterns(list(phrases))
  ]
  def disambiguate(token: Token) -> bool:
    ltoken = left_token(token)
    if ltoken and ltoken.text == "#":
      # Hashtagged
      return True
    for tok in token.sent:
      if tok != token:
        lower = tok.lower_
        if any(lookslike(lower, regmarker) for regmarker in regmarkers):
          return True
    return False
  return disambiguate

def dis_letterlike() -> Disambiguate:
  markers = {"lang", "language"}
  def disambiguate(token: Token) -> bool:
    ltoken = left_token(token)
    rtoken = right_token(token)
    if ltoken and ltoken.lower_ == "#":
      return True
    # Avoid highly ambiguos cases, at the cost of some FNs:
    if ltoken and ltoken.lower_ in {"-", "@"}:
      return False # foo-c, bar-v
    elif rtoken and rtoken.lower_ == "-":
      rtoken2 = right_token(rtoken)
      if rtoken2 and rtoken2.lower_ not in markers:
        return False # c-foo, v-bar
    return True
  return disambiguate

def dis_verblike() -> Disambiguate:
  def disambiguate(token: Token) -> bool:
    ltoken = left_token(token)
    rtoken = right_token(token)
    if ltoken and ltoken.text == "#":
      return True
    elif ltoken and ltoken.text == "@":
      return False
    elif ltoken and ltoken.text == "-":
      return True
    elif rtoken and rtoken.text == "-":
      return True
    elif token.pos_ in {"NOUN", "PROPN"}:
      return True
    elif token.is_sent_start and token.is_sent_end:
      return True
    elif token.is_sent_start and rtoken and rtoken.text in dis_punct:
      return True
    elif token.is_sent_end and ltoken and ltoken.text in dis_punct:
      return True
    return False
  return disambiguate

def dis_nounlike() -> Disambiguate:
  def disambiguate(token: Token) -> bool:
    ltoken = left_token(token)
    rtoken = right_token(token)
    if ltoken and ltoken.text == "#":
      return True
    elif ltoken and ltoken.text == "@":
      return False
    elif ltoken and ltoken.text == "-":
      return True
    elif rtoken and rtoken.text == "-":
      return True
    elif token.pos_ == "PROPN" and rtoken and rtoken.text in dis_punct:
      return True
    elif token.pos_ == "PROPN" and ltoken and ltoken.text in dis_punct:
      return True
    elif token.is_sent_start and token.is_sent_end:
      return True
    elif token.is_sent_start and rtoken and rtoken.text in dis_punct:
      return True
    elif token.is_sent_end and ltoken and ltoken.text in dis_punct:
      return True
    return False
  return disambiguate

def dis_namelike() -> Disambiguate:
  def disambiguate(token: Token) -> bool:
    ltoken = left_token(token)
    rtoken = right_token(token)
    if ltoken and ltoken.text == "#":
      return True
    elif ltoken and ltoken.text == "@":
      return False
    elif ltoken and ltoken.text == "-":
      return True
    elif rtoken and rtoken.text == "-":
      return True
    elif token.is_sent_start and token.is_sent_end:
      return True
    elif token.is_sent_start and rtoken and rtoken.text in dis_punct:
      return True
    elif token.is_sent_end and ltoken and ltoken.text in dis_punct:
      return True
    for tok in token.sent:
      if tok.lower_ in {"am", "'m", "is", "'s", "name"}:
        return False
    return True
  return disambiguate
