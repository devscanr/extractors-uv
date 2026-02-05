import re
from ..utils import uniq

TRIGGERS = [
  r"(?:phone|mobile|tel)(?:\s*-?\s*(?:num\.?|numbers?))?\s*[:=-]{0,2}\s*",
  r"(?:to\s+reach\s+me)\s*[:=-]{0,2}\s*",
  r"(?:whatsapp|viber|telegram|tg|signal)\s*[:=-]{0,2}\s*",
]
NUMBER = r"([(+]{0,2}\s*\d[-\d().\s]+\d)"

TRIGGERED_NUMBERS = [
  (TRIGGER + NUMBER) for TRIGGER in TRIGGERS
]
INTERNATIONAL_NUMBER = r"(\+\d{1,3}[-\s]\d{1,5}[-\s][-\d\s]{4,}\d)"
URLED_NUMBER = "|".join([
  r"(?<!\w)(?:wa.me|t.me)/(\+?\d{7,14})",
])
# TODO viber://contact?number=%2B0000000000000

def parse_phones(ntext: str) -> list[str]:
  # TODO smart deduplicate
  if not ntext:
    return []
  phones1 = [
    phone
    for REGEX in TRIGGERED_NUMBERS
    for phone in re.findall(REGEX, ntext, re.IGNORECASE)
  ]
  phones2 = re.findall(INTERNATIONAL_NUMBER, ntext)
  phones3 = re.findall(URLED_NUMBER, ntext)
  phones = phones1 + phones2 + [ensure_plus_prefixed(p) for p in phones3]
  clean_phones = (
    re.sub(r"[-\s.()]", "", phone) for phone in phones
  )
  return uniq(
    phone for phone in clean_phones
    if 4 <= len(phone.strip("+")) <= 17
  )

def ensure_plus_prefixed(phone: str) -> str:
  return phone if phone.startswith("+") else ("+" + phone)
