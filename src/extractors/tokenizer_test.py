# mypy: disable-error-code=no-untyped-def
import pytest
from extractors.tokenizer import modify_tokenizer
from extractors.utils import get_nlp

class Test_Tokenizer:
  @pytest.fixture(scope="class")
  def tokenize(self):
    nlp = get_nlp("en_core_web_lg")
    modify_tokenizer(nlp)
    def do(text: str) -> list[str]:
      return [tok.text for tok in nlp(text)]
    return do

  def test_split_ampersand(self, tokenize) -> None:
    assert tokenize("@foo") == ["@foo"]
    assert tokenize("foo@bar") == ["foo@bar"]
    assert tokenize("foo@bar.com") == ["foo@bar.com"]
    assert tokenize("foo@bar-baz.com") == ["foo@bar-baz.com"]
    assert tokenize("foo+bar@bar-baz.com") == ["foo+bar@bar-baz.com"]
    assert tokenize("foo@ bar") == ["foo", "@", "bar"]

  def test_split_hashmark(self, tokenize) -> None:
    assert tokenize("#foo") == ["#", "foo"]
    assert tokenize("#foo-bar") == ["#", "foo", "-", "bar"]
    assert tokenize("#123") == ["#", "123"]
    assert tokenize("C#") == ["C#"]
    assert tokenize("123#") == ["123#"]

  def test_split_plus(self, tokenize) -> None:
    assert tokenize("+123") == ["+123"]
    assert tokenize("+123-321") == ["+123", "-", "321"]
    assert tokenize("18+") == ["18", "+"] # EWT
    assert tokenize("+foo") == ["+", "foo"]
    assert tokenize("+foo-bar") == ["+", "foo", "-", "bar"]
    assert tokenize("junior+") == ["junior+"]
    assert tokenize("middle+") == ["middle+"]
    assert tokenize("dev+ops") == ["dev", "+", "ops"]

  def test_split_minus(self, tokenize) -> None:
    assert tokenize("-123") == ["-123"]
    assert tokenize("-123-321") == ["-123", "-", "321"]
    assert tokenize("18-") == ["18", "-"]
    assert tokenize("-foo") == ["-", "foo"]
    assert tokenize("-foo-bar") == ["-", "foo", "-", "bar"]
    assert tokenize("junior-") == ["junior-"]
    assert tokenize("middle-") == ["middle-"]
    assert tokenize("dev-ops") == ["dev", "-", "ops"]

  def test_split_comma(self, tokenize) -> None:
    assert tokenize(",123") == [",", "123"]
    assert tokenize("123,") == ["123", ","]
    assert tokenize("123,45") == ["123,45"]
    assert tokenize(",foo") == [",", "foo"]
    assert tokenize("foo,") == ["foo", ","]
    assert tokenize("foo,bar") == ["foo", ",", "bar"]

  def test_split_colon(self, tokenize) -> None:
    assert tokenize(":123") == [":", "123"]
    assert tokenize("123:") == ["123", ":"]
    assert tokenize("23:59") == ["23:59"]
    assert tokenize(":foo") == [":", "foo"]
    assert tokenize("foo:") == ["foo", ":"]
    assert tokenize("foo:bar") == ["foo", ":", "bar"]
    assert tokenize("http://foobar.com") == ["http://foobar.com"] # captured by `match_url`

  def test_split_dot(self, tokenize) -> None:
    assert tokenize(".123") == [".123"]
    assert tokenize("123.") == ["123", "."]
    assert tokenize("123.45") == ["123.45"]
    assert tokenize(".gitignore") == [".gitignore"]
    assert tokenize("foo.") == ["foo", "."]
    assert tokenize("foo.bar stuff.net") == ["foo.bar", "stuff.net"] # captured by `match_url`
    assert tokenize("foo.Bar") == ["foo", ".", "Bar"]                # not captured by `match_url`
    assert tokenize("java.lang.Math") == ["java.lang", ".", "Math"]  # is not captured by `match_url`
    assert tokenize("NODE.JS") == ["NODE.JS"] # captured by `match_token` (exception rules)
    assert tokenize("Web.Py") == ["Web.Py"]   # captured by `match_token` (exception rules)

  def test_split_slash(self, tokenize) -> None:
    assert tokenize("/123") == ["/", "123"]
    assert tokenize("123/") == ["123", "/"]
    assert tokenize("123/45") == ["123", "/", "45"]
    assert tokenize("/foo") == ["/", "foo"]
    assert tokenize("foo/") == ["foo", "/"]
    assert tokenize("foo/bar") == ["foo", "/", "bar"]
    assert tokenize("/foo/bar.com") == ["/", "foo", "/", "bar.com"] # the last token is captured by `match_url`
    assert tokenize("foo/bar.js") == ["foo", "/", "bar.js"]         # the last token is captured by `match_url`
    assert tokenize("foo.com/bar") == ["foo.com/bar"]               # full token is captured by `match_url`

  # def test_split_ampersand(self, tokenize) -> None:
  #   assert tokenize("&123") == ["/", "123"]
  #   assert tokenize("123&") == ["123", "/"]
  #   assert tokenize("123&45") == ["123", "/", "45"]
  #   assert tokenize("&foo") == ["/", "foo"]
  #   assert tokenize("foo&") == ["foo", "/"]
  #   assert tokenize("foo&bar") == ["foo", "/", "bar"]
  #   assert tokenize("&foo&bar.com") == ["/", "foo", "/", "bar.com"] # the last token is captured by `match_url`
  #   assert tokenize("foo&bar.js") == ["foo", "/", "bar.js"]         # the last token is captured by `match_url`
  #   assert tokenize("foo.com&bar") == ["foo.com/bar"]               # full token is captured by `match_url`
  #
  #   assert tokenize("&123") == ["/", "123"]
  #   assert tokenize("123&") == ["123", "/"]
  #   assert tokenize("123&45") == ["123", "/", "45"]
  #   assert tokenize("&foo") == ["/", "foo"]
  #   assert tokenize("foo&") == ["foo", "/"]
  #   assert tokenize("foo&bar") == ["foo", "/", "bar"]
  #   assert tokenize("&foo&bar.com") == ["/", "foo", "/", "bar.com"] # the last token is captured by `match_url`
  #   assert tokenize("foo&bar.js") == ["foo", "/", "bar.js"]         # the last token is captured by `match_url`
  #   assert tokenize("foo.com&bar") == ["foo.com/bar"]               # full token is captured by `match_url`
