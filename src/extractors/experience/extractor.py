from collections.abc import Generator, Sequence
import re
from spacy.tokens import Doc, Token
from ..extractor import BaseExtractor, UMatch
from ..markers import is_future, is_negated, is_past
from .experience import is_OtherExperienceKind
from .experience import Experience
from ..spacyhelpers import left_token, right_token
from ..utils import is_numeric_token

class ExperienceExtractor(BaseExtractor):
  def extract_many(self, text_or_docs: Sequence[str | Doc]) -> list[Experience | None]:
    if not text_or_docs:
      return []
    docs = self.nlp.pipe(text_or_docs) if isinstance(text_or_docs[0], str) else text_or_docs
    # LATER: `n_process` for multiprocessing
    return [self.extract(doc) for doc in docs]

  def extract(self, text_or_doc: str | Doc) -> Experience | None:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # pprint(list(self.nlp.tokenizer.explain(text_or_doc)))
    # pprint([{
    #   "token": tok, "pos": tok.pos_, "dep": tok.dep_, "head": tok.head}
    #   for tok in doc # if not tok.is_punct
    # ])
    umatches, _ = self.find_umatches(doc)
    # print("umatches:", umatches)

    # Filter negated and future matches
    umatches2 = [
      umatch for umatch in umatches
      if not any(pred(umatch.maintoken) for pred in [is_negated, is_future, is_past])
    ]
    # print("umatches2:", umatches2)

    experiences = list(self.parse_experiences(umatches2))
    # print("experiences:", experiences)
    match len(experiences):
      case 0: return None
      case 1: return experiences[0]
      case 2:
        e1, e2 = experiences
        is_e1_exact = e1.kind == "Exact"
        is_e2_exact = e2.kind == "Exact"
        if is_e1_exact and is_e2_exact or not is_e1_exact and not is_e2_exact:
          return None # "exact, exact" and "other, other" cases are ambiguous
        elif is_e2_exact:
          return e2 # "other, exact" -> exact
        else:
          return e1 # "exact, other" -> exact
      case _: return None

  def parse_experiences(self, umatches: list[UMatch]) -> Generator[Experience, None, None]:
    # experiences: list[Experience] = []
    # Note: all 'Other' matches are single token wide (phantoms are dropped by this point)
    skips: set[int] = set()
    for k, umatch in enumerate(umatches):
      if k in skips:
        continue
      if umatch.name in {"MOE", "YOE"}:
        exp = self.parse_ee(umatch.name, umatch.tokens)
        if exp:
          yield exp
      else:
        next_umatch = umatches[k + 1] if k < len(umatches) - 1 else None
        rtoken = right_token(umatch.maintoken)
        if (
          rtoken and rtoken.text in {"/", "-", "->", ",", "·"} and
          next_umatch and next_umatch.maintoken.i == umatch.maintoken.i + 2 and next_umatch.name not in {"MOE", "YOE"}
        ):
          match (umatch.name, next_umatch.name):
            case "Junior", "Middle":
              yield Experience("Junior", over=True)
              skips.add(k + 1)
              continue
            case "Middle", "Senior":
              yield Experience("Middle", over=True)
              skips.add(k + 1)
              continue
            case "Senior", "Principal":
              yield Experience("Senior", over=True)
              skips.add(k + 1)
              continue
        experience = self.parse_oe(umatch.name, umatch.tokens)
        if experience:
          yield experience

  def parse_ee(self, tagname: str, tokens: list[Token]) -> Experience | None:
    sent = tokens[0].sent
    # Search for `over`
    over = any(
      tok.lower_ == "+" and is_numeric_token(left_token(tok)) or
      tok.lower_ in {"more", "over"}
      for tok in sent
      if tok not in tokens
      if tok.head in tokens or tok.head.head in tokens
    ) or any (
      "+" in tok.text for tok in tokens
    )
    # Search for numeric number
    numstrs = [
      tok.lower_ for tok in sent
      if tok not in tokens
      if (tok.head in tokens or tok.head.head in tokens)
      if is_numeric_token(tok)
    ]
    num = parse_numstr(numstrs[0]) if len(numstrs) == 1 else None
    if num is not None and num > 0:
      return Experience("Exact", months=num_to_months(tagname, num), over=over)
    # Search for textual number
    wnumstrs = [
      tok.lower_ for tok in sent
      if tok not in tokens
      if (tok.head in tokens or tok.head.head in tokens)
      if re.fullmatch(r"one\+?|two\+?|\+", tok.lower_)
    ]
    num = parse_wnumstr(wnumstrs[0]) if len(wnumstrs) == 1 else None
    if num is not None and num > 0:
      return Experience("Exact", months=num_to_months(tagname, num), over=over)
    return None

  def parse_oe(self, tagname: str, tokens: list[Token]) -> Experience | None:
    sent = tokens[0].sent
    # Search for `over`
    over = any(
      tok.lower_ == "+" and is_numeric_token(left_token(tok))
      for tok in sent
      if tok not in tokens
      if tok.head in tokens or tok.head.head in tokens
    ) or any (
      "+" in tok.text for tok in tokens
    )
    # if not over:
    #   lt1 = left_token(tokens[0])
    #   lt2 = left_token(lt1)
    #   rt1 = right_token(tokens[-1])
    #   rt2 = right_token(rt1)
    #   if lt1.text in {"-", "/", "->"} and rt1.text not in {"-", "/", "->"}:
    #     # and lt2.lower_ in {"junior", "intermediate", "middle", "senior"}
    #     print("???")
    #     if (
    #       tagname == "Middle" and lt2.lower_ in {"junior"} or
    #       tagname == "Junior" and lt2.lower_ in {"middle", "intermediate"}
    #     ):
    #       return Experience("Junior", over=over)
    #     elif (
    #       tagname == "Senior" and lt2.lower_ in {"middle", "intermediate"} or
    #       tagname == "Middle" and lt2.lower_ in {"senior"}
    #     ):
    #       return Experience("Middle", over=over)
    #     elif (
    #       tagname == "Principal" and lt2.lower_ in {"middle", "intermediate"}
    #     ): # in {"junior", "intermediate", "middle", "senior"}:
    #       tagname = "Middle"
    #       over = True
    #     elif tagname == "Principal":
    #       tagname = "Middle"
    #       over = True
    #   elif rt1.text in {"-", "/", "->"} and lt1.text not in {"-", "/", "->"}:
    #     # and rt2.lower_ in {"intermediate", "middle", "senior", "principal"}
    #     over = True
    if is_OtherExperienceKind(tagname):
      return Experience(tagname, over=over)
    return None

def parse_numstr(numstr: str) -> float | None:
  try:
    return float(numstr) if numstr else None
  except:
    return None

def parse_wnumstr(wnumstr: str) -> float | None:
  if wnumstr in WNUM_TO_NUM:
    return WNUM_TO_NUM[wnumstr]
  return None

def num_to_months(tagname: str, num: float) -> int:
  if tagname == "YOE":
    return round(num * 12)
  elif tagname == "MOE":
    return round(num)
  else:
    raise ValueError()

WNUM_TO_NUM = {
  "one": 1,
  "two": 2,
  "three": 3,
  "four": 4,
  "five": 5,
}
