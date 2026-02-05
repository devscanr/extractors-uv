# mypy: disable-error-code=no-untyped-def
import pytest
from ..utils import normalize
from .url import parse_urls

# The logic is already tested in the library. So just to double-check...

class Test_parse_urls:
  @pytest.fixture(scope="class")
  def parse(self):
    def do(text: str) -> list[str]:
      ntext = normalize(text)
      return parse_urls(ntext)
    return do

  def test_parse_urls_smoke(self, parse) -> None:
    assert parse("""
      <a href="https://google.com">test1</a>
      [test2](https://facebook.com)
      https://gizmo.com/foo/bar?x=X#xxx
      scabbiaza.net
      ./aaa.txt
      bbb.txt
      /ccc.txt
      mailto:me@gg.net
      gg.ggx
      gg.gg
    """) == ["https://google.com", "https://facebook.com", "https://gizmo.com/foo/bar?x=X#xxx", "scabbiaza.net", "gg.gg"]
