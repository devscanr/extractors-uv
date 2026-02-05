from dataclasses import dataclass
from typing import Literal

type CategorizedRole = Literal["Dev", "Nondev", "Org", "Student"]

@dataclass
class Categorized:
  role: CategorizedRole | None
  is_freelancer: bool | None
  is_lead: bool | None
  is_remote: bool | None
  is_hireable: bool | None
