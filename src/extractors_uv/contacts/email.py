import re
from ..utils import uniq

# Taken from https://github.com/fabian-hiller/valibot
EMAIL = r"[\w+-]+(?:\.[\w+-]+)*@[\da-z]+(?:[.-][\da-z]+)*\.[a-z]{2,}"

# Note: underscores are not universally allowed in emails

def parse_emails(ntext: str) -> list[str]:
  if not ntext:
    return []
  # Notes:
  # - https://stackoverflow.com/questions/1423195/what-is-the-actual-minimum-length-of-an-email-address-as-defined-by-the-ietf
  # - https://stackoverflow.com/questions/386294/what-is-the-maximum-length-of-a-valid-email-address
  emails = re.findall(EMAIL, ntext, re.IGNORECASE)
  return uniq(
    email for email in emails
    if 6 <= len(email) <= 254
  )
