from lingua import Language, LanguageDetectorBuilder
from typing import Literal, cast

# https://github.com/pemistahl/lingua-py/discussions/240

detector = LanguageDetectorBuilder.from_languages(*[
  Language.ENGLISH, Language.RUSSIAN, # Language.GERMAN,
  # Language.POLISH, Language.RUSSIAN, Language.UKRAINIAN,
  # Language.SERBIAN, Language.CROATIAN,
  # Language.JAPANESE, Language.HINDI, Language.CHINESE, Language.SLOVENE,
  # Language.CZECH, Language.SLOVAK, Language.FRENCH, Language.DUTCH, Language.DANISH,
  # Language.FINNISH, Language.NYNORSK, Language.SWEDISH, Language.ESTONIAN,
]).with_minimum_relative_distance(0.05).build()

Lang = Literal["ENG", "RUS"]

def detect_language_iso639(text: str) -> Lang | None:
  """
  Lingua-Py does no support multi-lingual text detection yet.
  """
  values = detector.compute_language_confidence_values(text)
  for value in values:
    if value.value > 0.75:
      return cast(Lang, value.language.iso_code_639_3.name)
  return None
