from dataclasses import dataclass, field
from .email import parse_emails
from .phone import parse_phones
from .url import parse_urls

@dataclass
class Contacts:
  emails: list[str] = field(default_factory=list)
  phones: list[str] = field(default_factory=list)
  urls: list[str] = field(default_factory=list)

class ContactExtractor:
  def extract_many(self, ntexts: list[str]) -> list[Contacts]:
    return [self.extract(ntext) for ntext in ntexts]

  def extract(self, ntext: str) -> Contacts:
    if not ntext:
      return Contacts()
    return Contacts(
      emails = parse_emails(ntext),
      phones = parse_phones(ntext),
      urls = parse_urls(ntext),
    )
