from spacy.tokens import Token

(IN, IS_PUNCT, IS_SENT_START, LOWER, OP, ORTH, POS, REGEX, TAG) = (
  "IN", "IS_PUNCT", "IS_SENT_START", "LOWER", "OP", "ORTH", "POS", "REGEX", "TAG"
)
(LEFT_ID, REL_OP, RIGHT_ID, RIGHT_ATTRS) = ("LEFT_ID", "REL_OP", "RIGHT_ID", "RIGHT_ATTRS")

def is_word(token: Token) -> bool:
  return not token.is_punct and not token.is_space

# LEFT
def left_tokens(token: Token | None) -> list[Token]:
  if not token:
    return []
  return list(token.doc[token.sent.start:token.i])

def left_token(token: Token | None) -> Token | None:
  if not token:
    return None
  ltokens = left_tokens(token)
  return ltokens[-1] if ltokens else None

# RIGHT
def right_tokens(token: Token | None) -> list[Token]:
  if not token:
    return []
  return list(token.doc[token.i+1:token.sent.end])

def right_token(token: Token | None) -> Token | None:
  if not token:
    return None
  rtoks = right_tokens(token)
  return rtoks[0] if rtoks else None

# LEVELS
def ancestors(token: Token) -> list[Token]:
  tok = token
  toks: list[Token] = []
  while tok != tok.head:
    tok = tok.head
    toks.append(tok)
  return toks

def right_ancestors(token: Token) -> list[Token]:
  tok = token
  toks: list[Token] = []
  while tok != tok.head:
    tok = tok.head
    if tok.i > token.i:
      toks.append(tok)
    else:
      break
  return toks

def token_level(token: Token) -> int:
  level = 0
  while token != token.sent.root:
    level += 1
    token = token.head
  return level
