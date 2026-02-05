# mypy: disable-error-code=no-untyped-def
import pytest
from ..utils import normalize
from .email import parse_emails

# The logic is already tested in the library. So just to double-check...

class Test_parse_emails:
  @pytest.fixture(scope="class")
  def parse(self):
    def do(text: str) -> list[str]:
      ntext = normalize(text)
      return parse_emails(ntext)
    return do

  def test_parse_emails_smoke(self, parse) -> None:
    # Emails are fake (generated). Potential clashes with real contacts are non-intentional.
    assert parse("email: bishal-hadka-1600@gg.com phone: 970-799-9291") == ["bishal-hadka-1600@gg.com"]
    assert parse("akashkash934@hotmail.ru") == ["akashkash934@hotmail.ru"]
    assert parse("Email, Phone, other contacts") == []
    assert parse("Email: justin.rick@gmail.com Phone: 9046571689") == ["justin.rick@gmail.com"]
    assert parse("huyhain926guyen@gmail.com salmanzuck@zoho.com") == ["huyhain926guyen@gmail.com", "salmanzuck@zoho.com"]
