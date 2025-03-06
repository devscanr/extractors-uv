from collections.abc import Sequence
from itertools import dropwhile
import re
from typing import Literal

from spacy.tokens import Doc, Span, Token
from ..categories.extractor import is_hashtagged
from ..extractor import BaseExtractor
from ..markers import is_future, is_negated, is_past
from ..utils import LB, RB

class TitleExtractor(BaseExtractor):
  def extract_many(self, text_or_docs: Sequence[str | Doc], tagfilter: Literal["Human", "Org"]) -> list[str]:
    if not text_or_docs:
      return []
    docs = self.nlp.pipe(text_or_docs) if isinstance(text_or_docs[0], str) else text_or_docs
    # LATER: `n_process` for multiprocessing
    return [self.extract(doc, tagfilter=tagfilter) for doc in docs]

  def extract(self, text_or_doc: str | Doc, tagfilter: Literal["Human", "Org"]) -> str:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # pprint(list(self.nlp.tokenizer.explain(text_or_doc)))
    # pprint([{"token": tok, "pos": tok.pos_, "dep": tok.dep_, "head": tok.head} for tok in doc if not tok.is_punct])

    umatches, unmatches = self.find_umatches(doc)
    ignore_tokens = [tok for _, tokens, _ in unmatches for tok in tokens]
    # print("umatches:", umatches)
    # print("ignore_tokens:", ignore_tokens)

    # Filter umatches additionally (TODO apply the same role canceling we do in `CategoryExtractor`)
    umatches2 = [
      (name, tokens, maintoken)
      for name, tokens, maintoken in umatches
      if (name == tagfilter or name.startswith(tagfilter + ":")) and (
        maintoken.head.text.startswith("@") or
        maintoken.dep_ not in {"amod", "compound", "dobj", "pobj"} or
        maintoken.dep_ == "pobj" and maintoken.head.lower_ == "as"
        # ^ TODO maybe analize a verb instead
      )
    ]
    # print("umatches2:", umatches2)

    # Extract spans
    spans: list[Span] = []
    for _, _, maintoken in umatches2:
      span = find_noun_span(maintoken, [list(span) for span in spans] + [ignore_tokens])
      if is_hashtagged(span.root):
        spans.append(span)
      elif not any(pred(span.root) for pred in [is_negated, is_past, is_future]):
        spans.append(span)
    # print("spans:", spans)

    # Drop overlapping spans (if span.root is in other span – prefer other span)
    final_spans = [
      span for span in spans
      if not any(span.root in other_span for other_span in spans if other_span != span)
    ]
    # print("final_spans:", final_spans)

    return format_spans(final_spans)
    # Note: Initially I planned to keep "former" titles if nothing else is found.
    #       But some forms, e.g. "I was a web engineer" require a reformatting, like
    #       "Ex Web Engineer", which does not fit the current span-only implementation.
    #       It might be changed in future, too complex for now.
    # self.format_subtrees(selected_subtrees) or self.format_subtrees(all_subtrees)

def is_hanging(token: Token) -> bool:
  if token.lower_ in {"year", "years", "old", "young", "new"}:
    return True
  if token.pos_ in {"NOUN", "PROPN", "ADJ"}:
    return False
  if token.pos_ == "VERB":
    return token.tag_ != "VBN" # Smth like "embedded" (VBN) -> False, otherwise -> True
  return True

def find_noun_span(token: Token, acc_spans: list[list[Token]]) -> Span:
  toks: list[Token] = []
  for tok in token.sent:
    if tok.is_punct:
      continue
    if tok == token:
      toks.append(tok) # [Developer]
    if not any(tok in span for span in acc_spans):
      if tok.text.startswith("@"):
        toks.append(tok)
      elif tok.head == token and tok.i < token.i:
        toks.append(tok) # [Senior] Developer, [Senior] PHP Developer
      elif tok.head.head == token and tok.i < token.i:
        toks.append(tok) # [Full]-Stack Developer
      elif tok.head.head.head == token and tok.i < token.i:
        toks.append(tok) # [Game] Engine Development Amateur
      elif tok.head == token and tok.i > token.i and tok.lower_ in {"at", "of"}:
        toks.append(tok)
      elif tok.head.head == token and tok.i > token.i and tok.head.lower_ in {"at", "of"}:
        toks.append(tok)
  toks = list(dropwhile(is_hanging, toks))
  toks = list(dropwhile(is_hanging, reversed(toks)))
  toks = list(reversed(toks))
  if len(toks):
    start, end = toks[0].i, toks[-1].i + 1
    return token.doc[start:end]
  else:
    return token.doc[0:0]

def get_token_text(token: Token) -> str:
  # Ensure that tokens are appended with correct case
  if token.pos_ in {"ADP", "CCONJ", "DET", "PART"}:
    text = str(token).lower()
  elif re.search(r"[A-Z]", token.text):
    text = str(token)
  else:
    text = str(token).title()
  return re.sub(r"^#", "", text)

def format_spans(spans: list[Span]) -> str:
  results: list[str] = []
  for ts1 in spans:
    ts2 = list(dropwhile(is_hanging, ts1))
    ts3 = list(dropwhile(is_hanging, reversed(ts2)))
    results.append(""
      .join(get_token_text(tok) + tok.whitespace_ for tok in reversed(ts3))
      .strip()
    )
  return " | ".join(results[0:3]).strip() # the slice length should depend on how long the items are...

MORE_GRAMMAR_FIXES: list[tuple[str, str, re.RegexFlag | int]] = [
  (rf"{LB}Professional{RB}", r"professional", 0), # to not receive PROPN by mistake, though will break company names with this word :(
  (rf"{LB}PROFESSIONAL{RB}", r"professional", 0),
  (rf"{LB}Remote{RB}", r"remote", 0), # prevents more serious Spacy bugs
  (rf"{LB}REMOTE{RB}", r"remote", 0),
]

def fix_more_grammar(text: str) -> str:
  for pattern, replacement, flags in MORE_GRAMMAR_FIXES:
    text = re.sub(pattern, replacement, text, count=0, flags=flags)
  return text
