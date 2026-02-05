from urlextract import URLExtract # type: ignore
from ..utils import uniq

extractor = URLExtract()

def parse_urls(ntext: str) -> list[str]:
  # TODO smart deduplicate
  if not ntext:
    return []
  urls = extractor.find_urls(ntext)
  return uniq(
    url.strip("()[]{} ")
    for url in urls # The library mistakenly grabs trailing "]" and ")" in MD
    if len(url) <= 255
  )
