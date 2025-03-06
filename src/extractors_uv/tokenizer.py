from spacy import Language
from spacy.util import compile_infix_regex, compile_prefix_regex, compile_suffix_regex

QUOTES = [r"'", r'"', r'”', r'“', r"„", r"‘", r"’", r"«", r"»", r"`", r"´"]
BRACKETS = [r"\(", r"\)", r"\[", r"\]", r"\{", r"\}", r"<", r">"]
CURRENCIES = [r"\$", "£", "€", "¥", "฿", r"US\$", r"C\$", r"A\$", "₽", "﷼", "₴", "₠₣", "₤", "₥", "₦", "₧", "₨", "₩", "₪", "₫", "€", "₭", "₮", "₯", "₰", "₱", "₲", "₳", "₴", "₵", "₶", "₷", "₸", "₹", "₺", "₻", "₼", "₽", "₾", "₿"]

# Keep only symbols that potentially bear semanthics. Everything else should be removed at normalization.

PREFIXES = [
  r"\.\.+",
  r"§",
  r"%",
  r"#", # to not duplicate all skills with #, EWT is internally inconsistent about # splitting
  r"=",
  r"—",
  r"–",
  r"-+(?!\d)",  # -11 is kept single token in EWT treebank
  r"\++(?!\d)", # +8 is kept single token in EWT treebank
  r"…",
  r",",
  r";",
  r":+",
  r"\!+",
  r"\?+",
  r"¿", r"؟", r"¡",
  *BRACKETS,
  r"•",
  r"·",
  r"#(?=\d)",
  r"\*",
  r"×",
  r"÷",
  r"/+",
  r"&+",
  r"\|+",
  r"。", r"？", r"！", r"，", r"、", r"；", r"：", r"～", r"।", r"،", r"۔", r"؛", r"٪",
  *QUOTES,
  *CURRENCIES,
]

SUFFIXES = [
  r"\.\.+",
  r"§",
  r"%",
  r"@",
  r"=",
  r"—",
  r"–",
  r"-+",
  r"\++",
  r"…",
  r",",
  r";",
  r":+",
  r"\!+",
  r"\?+",
  r"¿", r"؟", r"¡",
  *BRACKETS,
  r"•",
  r"·",
  r"\*",
  r"×",
  r"÷",
  r"/+",
  r"&+",
  r"\|+",
  r"。", r"？", r"！", r"，", r"、", r"；", r"：", r"～", r"।", r"،", r"۔", r"؛", r"٪",
  *QUOTES,
  r"['’][sS]",
  r"(?<=°[FfCcKk])\.",
  r"(?<=\d)(?:\$|£|€|¥|฿|US\$|C\$|A\$|₽|﷼|₴|₠|₡|₢|₣|₤|₥|₦|₧|₨|₩|₪|₫|€|₭|₮|₯|₰|₱|₲|₳|₴|₵|₶|₷|₸|₹|₺|₻|₼|₽|₾|₿)",
  r"(?<=\d)(?:km[²³]?|m[²³]?|dm|dm²|dm³|cm|cm²|cm³|mm|mm²|mm³|ha|µm|nm|yd|in|ft|kg|g|mg|µg|t|lb|oz|m/s|km/h|kmh|mph|hPa|Pa|mbar|T|G|M|K|%|км|км²|км³|м|м²|м³|дм|дм²|дм³|см|см²|см³|мм|мм²|мм³|нм|кг|г|мг|м/с|км/ч|кПа|Па|мбар|Кб|КБ|кб|Мб|МБ|мб|Гб|ГБ|гб|Тб|ТБ|тбكم|كم²|كم³|م|م²|م³|سم|سم²|سم³|مم|مم²|مم³|كم|غرام|جرام|جم|كغ|ملغ|كوب|اكواب)",
  r"(?<=\d)(?:mi?b|Mi?[Bb]|ki?b|Ki?[Bb]|gi?b|Gi?[Bb]|ti?b|Ti?[Bb])",
  r"(?<=\d)(?:yo)",
  r"\.(?!\d)",
]

INFIXES = [
  r"(?<=[\w\d)])\.\.+(?=[\w\d(])",
  r"(?<=[\w\d)])§(?=[\w\d(])",
  r"(?<=[\w\d)])%(?=[\w\d(])",
  r"(?<=[\w\d)])=(?=[\w\d(])",
  r"(?<=[\w\d)])—(?=[\w\d(])",
  r"(?<=[\w\d)])–(?=[\w\d(])",
  r"(?<=[\w\d)])-(?=[\w\d(])",
  r"(?<=[\w\d)])\+(?=[\w\d(])",
  r"(?<=[\w\d)])…(?=[\w\d(])",
  r"(?<!\d),(?!\d)",
  r"(?<=[\w\d)]);(?=[\w\d(])",
  r"(?<=[\w\d)])\!+(?=[\w\d(])",
  r"(?<=[\w\d)])\?+(?=[\w\d(])",
  r"(?<=[\w\d)])[¿؟¡](?=[\w\d(])",
  *[rf"(?<=[\w\d]){b}(?=[\w\d])" for b in BRACKETS],
  r"(?<=[-+\w\d)])•(?=[\w\d(])",
  r"(?<=[-+\w\d)])·(?=[\w\d(])",
  r"(?<=[\w\d)])\*(?=[\w\d(])",
  r"(?<=[\w\d)])×(?=[\w\d(])",
  r"(?<=[\w\d)])÷(?=[\w\d(])",
  r"(?<=[-+\w\d)])/+(?=[\w\d(])",
  r"(?<=[-+\w\d)])&+(?=[\w\d(])",
  r"(?<=[-+\w\d)])\|+(?=[\w\d(])",
  *[rf"(?<=[\w\d)]){q}(?=[\w\d(])" for q in QUOTES if q not in {r"'", r"’"}],
  r"(?<!\d):(?!\d)",
  r"(?<=[\w\d])\.(?=[A-ZА-Я])",
]

prefix_regex = compile_prefix_regex(PREFIXES)
suffix_regex = compile_suffix_regex(SUFFIXES)
infix_regex = compile_infix_regex(INFIXES)

def modify_tokenizer(nlp: Language) -> None:
  tokenizer = nlp.tokenizer

  # Special cases are strictly cases-sensitive (unfortunately) and can affect sentence boundaries.
  # for abbr in ["c#", "C#", "c++", "C++", ".net", ".Net", ".NET", "->", "16+", "18+", "21+", "ex.", "EX.", "Ex."]:
  #   tokenizer.add_special_case(abbr, [{"ORTH": abbr}])
  # tokenizer.add_special_case("...gimme...?", [{ORTH: "...gimme...?"}])
  # tokenizer.add_special_case("c++", [{ORTH: "c++"}])
  # tokenizer.add_special_case("C++", [{ORTH: "C++"}])
  # tokenizer.add_special_case("c#", [{ORTH: "c#"}])
  # tokenizer.add_special_case("C#", [{ORTH: "C#"}])
  # tokenizer.add_special_case("C++", [{ORTH: "C"}, {ORTH: "++"}])
  # tokenizer.add_special_case("C#", [{ORTH: "C"}, {ORTH: "#"}])

  tokenizer.prefix_search = prefix_regex.search    # type: ignore
  tokenizer.suffix_search = suffix_regex.search    # type: ignore
  tokenizer.infix_finditer = infix_regex.finditer  # type: ignore
  tokenizer.token_match = nlp.Defaults.token_match # type: ignore
  tokenizer.url_match = nlp.Defaults.url_match     # type: ignore

  # Tokenizer exceptions
  def token_match(text: str) -> bool | None:
    lower = text.lower()
    if lower in {"c+", "c++", "c#", ".net", "ph.d", "->", "ex.", "tl/dr", "tl;dr", "w/"}:
      return True
    if lower in {
      "month+", "months+", "year+", "years+",
      "junior+", "junior-", "middle+", "middle-", "intermediate+", "intermediate-",
      "senior+", "senior-", "principal+", "principal-"
    }:
      return True
    if lower.startswith(("co-",)) and not lower.endswith((".", ",", "/", ";", ":", "?", "!")): # "ex-"
      return True
    if lower.endswith((".js", ".py", ".net")) and not lower.startswith((".", ",", "/", ";", ":", "?", "!")):
      if not set(lower) & {"/"}:
        return True
    return False
  tokenizer.token_match = token_match # type: ignore

  # Tokenizer exceptions (sometimes are applied after prefix/suffix, sometimes before – wtf)
  # def token_match(token: str) -> bool | None:
  #   # Preserve ".js"-like suffixes
  #   return False
  # nlp.tokenizer.token_match = token_match # type: ignore

  # tokenizer.add_special_case("C++", [{ORTH: "C"}, {ORTH: "++"}])
  # tokenizer.add_special_case("C#", [{ORTH: "C"}, {ORTH: "#"}])
