from bs4 import BeautifulSoup, Comment, NavigableString, ParserRejectedMarkup, Tag
from markdown import markdown
import re

def html2text(html: str) -> str:
  soup = BeautifulSoup(html, features="html.parser")
  texts: list[str] = []
  for element in soup.descendants:
    if isinstance(element, NavigableString) and not isinstance(element, Comment):
      text = element.strip()
      if element.parent and element.parent.name == "code":
        if text:
          texts.append("/Code/")
      elif element.parent and element.parent.name == "a":
        href = str(element.parent.get("href", ""))
        if href.startswith("mailto:"):
          texts.append(f"{text.capitalize() or "Email"}: {href}")
        elif href and text and "://" not in text:
          texts.append(f"{text.capitalize()}: {href}")
        elif text:
          texts.append(text)
      elif text:
        texts.append(text)
    elif isinstance(element, Tag) and element.name == "a":
      if not element.get_text().strip():
        # ^ Non-empty cases are handled by the first branch
        href = str(element.get("href", ""))
        if href.startswith("mailto:"):
          texts.append(f"Email: {href}")
        elif is_whitelist_url(href):
          texts.append(f"URL: {href}")
        elif href:
          texts.append("/URL/")

  return "\n\n".join(text for text in texts)

def html2text_(html: str) -> str:
  try:
    return html2text(html)
  except ParserRejectedMarkup:
    return ""

def markdown2text(md: str) -> str:
  if not md:
    return ""
  html = markdown(md, extensions=["fenced_code"])
  return html2text(html)

def markdown2text_(html: str) -> str:
  try:
    return markdown2text(html)
  except ParserRejectedMarkup:
    return ""

def is_whitelist_url(href: str) -> bool:
  return re.search(WHITE_DOMAINS_REGEX, href) is not None

WHITE_DOMAINS_REGEX = r"\b" + r"|".join([
  r"about\.me",
  r"behance\.net",
  r"bio\.link",
  r"buymeacoffee\.com",
  r"codecademy\.com",
  r"codepen\.io",
  r"codersrank\.io",
  r"codewars\.com",
  r"dev\.to",
  r"discord\.com",
  r"discordapp\.com",
  r"dribbble\.com",
  r"facebook\.com",
  r"fb\.com",
  r"github\.com",
  r"github\.io",
  r"gitlab\.com",
  r"habr\.com",
  r"hashnode\.com",
  r"hashnode\.dev",
  r"herokuapp\.com",
  r"hexlet\.io",
  r"hh\.ru",
  r"instagram\.com",
  r"kaggle\.com",
  r"leetcode\.com",
  r"linkedin\.com",
  r"linktr\.ee",
  r"medium\.com",
  r"netlify\.app",
  r"patreon\.com",
  r"reddit\.com",
  r"showwcase\.com",
  r"stackoverflow\.com",
  r"stackshare\.io",
  r"t\.me",
  r"tiktok\.com",
  r"tilda\.ws",
  r"toptal\.com",
  r"twitch\.tv",
  r"twitter\.com",
  r"udemy\.com",
  r"upwork\.com",
  r"vercel\.app",
  r"vk\.com",
  r"vk\.me",
  r"wordpress\.com",
  r"wordpress\.org",
  r"youtube\.com",
  r"x\.com",
]) + r"\b"
