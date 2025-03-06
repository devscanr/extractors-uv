# mypy: disable-error-code=no-untyped-def
from extractors_uv.utils import normalize

class Test_normalize:
  def test_smoke(self) -> None:
    # This one mostly tests `normalize_sents`, we need more...
    assert normalize("""
      First?
      
      Second!
      
      Third-a
      Third-b
      foo: bar
      
      > foo
      > http://url.com
        
      - foo
      - email@url.com
      - bar
      """
    ) == "First? Second! Third-a Third-b. Foo: bar. Foo http://url.com . Foo; email@url.com ; Bar."
