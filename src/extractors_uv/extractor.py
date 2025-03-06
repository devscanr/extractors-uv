from collections.abc import Callable, Sequence
from dataclasses import dataclass
import re
from spacy import Language
from spacy.matcher import DependencyMatcher, Matcher, PhraseMatcher
from spacy.tokens import Doc, Token
from typing import Any, NamedTuple, cast
from .ppatterns import to_ppatterns
from .spacyhelpers import token_level
from .utils import hash_skillname, uniq2
from .dpatterns import DPattern, separate_dphantoms, separate_xphantoms, to_dpatterns2
from .xpatterns import XPattern, literal

class OMatch(NamedTuple):
  mname: str
  offsets: list[int]

class TMatch(NamedTuple):
  name: str
  tokens: list[Token]

class UMatch(NamedTuple):
  name: str
  tokens: list[Token]
  maintoken: Token

type Disambiguate = Callable[[Token], bool]

@dataclass
class Tag:
  name: str
  phrases: Sequence[
    str |      # Custom (converted to XPattern, DPattern or expanded)
    XPattern | # Matcher pattern
    DPattern   # DependencyMatcher pattern
  ]
  descr: str
  exclusive: bool
  disambiguate: Disambiguate | list[Disambiguate] | None
  @property
  def ambiguous(self) -> bool:
    return bool(self.disambiguate)

class BaseExtractor:
  """
  Custom alternative for entity recognition, since the latter is incompatible
  with `DependencyMatcher` and does not provide any disambiguation mechanics.
  """

  def __init__(self, nlp: Language, tags: Sequence[Tag]):
    self.nlp = nlp
    # == Simplicity -> Flexibility ==
    # PMatcher -> XMatcher -> DMatcher
    self.pmatcher = PhraseMatcher(self.nlp.vocab, attr="LOWER") # fastest, direct phrases
    self.xmatcher = Matcher(self.nlp.vocab)                     # pattern-based
    self.dmatcher = DependencyMatcher(self.nlp.vocab)           # pattern-based+
    self.descrs: dict[str, str] = {}
    self.exclusives: dict[str, bool] = {}
    self.disambiguates: dict[str, list[Disambiguate]] = {}
    self.phantoms: dict[str, list[int]] = {}
    self.init_matchers(tags)

  def init_matchers(self, tags: Sequence[Tag]) -> None:
    for tag in tags:
      mname = attach_maybe(tag.name) if tag.ambiguous else tag.name
      # Update descriptions
      if tag.name not in self.descrs:
        self.descrs[tag.name] = tag.descr
      # Update exclusives
      assert (
        self.exclusives[tag.name] == tag.exclusive
        if tag.name in self.exclusives
        else True
      ), f"varying `exclusive` at {tag.name!r}"
      self.exclusives[tag.name] = tag.exclusive
      # Update disambiguate fns
      if tag.disambiguate is not None:
        assert mname not in self.disambiguates, f"duplicate `disambiguate` at {tag.name!r}"
        self.disambiguates[mname] = tag.disambiguate if isinstance(tag.disambiguate, list) else [tag.disambiguate]
      # Update matchers with patterns
      for phrase in tag.phrases:
        if isinstance(phrase, str):
          if "<" in phrase or (">" in phrase and not "->" in phrase): # hack
            assert "-" not in phrase, f"Dashes are not supported yet with dep. operations: {phrase!r}"
            assert " " not in phrase, f"Spaces are not supported yet with dep. operations: {phrase!r}"
            dpatterns = to_dpatterns2([phrase])
            for dpattern in dpatterns:
              dpattern, dphantoms = separate_dphantoms(dpattern)
              if dphantoms:
                k = len(self.phantoms) + 1
                pname = attach_phantom(mname, k)
                self.phantoms[pname] = dphantoms
                self.dmatcher.add(pname, [dpattern])
              else:
                self.dmatcher.add(mname, [dpattern])
          else:
            if re.search("[A-Z]", phrase):
              self.xmatcher.add(mname, [literal(p) for p in to_ppatterns([phrase])])
            else:
              pipe = cast(Any, self.nlp.tokenizer).pipe # `tokenizer.pipe` is untyped in Spacy @_@
              self.pmatcher.add(mname, list(pipe(to_ppatterns([phrase]))))
        elif isinstance(phrase, list) and len(phrase):
          if "RIGHT_ID" in phrase[0]:
            dpattern, dphantoms = separate_dphantoms(phrase)
            # print("dpattern:", dpattern)
            if dphantoms:
              k = len(self.phantoms) + 1
              pname = attach_phantom(mname, k)
              self.phantoms[pname] = dphantoms
              self.dmatcher.add(pname, [dpattern])
            else:
              self.dmatcher.add(mname, [dpattern])
          else:
            xpattern, xphantoms = separate_xphantoms(phrase)
            # print("xpattern:", xpattern)
            if xphantoms:
              k = len(self.phantoms) + 1
              pname = attach_phantom(mname, k)
              self.phantoms[pname] = xphantoms
              self.xmatcher.add(pname, [xpattern])
            else:
              self.xmatcher.add(mname, [xpattern])

  def find_omatches(self, doc: Doc) -> list[OMatch]:
    """
    Find offset-based matches (a union-set of xmatches, pmatches, dmatches)
    """
    omatches: list[OMatch] = []
    xmatches = self.xmatcher(doc) if len(self.xmatcher) else []
    pmatches = self.pmatcher(doc) if len(self.pmatcher) else []
    dmatches = self.dmatcher(doc) if len(self.dmatcher) else []
    for pmatch in pmatches:
      [match_id, start, end] = pmatch
      mname = self.nlp.vocab.strings[match_id]
      omatches.append(OMatch(mname, list(range(start, end))))
    for xmatch in xmatches:
      [match_id, start, end] = xmatch
      offsets = list(range(start, end)) # global offsets
      pname = self.nlp.vocab.strings[match_id]
      if pname in self.phantoms:
        offsets = [offs for o, offs in enumerate(offsets) if o not in self.phantoms[pname]]
      mname = detach_phantom(pname) # Can still contain ":maybe"...
      omatches.append(OMatch(mname, offsets))
    for dmatch in dmatches:
      [match_id, offsets] = dmatch # global offsets
      pname = self.nlp.vocab.strings[match_id]
      if pname in self.phantoms:
        offsets = [offs for o, offs in enumerate(offsets) if o not in self.phantoms[pname]]
      mname = detach_phantom(pname) # Can still contain ":maybe"...
      omatches.append(OMatch(mname, offsets))
    # DMatcher often produces duplicates (graph-based pattern)
    omatches = uniq2(omatches)
    # print("omatches:", omatches)
    return omatches

  def find_tmatches(self, doc: Doc) -> list[TMatch]:
    """
    Find token-based matches, preserving only unambiguous
    """
    omatches = self.find_omatches(doc)
    tmatches: list[TMatch] = []
    for omatch in omatches:
      tokens = [doc[offset] for offset in omatch.offsets]
      maintoken = (
        tokens[-1]
        if all([token_level(t) == token_level(tokens[0]) for t in tokens])
        else min(tokens, key=lambda t: token_level(t))
      )
      name = detach_maybe(omatch)
      if name == omatch.mname:
        tmatches.append(TMatch(name, tokens))
      else:
        if name.startswith("-"):
          raise ValueError("disambiguation for negations is not supported yet")
        if any(disambiguate(maintoken) for disambiguate in self.disambiguates[omatch.mname]):
          tmatches.append(TMatch(name, tokens))
    tmatches = uniq2(tmatches)
    # Discard canceled matches
    tmatches2: list[TMatch] = []
    for tmatch in tmatches:
      other_tmatches = [tmat for tmat in tmatches if tmatch != tmat]
      if not any([self.is_canceled_by(tmatch, other_tm) for other_tm in other_tmatches]):
        tmatches2.append(tmatch)
    # print("tmatches2:", tmatches2)
    return tmatches2

  def find_umatches(self, doc: Doc) -> tuple[list[UMatch], list[UMatch]]:
    """
    Find unique matches by merging overlapping and/or neighboring matches
    """
    tmatches = self.find_tmatches(doc)
    # Merge overlapping and neighboring sets of offsets (for the same tagname)
    _matches = merge_overlapping([
      (tmatch.name, set([tok.i for tok in tmatch.tokens]))
      for tmatch in tmatches
    ])
    # print("_matches:", _matches)
    # Derive umatches with properly sorted tokens from tmatches
    umatches: list[UMatch] = []
    unmatches: list[UMatch] = []
    for name, offsets in _matches:
      tokens = [doc[i] for i in sorted(offsets)]
      maintoken = (
        tokens[-1]
        if all([token_level(t) == token_level(tokens[0]) for t in tokens])
        else min(tokens, key=lambda t: token_level(t))
      )
      if name.startswith("-"):
        unmatches.append(UMatch(name, tokens, maintoken))
      else:
        umatches.append(UMatch(name, tokens, maintoken))
    # Sort umatches and unmatches by their maintokens' indexes
    umatches.sort(key=lambda umat: umat.maintoken.i)
    unmatches.sort(key=lambda umat: umat.maintoken.i)
    # print("umatches:", umatches)
    # print("unmatches:", unmatches)
    return umatches, unmatches

  def is_canceled_by(self, match: TMatch, other_match: TMatch) -> bool:
    exclusive = self.exclusives[match.name]
    other_exclusive = self.exclusives[other_match.name]
    soffsets = {tok.i for tok in match.tokens}
    other_soffsets = {tok.i for tok in other_match.tokens}
    if other_match.name in {"-", "-" + match.name}:
      return bool(soffsets & other_soffsets)
    # # TODO potentially prefer longer name (with more dashes) as more precisef
    if soffsets < other_soffsets:
      # Ignore an exclusive match in case of another, wider exclusive match
      return exclusive and other_exclusive
    elif soffsets == other_soffsets:
      # For VPC and AWS-VPC matching "aws ... vpc" we prefer AWS-VPC as more specific
      return exclusive and other_exclusive and match.name in other_match.name.split("-")
    return False

def is_maybe(mname_or_omatch: str | OMatch) -> bool:
  mname = mname_or_omatch if isinstance(mname_or_omatch, str) else mname_or_omatch.mname
  return ":maybe:" in mname

def attach_maybe(name: str) -> str:
  return name + ":maybe:" + hash_skillname(name)

def detach_maybe(mname_or_omatch: str | OMatch) -> str:
  mname = mname_or_omatch if isinstance(mname_or_omatch, str) else mname_or_omatch.mname
  name = re.sub(r":maybe:.+(?=$|:)", "", mname)
  return name

# Phantoms (serve similar purpose to Regex lookaheads and lookbehinds – limit matches but aren't captured)
def attach_phantom(name: str, k: int) -> str:
  return name + f":ph{k}"

def detach_phantom(pname: str) -> str:
  name = re.sub(r":ph\d+(?=$|:)", "", pname)
  return name

type M = tuple[str, set[int]]

def merge_overlapping(matches: list[M]) -> list[M]:
  # Recursive solution, can be probably be rewritten in imperative `while (True)` style if necessary.
  """
  assert merge_overlapping([
    ("JS", {7}),
    ("Senior", {1, 2}),
    ("Senior", {1, 3}), # [senior fullstack] developer vs [senior] fullstack [developer]
    ("SQL", {1}),
    ("PHP", {4}),
    ("Senior", {1, 2, 3}),
  ]) == [("JS", {7}), ('Senior', {1, 2, 3}), ('SQL', {1}), ('PHP', {4})]
  """
  rs: list[M] = []
  for k, (name, offsets) in enumerate(matches):
    for l, (other_name, other_offsets) in enumerate(matches):
      if k != l:
        if name == other_name and (offsets & other_offsets or is_neighboring(offsets, other_offsets)):
          common_name = name if is_maybe(other_name) else other_name
          ms = [(common_name, offsets | other_offsets)]
          ms.extend(match for m, match in enumerate(matches) if m != k and m != l)
          return merge_overlapping(ms)
    rs.append((name, offsets))
  if rs == matches:
    return matches
  else:
    return merge_overlapping(rs)

def is_neighboring(s1: set[int], s2: set[int]) -> bool:
  min1, min2 = min(s1), min(s2)
  max1, max2 = max(s1), max(s2)
  if abs(min1 - min2) == 1 or abs(max1 - max2) == 1:
    return True
  if abs(min1 - max2) == 1 or abs(max1 - min2) == 1:
    return True
  return False
