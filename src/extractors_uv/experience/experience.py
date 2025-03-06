from dataclasses import dataclass
import typing
from typing import Literal
from typing_extensions import TypeIs

type ExactExperienceKind = Literal["Exact"] # no `type` kw due to https://github.com/python/cpython/issues/112472
type OtherExperienceKind = Literal["Intern", "Junior", "Middle", "Senior", "Principal"] # /
type ExperienceKind = ExactExperienceKind | OtherExperienceKind

@dataclass
class Experience:
  kind: ExperienceKind      # Junior-Middle will be represented is {kind: Junior, over: True}
  months: int | None = None # months or years converted to months
  over: bool = False        # years+

def is_ExactExperienceKind(s: str) -> TypeIs[ExactExperienceKind]:
  return s in typing.get_args(ExactExperienceKind.__value__)

def is_OtherExperienceKind(s: str) -> TypeIs[OtherExperienceKind]:
  return s in typing.get_args(OtherExperienceKind.__value__)

def is_ExperienceKind(s: str) -> TypeIs[ExperienceKind]:
  return s in typing.get_args(ExperienceKind.__value__)
