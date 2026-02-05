# mypy: disable-error-code=no-untyped-def
import pytest
from spacy import Language
from .utils import fix_grammar, normalize
from . import markers

# Note: offsets must be given as for normalized texts!
# "Ex-" and "Non-" become just "Ex" and "None" to cover Spacy issues.

class Test_is_hashtagged:
  @pytest.fixture(scope="class")
  def is_hashtagged(self, nlp: Language):
    def do(text: str, i: int) -> bool:
      ntext = fix_grammar(normalize(text))
      return markers.is_hashtagged(nlp(ntext)[i])
    return do

  def test_smoke(self, is_hashtagged) -> None:
    assert not is_hashtagged("Developer", 0)
    assert not is_hashtagged("A developer", 1)
    assert not is_hashtagged("I am a developer", 3)
    assert is_hashtagged("#developer", 1)
    assert is_hashtagged("#web-developer", 1)

class Test_is_negated:
  @pytest.fixture(scope="class")
  def is_negated(self, nlp: Language):
    def do(text: str, i: int) -> bool:
      ntext = fix_grammar(normalize(text))
      return markers.is_negated(nlp(ntext)[i])
    return do

  def test_no_indicators(self, is_negated) -> None:
    assert not is_negated("Developer", 0)
    assert not is_negated("A developer", 1)
    assert not is_negated("I am a developer", 3)

  def test_not_indicators(self, is_negated) -> None:
    assert is_negated("not developer", 1)        # ?developer
    assert is_negated("not a developer", 2)      # ?developer
    assert is_negated("not a web developer", 2)  # ?web
    assert is_negated("I am not a developer", 4) # ?developer

  def test_non_indicators(self, is_negated) -> None:
    # post-normalization offsets
    assert is_negated("non developer", 2)     # ?developer
    assert is_negated("non-developer", 2)     # ?developer
    assert is_negated("non web developer", 2) # ?developer
    assert is_negated("non web developer", 1) # ?web

  def test_adhoc1(self, is_negated):
    text = "not a senior web developer, a junior mobile qa"
    assert is_negated(text, 4) # ?developer
    assert is_negated(text, 3) # ?web
    assert is_negated(text, 2) # ?senior
    # assert not is_negated(text, 9) # ?qa
    # assert not is_negated(text, 8) # ?mobile
    # assert not is_negated(text, 7) # ?junior

class Test_is_past:
  @pytest.fixture(scope="class")
  def is_past(self, nlp: Language):
    def do(text: str, i: int) -> bool:
      ntext = fix_grammar(normalize(text))
      return markers.is_past(nlp(ntext)[i])
    return do

  def it_handles_no_indicators(self, is_past) -> None:
    assert not is_past("Non-developer", 1) # offset after norm.
    assert not is_past("Developer", 0)
    assert not is_past("A developer", 1)
    assert not is_past("I am a developer", 3)
    assert not is_past("I will be a developer", 4)

  def it_handles_ex_indicators(self, is_past) -> None:
    assert is_past("ex developer", 1)
    assert is_past("ex. developer", 1)
    assert is_past("ex-developer", 1)     # offsets after norm.
    assert is_past("ex-web developer", 2) # /

  def it_handles_past_indicators(self, is_past) -> None:
    assert is_past("Former developer", 1)
    assert is_past("A former developer", 2)
    assert is_past("Retired developers", 1)
    assert is_past("A retired developer", 2)
    assert is_past("Previously a developer at Facebook", 2)

  def it_handles_was_indicator(self, is_past) -> None:
    assert is_past("Previously I was a developer at Facebook", 4)
    assert is_past("I was developer", 2)
    assert is_past("I was a developer", 3)
    assert is_past("We were developers", 2)

  def it_handles_complex_cases1(self, is_past) -> None:
    text = "I was a developer now I am a manager"
    assert is_past(text, 3)     # developer
    assert not is_past(text, 8) # manager

  def it_handles_complex_cases2(self, is_past) -> None:
    text = "Today I'm developer yet I was manager"
    assert not is_past(text, 3) # developer
    assert is_past(text, 7)     # manager

  def it_handles_complex_cases3(self, is_past) -> None:
    text = "Former developer, currently a manager"
    assert is_past(text, 1)     # developer
    assert not is_past(text, 5) # manager

  def test_adhoc1(self, is_past):
    text = "An engineer, formerly a junior devops"
    assert is_past(text, 6) # ?devops
    assert is_past(text, 5) # ?junior
    assert not is_past(text, 1) # ?engineer

class Test_is_future:
  @pytest.fixture(scope="class")
  def is_future(self, nlp: Language):
    def do(text: str, i: int) -> bool:
      ntext = fix_grammar(normalize(text))
      return markers.is_future(nlp(ntext)[i])
    return do

  def test_no_indicators(self, is_future) -> None:
    assert not is_future("Non-developer", 1) # offset after norm.
    assert not is_future("Developer", 0)
    assert not is_future("A developer", 1)
    assert not is_future("I am a developer", 3)
    assert not is_future("I was a developer", 3)

  def test_future_indicators(self, is_future) -> None:
    assert is_future("Future developer", 1)
    assert is_future("A future developer", 2)
    assert is_future("Aspiring developer", 1)
    assert is_future("An aspiring developer", 2)
    assert is_future("Upcoming developer", 1)
    assert is_future("An upcoming developer", 2)

  def test_future_shortcuts(self, is_future) -> None:
    assert is_future("Wannabe developer", 1)
    assert is_future("Gonnabe developer", 1)
    assert is_future("Developer wannabe", 0)

  def test_will_indicators(self, is_future) -> None:
    assert is_future("I will be developer", 3)
    assert is_future("I will be a developer", 4)
    assert is_future("I will become developer", 3)
    assert is_future("I will become a developer", 4)
    assert is_future("I'll be developer", 3)
    assert is_future("I'll be a developer", 4)

  def test_plan_indicators(self, is_future) -> None:
    assert is_future("I plan to become developer", 4)
    assert is_future("Planning to be the developer", 4)
    assert is_future("Planning to become a developer", 4)
    assert is_future("Striving to become a developer", 4)
    assert is_future("I strive to be a developer", 5)
    assert is_future("Going to become developer", 3)
    assert is_future("Going to become a developer", 4)
    assert is_future("Gonna be developer", 3) # Tokenization yields [Gon, na]
    assert is_future("Gonna become a developer", 4) # Tokenization yields [Gon, na]

  def test_desire_indicators(self, is_future) -> None:
    assert is_future("Want to be a developer", 4)
    assert is_future("Carl wants to be a developer", 5)
    assert is_future("I wish to be a developer", 5)
    assert is_future("looking forward to become a developer", 5)

  def test_search_indicators(self, is_future) -> None:
    assert is_future("Looking for internship", 2)
    assert is_future("Looking for an internship", 3)
    assert is_future("Looking for internship opportunities", 2)
    assert is_future("Looking for an internship opportunity", 3)
    assert is_future("Seeking internship", 1)
    assert is_future("Seeking an internship", 2)
    assert is_future("Seeking internship opportunities", 1)
    assert is_future("Seeking an internship opportunity", 2)
    assert is_future("Open to an internship opportunity", 3)

  def test_adhoc1(self, is_future):
    text = "Currently a student, I will be a junior devops soon"
    assert is_future(text, 9) # ?devops
    assert is_future(text, 8) # ?junior
    assert not is_future(text, 2) # ?student
