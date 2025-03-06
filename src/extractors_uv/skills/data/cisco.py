from ..tag import Company, Skill, Tech

SKILLS: list[Skill] = [
  Company("Cisco", ["(@)cisco", "cysco=systems"]),

  # NETWORKS
  Tech("Cisco-ACI", ["cisco=aci"], "Software-defined networking (SDN) solution for data centers"),
  Tech("Cisco-Nexus", ["cisco=nexus"], "Modular and fixed port network switches for data centers"),
]
