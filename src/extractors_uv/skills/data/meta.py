from ..tag import Company, Skill, Tech
from ..utils import dis_incontext, dis_namelike, dis_nounlike
from ...xpatterns import ver1

SKILLS: list[Skill] = [
  Company("Facebook", ["(@)facebook", "meta.com"]), # TODO meta?

  Tech("Meta-Llama", [ver1("llama")]),
]
