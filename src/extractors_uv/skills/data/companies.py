from ..tag import Company, Skill

SKILLS: list[Skill] = [
  # == Companies not (yet/intentionally) extracted into their own modules ==

  # BIGTECH
  Company("AMD", ["(@)amd", "amd=32", "amd=64"]),
  Company("Autodesk", ["(@)autodesk"]),
  Company("eBay", ["(@)ebay"]),
  Company("Facebook", ["(@)facebook"]), # TODO meta?
  Company("IBM", ["(@)ibm"]),
  Company("Intel", ["(@)intel"]),
  Company("Kaggle", ["(@)kaggle"]),
  Company("Mozilla", ["(@)mozilla"]),
  Company("Netflix", ["(@)netflix"]),
  Company("NVidia", ["(@)nvidia"]),
  Company("SalesForce", ["(@)salesforce"]),
  Company("SAP", ["(@)sap"]),
  Company("Vercel", ["(@)vercel"]),
]
