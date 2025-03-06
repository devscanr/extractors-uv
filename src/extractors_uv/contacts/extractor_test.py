# mypy: disable-error-code=no-untyped-def
import pytest
from textwrap import dedent
from ..utils import normalize
from ..web import markdown2text
from .extractor import Contacts, ContactExtractor

class Test_ContactExtractor:
  @pytest.fixture(scope="class")
  def ex(self):
    return ContactExtractor()

  @pytest.fixture(scope="class")
  def extract(self, ex: ContactExtractor):
    def do(text: str) -> Contacts:
      ntext = normalize(text)
      return ex.extract(ntext)
    return do

  @pytest.fixture(scope="class")
  def extract_many(self, ex: ContactExtractor):
    def do(texts: list[str]) -> list[Contacts]:
      ntexts = [normalize(text) for text in texts]
      return ex.extract_many(ntexts)
    return do

  def test_extract_many_smoke(self, extract_many) -> None:
    assert extract_many(["foo@google.com", "bar@yandex.ru"]) == [
      Contacts(emails=["foo@google.com"], phones=[], urls=[]),
      Contacts(emails=["bar@yandex.ru"], phones=[], urls=[])
    ]

  def test_extract_set1(self, extract) -> None:
    assert extract("email: bishal-hadka-1600@gg.com phone: 970-799-9291") == Contacts(
      emails = ["bishal-hadka-1600@gg.com"],
      phones = ["9707999291"],
      urls = [],
    )
    assert extract("Phone: 9046571689 https://justin-rick.com") == Contacts(
      emails = [],
      phones = ["9046571689"],
      urls = ["https://justin-rick.com"],
    )

  def test_extract_set2(self, extract) -> None:
    assert extract("email: bishal-hadka-1600@gg.com phone: 970-799-9291") == Contacts(
      emails = ["bishal-hadka-1600@gg.com"],
      phones = ["9707999291"],
      urls = [],
    )
    assert extract("Phone: 9046571689 https://justin-rick.com") == Contacts(
      emails = [],
      phones = ["9046571689"],
      urls = ["https://justin-rick.com"],
    )

  def test_extract_md1(self, extract) -> None:
    md = c("""
      # Hi there! 👋

      [![Vienna](https://raw.githubusercontent.com/hu8813/hu8813/main/weather_badge.svg)](https://playing-with-fastapi.vercel.app/weather/vienna)

      Welcome to my GitHub profile!

      <a href="https://scabbiaza.net">Test1</a>

      [Test2](https://paqmind.com)

      ## 🌱 What I'm Learning

      I'm currently sharpening my skills in: ![C Logo](https://img.shields.io/badge/-C-000000?style=flat-square&logo=C&logoColor=white) ![C++ Logo](https://img.shields.io/badge/-C++-000000?style=flat-square&logo=C%2B%2B&logoColor=white) ![Python Logo](https://img.shields.io/badge/-Python-008000?style=flat-square&logo=Python&logoColor=white)

      Feel free to connect with me and share your coding adventures! 🚀

      [![committers.top badge](https://user-badge.committers.top/austria/hu8813.svg)](https://user-badge.committers.top/austria/hu8813)
    """)
    txt = markdown2text(md)
    assert extract(txt) == Contacts(
      emails = [],
      phones = [],
      urls = ["https://playing-with-fastapi.vercel.app/weather/vienna", "https://scabbiaza.net", "https://paqmind.com"],
    )

  def test_extract_md2(self, extract) -> None:
    md = c("""
      <div>
        <a href="https://github.com/Sabya-sachi-Seal">
        <img width=100% src="https://raw.githubusercontent.com/Sabya-sachi-Seal/Sabya-sachi-Seal/ouput/action2.gif" href="https://github.com/Sabya-sachi-Seal" /></a>
      </div>
      <h1>
        <a href="https://github.com/Sabya-sachi-Seal">
          <img width=7% height=15% src="https://raw.githubusercontent.com/Sabya-sachi-Seal/Sabya-sachi-Seal/ouput/Hi.gif"/>
        </a>
        I'm a
        <a href="https://github.com/Sabya-sachi-Seal">
          <img align=center width=100% src="https://readme-typing-svg.herokuapp.com?font=Sora&color=%2336BCF7&size=35&center=true&vCenter=true&width=600%&lines=Cloud+Computing+Enthusiast;Cybersecurity+Passionate;Data+Science+Practitioner;AI+%26+ML+Enthusiast;Computer+Science+Undergrad;Tech+Blogger" />
        </a>
      </h1>
    """)
    txt = markdown2text(md)
    assert extract(txt) == Contacts(
      emails = [],
      phones = [],
      urls = ["https://github.com/Sabya-sachi-Seal"],
    )

  def test_extract_md3(self, extract) -> None:
    md = c("""
      <a href="mailto:test1@gmail.com"><img src="https://svg.herokuapp.com"/></a>
      <a href="mailto:test2@gmail.com">test2</a>
      <a href="https://test3.com">test3</a>

      [![alt](https://svg.herokuapp.com)](mailto:test4@gmail.com)
      [![](https://svg.herokuapp.com)](mailto:test5@gmail.com)
      [test6](mailto:test6@gmail.com)
      [test7](https://test7.com)
    """)
    txt = markdown2text(md)
    assert extract(txt) == Contacts(
      emails = ["test1@gmail.com", "test2@gmail.com", "test4@gmail.com", "test5@gmail.com", "test6@gmail.com"],
      phones = [],
      urls = ["https://test3.com", "https://test7.com"],
    )

  def test_extract_md4(self, extract) -> None:
    md = c("""
      <div>
      <a href="mailto:iam.sabya-sachi@gmail.com">
         <img src="https://readme-typing-svg.herokuapp.com?font=Sora&color=%2336BCF7&center=true&vCenter=true&width=450%&lines=iam.sabya-sachi@gmail.com" />
           <img src="https://readme-typing-svg.herokuapp.com?font=Sora&color=%232CF7E4&center=true&vCenter=true&width=450%&lines=(%2B91)+991-042-7807" />
         </a>
        </div>
      <div>
         <a href="https://github.com/Sabya-Sachi-Seal"><img src="https://raw.githubusercontent.com/Sabya-Sachi-Seal/Sabya-Sachi-Seal/ouput/divider.gif"></a>
      </div>
        <div>
         <a href="https://www.youtube.com/channel/UC5VBAKQWkYdrALsQ_W8woCg">
         <img alt="Youtube" src="https://readme-typing-svg.herokuapp.com?font=Sora&color=e3d20c&center=true&vCenter=true&width=450%&lines=Watch+some+of+my+videos+?" />
            </a>
      </div>
    """)
    txt = markdown2text(md)
    assert extract(txt) == Contacts(
      emails = ["iam.sabya-sachi@gmail.com"],
      phones = [],
      urls = ["https://github.com/Sabya-Sachi-Seal", "https://www.youtube.com/channel/UC5VBAKQWkYdrALsQ_W8woCg"],
    )

def c(text: str) -> str:
  return dedent(text).strip()
