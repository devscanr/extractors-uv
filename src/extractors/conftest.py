import pytest
from spacy import Language
from .utils import get_nlp

@pytest.fixture(scope="session")
def nlp() -> Language:
  return get_nlp("en_core_web_lg")
  # return get_nlp("./model-best")
