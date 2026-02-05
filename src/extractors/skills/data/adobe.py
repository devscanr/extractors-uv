from ...xpatterns import ver1
from ..tag import Company, Skill, Tech

SKILLS: list[Skill] = [
  Company("Adobe", ["(@)adobe"]),

  # Low-Code
  Tech("Adobe-Commerce", ["adobe=commerce", "magento-enterprise", ver1("magento")]),
  Tech("Adobe-CC", ["adobe=cc", "adobe=creative=cloud"]),
  Tech("Adobe-Illustrator", ["adobe=illustrator"]), # TODO disambig. Illustrator
  Tech("Adobe-Photoshop", ["adobe=photoshop", "photoshop"]),
]
