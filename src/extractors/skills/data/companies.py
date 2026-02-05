from ..tag import Company, Skill

SKILLS: list[Skill] = [
  # == Companies not (yet/intentionally) extracted into their own modules ==

  # BIGTECH
  Company("AMD", ["(@)amd", "amd=32", "amd=64"]),
  Company("Autodesk", ["(@)autodesk"]),
  Company("eBay", ["(@)ebay"]),
  Company("IBM", ["(@)ibm"]),
  Company("Intel", ["(@)intel"]),
  Company("Kaggle", ["(@)kaggle"]),
  Company("Mozilla", ["(@)mozilla"]),
  Company("Netflix", ["(@)netflix"]),
  Company("NVidia", ["(@)nvidia"]),
  Company("SalesForce", ["(@)salesforce"]),
  Company("SAP", ["(@)sap"]),
  Company("Vercel", ["(@)vercel"]),

  Company("Anthropic", ["(@)anthropic"], "High-reasoning AI models"),
  Company("OpenAI", ["(@)open=ai"], "High-reasoning AI models"),
  Company("Groq", ["groq"], "Ultra-fast LPU inference engine"),
  Company("HuggingFace", ["hugging=face", "hf"], "Repository for open-source models"),
]
