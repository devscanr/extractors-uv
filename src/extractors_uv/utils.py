from collections.abc import Callable, Iterable
from emoji import replace_emoji
import hashlib
from pathlib import Path
import re
import spacy
from spacy import Language
from spacy.lang.tokenizer_exceptions import URL_PATTERN
from spacy.tokens import Doc, Token
from typing import Any, cast
from .tokenizer import modify_tokenizer
from .xpatterns import IN, IS_PUNCT, IS_SENT_START, LOWER, ORTH, TAG, tag_jj, tag_nnp

URL_RE = re.compile(URL_PATTERN)
I_RE = re.compile("^i[A-Z]")
DECORATION_RE = re.compile(r"[\u00A6\u00A9\u00AE\u00B0\u0482\u058D\u058E\u060E\u060F\u06DE\u06E9\u06FD\u06FE\u07F6\u09FA\u0B70\u0BF3-\u0BF8\u0BFA\u0C7F\u0D4F\u0D79\u0F01-\u0F03\u0F13\u0F15-\u0F17\u0F1A-\u0F1F\u0F34\u0F36\u0F38\u0FBE-\u0FC5\u0FC7-\u0FCC\u0FCE\u0FCF\u0FD5-\u0FD8\u109E\u109F\u1390-\u1399\u1940\u19DE-\u19FF\u1B61-\u1B6A\u1B74-\u1B7C\u2100\u2101\u2103-\u2106\u2108\u2109\u2114\u2116\u2117\u211E-\u2123\u2125\u2127\u2129\u212E\u213A\u213B\u214A\u214C\u214D\u214F\u218A\u218B\u2195-\u2199\u219C-\u219F\u21A1\u21A2\u21A4\u21A5\u21A7-\u21AD\u21AF-\u21CD\u21D0\u21D1\u21D3\u21D5-\u21F3\u2300-\u2307\u230C-\u231F\u2322-\u2328\u232B-\u237B\u237D-\u239A\u23B4-\u23DB\u23E2-\u2426\u2440-\u244A\u249C-\u24E9\u2500-\u25B6\u25B8-\u25C0\u25C2-\u25F7\u2600-\u266E\u2670-\u2767\u2794-\u27BF\u29BE-\u29BF\u2800-\u28FF\u2B00-\u2B2F\u2B45\u2B46\u2B4D-\u2B73\u2B76-\u2B95\u2B98-\u2BC8\u2BCA-\u2BFE\u2CE5-\u2CEA\u2E80-\u2E99\u2E9B-\u2EF3\u2F00-\u2FD5\u2FF0-\u2FFB\u3004\u3012\u3013\u3020\u3036\u3037\u303E\u303F\u3190\u3191\u3196-\u319F\u31C0-\u31E3\u3200-\u321E\u322A-\u3247\u3250\u3260-\u327F\u328A-\u32B0\u32C0-\u32FE\u3300-\u33FF\u4DC0-\u4DFF\uA490-\uA4C6\uA828-\uA82B\uA836\uA837\uA839\uAA77-\uAA79\uFDFD\uFFE4\uFFE8\uFFED\uFFEE\uFFFC\uFFFD\U00010137-\U0001013F\U00010179-\U00010189\U0001018C-\U0001018E\U00010190-\U0001019B\U000101A0\U000101D0-\U000101FC\U00010877\U00010878\U00010AC8\U0001173F\U00016B3C-\U00016B3F\U00016B45\U0001BC9C\U0001D000-\U0001D0F5\U0001D100-\U0001D126\U0001D129-\U0001D164\U0001D16A-\U0001D16C\U0001D183\U0001D184\U0001D18C-\U0001D1A9\U0001D1AE-\U0001D1E8\U0001D200-\U0001D241\U0001D245\U0001D300-\U0001D356\U0001D800-\U0001D9FF\U0001DA37-\U0001DA3A\U0001DA6D-\U0001DA74\U0001DA76-\U0001DA83\U0001DA85\U0001DA86\U0001ECAC\U0001F000-\U0001F02B\U0001F030-\U0001F093\U0001F0A0-\U0001F0AE\U0001F0B1-\U0001F0BF\U0001F0C1-\U0001F0CF\U0001F0D1-\U0001F0F5\U0001F110-\U0001F16B\U0001F170-\U0001F1AC\U0001F1E6-\U0001F202\U0001F210-\U0001F23B\U0001F240-\U0001F248\U0001F250\U0001F251\U0001F260-\U0001F265\U0001F300-\U0001F3FA\U0001F400-\U0001F6D4\U0001F6E0-\U0001F6EC\U0001F6F0-\U0001F6F9\U0001F700-\U0001F773\U0001F780-\U0001F7D8\U0001F800-\U0001F80B\U0001F810-\U0001F847\U0001F850-\U0001F859\U0001F860-\U0001F887\U0001F890-\U0001F8AD\U0001F900-\U0001F90B\U0001F910-\U0001F93E\U0001F940-\U0001F970\U0001F973-\U0001F976\U0001F97A\U0001F97C-\U0001F9A2\U0001F9B0-\U0001F9B9\U0001F9C0-\U0001F9C2\U0001F9D0-\U0001F9FF\U0001FA60-\U0001FA6D]")

# RESOURCES
# - https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk
# - https://corenlp.run/

def clean_asian(text: str) -> str:
  # Drop "etc" in Japanese – e.g handle "Salesforceなど"
  text = text.replace("など", "")
  return text

def clean_unicode(text: str) -> str:
  # Replace emojis and decoration
  text = replace_emoji(text, "·")
  text = re.sub(DECORATION_RE, "·", text)
  # Drop sudo-emojis like ":snowflake:" which might overlap with skills
  text = re.sub(r":[-\w]+:", "!", text)
  return text

def normalize(text: str) -> str:
  # Remove junk characters
  text = clean_asian(text)
  text = clean_unicode(text)
  # Normalize non-conventional separators
  text = re.sub(r" ?[•·|][•·|\s]*", f" · ", text)
  # Normalize whitespace
  text = re.sub(r"[ \t]+", " ", text)
  # Workaround FPs for URLs – cases like "next.js/nuxt", look like URLs to NLP
  text = re.sub(r"(\.js)/(?=\w)", r"\1 / ", text, flags=re.IGNORECASE)
  # Workarounds for C# and C++ joined with separators
  text = re.sub(r"(?<!\w)(c(?:\+\+|#))([,/])(?=\w)", sep_splitter, text, flags=re.IGNORECASE)
  # Normalize sentence flow
  return normalize_sents(text)

def normalize_sents(text: str) -> str:
  result = ""
  paragraphs = re.split(r"\r?\n(\r?\n)+", text.strip())
  for paragraph in paragraphs:
    lines = re.split(r"\r?\n", paragraph)
    for l, line in enumerate(lines):
      line = trim(line)
      if line.strip():
        if l < len(lines) - 1:
          next_line = lines[l + 1].lstrip()
          if not next_line:
            result += decorate(line, ".")
          elif re.match(r"[-\w]+:", next_line) or re.match(r"--", next_line):
            result += decorate(line, ".")
          elif re.match(r"- \w", next_line):
            result += decorate(line, ";")
          else:
            result += decorate(line, "")
        else:
          result += decorate(line, ".")
        result += " "
  return result.rstrip()

def decorate(line: str, sep: str) -> str:
  tokens = line.split(" ")
  if should_capitalize_first(tokens[0]):
    if should_gap_last(tokens[-1]):
      return line[0].upper() + line[1:] + " " + sep
    else:
      sep = "" if tokens[-1].endswith((".", "?", "!", ",", ";", ":")) else sep
      return line[0].upper() + line[1:] + sep
  else:
    if should_gap_last(tokens[-1]):
      return line + " " + sep
    else:
      sep = "" if tokens[-1].endswith((".", "?", "!", ",", ";", ":")) else sep
      return line + sep

def should_capitalize_first(token: str) -> bool:
  return not re.search(URL_RE, token) and not re.search(I_RE, token)

def should_gap_last(token: str) -> bool:
  return bool(re.search(URL_RE, token))

def trim(line: str) -> str:
  # Trim wrapping decorations and whitespace
  return re.sub(r"(^[-~=\s>]+)|([-~=#@\s]+$)", "", line)
  # TODO we should ideally enforce " around > quotes

def sep_splitter(match: re.Match[str]) -> str:
  word, sep = match.group(1), match.group(2)
  return (
    word + f"{sep} " if sep in {","} else
    word + f" {sep} "
  )

def uniq[T](itr: Iterable[T]) -> list[T]:
  """
  Order-preserving uniq. Does not support nested lists and other non-hashable item types.
  """
  arr = list(itr)
  d = {}
  for x in arr:
    d[x] = 1
  keys = cast(Iterable[T], d.keys()) # Looks like MyPy (or something) is improperly typing this
  return list(keys)

def uniq2[T](itr: Iterable[T]) -> list[T]:
  """
  Order-preserving uniq. Supports nested lists and other non-hashable item types. Slower than the above.
  """
  arr = list(itr)
  return [x for i, x in enumerate(arr) if arr.index(x) == i]

def omit_parens(input: str) -> str:
  output = ""
  paren = 0
  for ch in input:
    if ch == "(":
      paren += 1
    elif ch == ")" and paren:
      paren -= 1
    elif not paren:
      output += ch
  return re.sub(r"\s+", " ", output)

def is_numstr(numstr: str) -> bool:
  return bool(re.fullmatch(r"\d+(\.\d+)?", numstr))

def is_numeric_token(token: Token | None) -> bool:
  return is_numstr(token.text) if token else False

# --------------------------------------------------------------------------------------------------
# Invalid grammar, especially punctuation, ruins Spacy analysis. I've found that
# it's much easier to fix common errors preventively, than to fight them post-factum.
# --------------------------------------------------------------------------------------------------

LB = r"(?<!\w)" # Builtin r"\b" does not fit us. E.g.
RB = r"(?!\w)"  # r"\beng.\b" won't match as right r"\b" wants left-side to be alphanum!

def drop_lastchar(match: re.Match[str]) -> str:
  return match.group(0)[0:-1]

def endwith_dash(match: re.Match[str]) -> str:
  return str(match.group(0)).rstrip("-. ") + "-"

type ReplaceFn = Callable[[re.Match[str]], str]

GRAMMAR_FIXES: list[tuple[str, str | ReplaceFn, re.RegexFlag | int]] = [
  (rf"{LB}free[-\s]+lanc([edring]*){RB}", r"freelanc\1", re.IGNORECASE), # does not preserve casing yet
  (rf"{LB}B\.?S\.?C?\.?{RB}|{LB}SC?\.?B\.?{RB}", r"B.S", re.IGNORECASE), # B.S  = Bachelor of Science
  (rf"{LB}M\.?S\.?C?\.?{RB}|{LB}SC\.?M\.?{RB}", r"M.S", re.IGNORECASE),  # M.S  = Master of Science (not handling "SM" forms for now)
  (rf"{LB}P\.?H\.?D?\.?{RB}", r"Ph.D", re.IGNORECASE),                   # Ph.D = Doctor of Philosophy
  (rf"{LB}eng\.{RB}", drop_lastchar, re.IGNORECASE),
  (rf"{LB}(co )(?=\w)", endwith_dash, re.IGNORECASE),
  (rf"{LB}(ex\.? )(?=\w)", endwith_dash, re.IGNORECASE),
  (rf"{LB}(non )(?=\w)", endwith_dash, re.IGNORECASE),
  (r" @ ", r" at ", re.IGNORECASE),
  (r"(?<!\b(at|of|in)) @(?=\w)", r" at @", re.IGNORECASE), # does not construct perfect casing yet
  (r" & ", r" and ", re.IGNORECASE),
  (r"(?<=[\w\s])/co-founder", r" / co-founder", re.IGNORECASE), # does not preserve casing yet
  (r"(?<=[\w\s])/co-owner", r" / co-owner", re.IGNORECASE), # does not preserve casing yet
  (r"(?<=[\w\s])/\.net", r" / .net", re.IGNORECASE),
  (rf"{LB}w/{RB}", r"with", re.IGNORECASE),
]

def fix_grammar(text: str) -> str:
  for pattern, replacement, flags in GRAMMAR_FIXES:
    text = re.sub(pattern, replacement, text, count=0, flags=flags)
  return text

def add_dev_exceptions(nlp: Language) -> None:
  # Covers most common cases (ideally, we should retrain the model)
  ruler = cast(Any, nlp.get_pipe("attribute_ruler"))
  problematic = ["Go", "Lit", "Next", "Node", "React", "REST"]
  # "go.", "react."
  ruler.add([
    [{LOWER: orth.lower(), IS_SENT_START: True}, {ORTH: "."}]
    for orth in problematic
  ], tag_nnp, index=0)
  # "go", "react" -- can't be trivially implemented due to missing IS_SENT_START (need a custom component mess)
  # ...           -- solved as disambiguations
  # "foo Go. bar Next"
  ruler.add([
    [{ORTH: orth, IS_SENT_START: False}]
    for orth in problematic
  ], tag_nnp, index=0)
  # "#go, #node, #next"
  ruler.add([
    [{ORTH: "#"}, {LOWER: orth.lower()}]
    for orth in problematic
  ], tag_nnp, index=1)
  # "; go,"
  ruler.add([
    [{IS_PUNCT: True}, {LOWER: orth.lower()}, {IS_PUNCT: True}]
    for orth in problematic
  ], tag_nnp, index=1)
  # e.g. "_/go"
  ruler.add([
    [{ORTH: "/"}, {LOWER: orth.lower()}]
    for orth in problematic
  ], tag_nnp, index=1)
  # e.g. "go/_"
  ruler.add([
    [{LOWER: orth.lower()}, {ORTH: "/"}]
    for orth in problematic
  ], tag_nnp, index=0)
  # React Native
  ruler.add([
    [{LOWER: "react"}, {LOWER: "native"}]
  ], tag_nnp, index=0)
  ruler.add([
    [{LOWER: "react"}, {LOWER: "native"}]
  ], tag_nnp, index=1)
  ruler.add([
    [{LOWER: "react"}, {ORTH: "-"}, {LOWER: "native"}]
  ], tag_nnp, index=0)
  ruler.add([
    [{LOWER: "react"}, {ORTH: "-"}, {LOWER: "native"}]
  ], tag_nnp, index=1)
  ruler.add([
    [{LOWER: "react"}, {ORTH: "-"}, {LOWER: "native"}]
  ], tag_nnp, index=2)

def add_jj_exceptions(nlp: Language, items: list[str]) -> None:
  ruler = cast(Any, nlp.get_pipe("attribute_ruler"))
  for item in items:
    spacecount = item.count(" ")
    if spacecount >= 1:
      raise ValueError("JJ items with >= 1 spaces are not supported")
    else:
      ruler.add([[
        {LOWER: item.lower(), TAG: {IN: ["NN", "NNP", "NNS", "NNPS"]}},
        {TAG: {IN: ["NN", "NNP", "NNS", "NNPS", "CD"]}},
      ]], tag_jj)

def add_jj_exceptions2(nlp: Language, items: list[str]) -> None:
  ruler = cast(Any, nlp.get_pipe("attribute_ruler"))
  for item in items:
    spacecount = item.count(" ")
    if spacecount >= 1:
      raise ValueError("VBG items with >= 1 spaces are not supported")
    else:
      ruler.add([[
        {TAG: {IN: ["VBG"]}}, {LOWER: item.lower()},
      ]], tag_jj, index=1)

def get_nlp(name: str | Path="en_core_web_md") -> Language:
  nlp = spacy.load(name, exclude=["lemmatizer", "ner"])

  # Custom components
  nlp.add_pipe("index_tokens_by_sents", after="parser")

  modify_tokenizer(nlp)

  # Make the following PROPER NOUNs
  add_dev_exceptions(nlp)
  # add_nnp_exceptions(nlp, [
  #   "computer science", # fixing POS, TAG, DEP, HEAD
  #   "deep learning",
  #   "data science",
  #   "machine learning",
  #   "software engineer",
  # ])
  add_jj_exceptions(nlp, [
    # Make the following ADJECTIVEs if before NOUNs
    "graduate", "graduated",
    "undergraduate", "undergraduated",
    "learning", "aspiring",
    "remote",
  ])
  add_jj_exceptions2(nlp, [
    # Make the following ADJECTIVEs if after VERBs
    "leading",
  ])
  return nlp

@Language.factory("index_tokens_by_sents")
def component(nlp: Language, name: str) -> Callable[[Doc], Doc]:
  del nlp, name
  def index_tokens_by_sents(doc: Doc) -> Doc:
    for token in doc:
      token._.i = token.i - token.sent.start
    return doc
  return index_tokens_by_sents

def hash_skillname(text: str) -> str:
  return hashlib.md5(text.encode()).hexdigest()[:12]

# TODO remove `_.used` extension if it's no longer necessary :)

def lookslike(lower: str, patt: re.Pattern[str]) -> bool:
  for match in re.finditer(patt, lower):
    start, end = match.span()
    lb = (lower[start-1] if start > 0 else "", lower[start])
    rb = (lower[end-1], lower[end] if end < len(lower) else "")
    is_left_bounded = (
      not lb[0].isalpha() or
      lb[0].islower() and lb[1].isupper() or
      lb[0].isupper() and lb[1].islower()
    )
    is_right_bounded = (
      not rb[1].isalpha() or
      rb[0].islower() and rb[1].isupper() or
      rb[0].isupper() and rb[1].islower()
    )
    if is_left_bounded and is_right_bounded:
      return True
  return False

def includes[T](itr: Iterable[T], subitr: Iterable[T]) -> bool:
  arr, subarr = list(itr), list(subitr)
  la, ls = len(arr), len(list(subarr))
  if not la or not ls:
    return False
  for i in range(0, la):
    try:
      for j in range(0, ls):
        if arr[i + j] != subarr[j]:
          raise ValueError()
      return True
    except (IndexError, ValueError):
      pass
  return False

# def merge_overlapping(matches: list[set[int]]) -> list[set[int]]:
#   rs: list[set[int]] = []
#   for k, match in enumerate(matches):
#     for l, other_match in enumerate(matches):
#       if k != l:
#         if match & other_match:
#           ms = [match | other_match]
#           ms.extend(match for m, match in enumerate(matches) if m != k and m != l)
#           return merge_overlapping(ms)
#     rs.append(match)
#   if rs == matches:
#     return matches
#   else:
#     return merge_overlapping(rs)

def takewhile[T](pred: Callable[[T], bool], xs: Iterable[T]) -> Iterable[T]:
  xs_ = list(xs)
  for x in xs_:
    if not pred(x):
      break
    yield x

def revtakewhile[T](pred: Callable[[T], bool], xs: Iterable[T]) -> Iterable[T]:
  xs_ = list(xs)
  for x in reversed(xs_):
    if not pred(x):
      break
    yield x

def takeuntil[T](pred: Callable[[T], bool], xs: Iterable[T]) -> Iterable[T]:
  for x in xs:
    if pred(x):
      break
    yield x

def revtakeuntil[T](pred: Callable[[T], bool], xs: Iterable[T]) -> Iterable[T]:
  xs_ = list(xs)
  for x in reversed(xs_):
    if pred(x):
      break
    yield x

def revlist[T](xs: Iterable[T]) -> list[T]:
  return list(reversed(list(xs)))
