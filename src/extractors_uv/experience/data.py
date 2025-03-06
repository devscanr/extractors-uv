from ..dpatterns import DPattern, DToken, LEFT_ID, PHANTOM, REL_OP, RIGHT_ATTRS, RIGHT_ID
from ..extractor import Tag
from .tag import ExpTag
from ..ppatterns import expandlist_parens as expl
from ..xpatterns import DEP, IN, LOWER, XPattern, x_lower, x_nounlike, x_orth, x_orthlower, x_regex

ROLES = expl([
  "administrator", "admin",
  "architect",
  "analyst",
  "coder",
  "dataop(s)",
  "developer", "dev",
  "devop(s)",
  "engineer", "eng",
  "mlop(s)",
  "netop(s)",
  "op(s)",
  "programmer",
  "qa",
  "researcher",
  "scientist",
  "secop(s)",
  "sysop(s)",
  "tester",
  # Special
  "backender",
  "frontender",
  "fullstacker",
])

SUDOROLES = expl([
  # Languages
  "c", "c.",
  "c++",
  "c#",
  "go",
  "javascript", "js",
  "kotlin",
  "php",
  "python",
  "ruby",
  "rust",
  "sql",
  "typescript", "ts",
  # Fields
  "backend",
  "blockchain(s)",
  "frontend",
  "fullstack",
  "game(s)",
  "mobile(s)",
  "network(s)",
  "security",
  "system(s)",
  "web",
  # Platforms
  "android",
  "ios",
  # Frameworks
  ".net",
  "asp.net",
  "angular(js)",
  "react(js)",
  "unity",
  "unreal",
  "vue",
])

P = {PHANTOM: True}

def d_token(word: str) -> DToken:
  return {RIGHT_ID: word, RIGHT_ATTRS: x_orthlower(word)}

def d_parent(child: str) -> DToken:
  return {REL_OP: "<", LEFT_ID: child}

def term_of_exp_patterns() -> list[Tag]:
  # Example: years* > of > experience
  return [
    tag
    for name, termreg in [("YOE", r"(?i)^years?\+?$"), ("MOE", r"(?i)^months?\+?$")]
    for exp in ["experience", "expertise"]
    for tag in [
      ExpTag(name, [[
        {RIGHT_ID: "term", RIGHT_ATTRS: x_regex(termreg)},
        {RIGHT_ID: "of", RIGHT_ATTRS: x_orthlower("of"), LEFT_ID: "term", REL_OP: ">"},
        {RIGHT_ID: exp, RIGHT_ATTRS: x_orthlower(exp), LEFT_ID: "of", REL_OP: ">"},
      ]]),
      ExpTag(name, [[
        x_regex(termreg),
        {LOWER: "of"},
        x_orthlower(exp),
      ]])
    ]
  ]

def term_exp_patterns() -> list[Tag]:
  # Example: years < experience*
  return [
    tag
    for name, reg in [("YOE", r"(?i)^years?\+?$"), ("MOE", r"(?i)^months?\+?$")]
    for exp in ["experience", "expertise"]
    for tag in [
      ExpTag(name, [[
        {RIGHT_ID: "term", RIGHT_ATTRS: x_regex(reg)},
        {RIGHT_ID: exp, RIGHT_ATTRS: x_orthlower(exp), LEFT_ID: "term", REL_OP: "<"},
      ]]),
      ExpTag(name, [[
        x_regex(reg),
        x_orthlower(exp),
      ]]),
    ]
  ]

def init_root_patterns(modifiers: list[str]) -> list[XPattern]:
  return [
    [{DEP: "ROOT", LOWER: modifier}]
    for modifier in modifiers
  ]

def init_role_patterns(modifiers: list[str]) -> list[str | DPattern]:
  return [
    pattern
    for anchor in ROLES
    for modifier in modifiers
    for pattern in [
      [
        # (modifier) (^anchor)
        x_orthlower(modifier),
        x_orthlower(anchor) | P,
      ],
      [
        # (modifier) (^-) (^anchor)
        x_orthlower(modifier),
        x_orth("-") | P,
        x_orthlower(anchor) | P,
      ],
      [
        # (modifier) ($nounlike) (^anchor)
        x_orthlower(modifier),
        x_nounlike() | P,
        x_orthlower(anchor) | P,
      ],
      [
        # (modifier) ($nounlike) ($nounlike) (^anchor)
        x_orthlower(modifier),
        x_nounlike() | P,
        x_nounlike() | P,
        x_orthlower(anchor) | P,
      ],
      [
        # (^anchor) (^-) (modifier)
        x_orthlower(anchor) | P,
        x_orth("-") | P,
        x_orthlower(modifier),
      ],
      [
        # (modifier) < (^anchor)
        d_token(modifier),
        d_token(anchor) | d_parent(modifier) | P,
      ],
    ]
  ]

def init_sudorole_patterns(modifiers: list[str]) -> list[str | DPattern]:
  return [
    pattern
    for anchor in SUDOROLES
    for modifier in modifiers
    for pattern in [
      [
        # (modifier) (^anchor)
        x_orthlower(modifier),
        x_orthlower(anchor) | P,
      ],
      [
        # (modifier) (^-) (^anchor)
        x_orthlower(modifier),
        x_orth("-") | P,
        x_orthlower(anchor) | P,
      ],
      [
        # (^anchor) (modifier)
        x_orthlower(anchor) | P,
        x_orthlower(modifier),
      ],
      [
        # (^anchor) (^-) (modifier)
        x_orthlower(anchor) | P,
        x_orth("-") | P,
        x_orthlower(modifier),
      ],
      [
        # (modifier) < (^anchor)
        d_token(modifier),
        d_token(anchor) | d_parent(modifier) | P,
      ],
    ]
  ]

RANGE_SENIORITIES = expl([
  "junior(+)", "junior-",
  "middle(+)", "middle-",
  "intermediate(+)", "intermediate-",
  "senior(+)", "senior-",
  "principal(+)", "principal-",
])

def init_sep_patterns(modifiers: list[str]) -> list[str | DPattern]:
  return [
    [
      x_lower(modifiers),
      x_orth(["/", "-", "|", ",", "->"]) | P,
      {LOWER: {IN: RANGE_SENIORITIES}} | P
    ],
    [
      {LOWER: {IN: RANGE_SENIORITIES}} | P,
      x_orth(["/", "-", "|", ",", "->"]) | P,
      x_lower(modifiers),
    ]
  ]

def init_intern_patterns() -> list[str | DPattern]:
  modifiers = expl(["intern", "internship", "trainee"])
  return [
    *modifiers,
    *init_role_patterns(modifiers),
    *init_sudorole_patterns(modifiers),
  ]

def init_junior_patterns() -> list[str | DPattern]:
  modifiers = expl(["junior(+)", "junior-"])
  return [
    *init_root_patterns(modifiers),
    *init_role_patterns(modifiers),
    *init_sudorole_patterns(modifiers),
    *init_sep_patterns(modifiers),
  ]

def init_middle_patterns() -> list[str | DPattern]:
  modifiers = expl(["middle(+)", "middle-", "intermediate(+)", "intermediate-"])
  return [
    *init_root_patterns(modifiers),
    *init_role_patterns(modifiers),
    *init_sudorole_patterns(modifiers),
    *init_sep_patterns(modifiers),
  ]

def init_senior_patterns() -> list[str | DPattern]:
  modifiers = expl(["senior(+)", "senior-"])
  return [
    *init_root_patterns(modifiers),
    *init_role_patterns(modifiers),
    *init_sudorole_patterns(modifiers),
    *init_sep_patterns(modifiers),
  ]

def init_principal_patterns() -> list[str | DPattern]:
  modifiers = expl(["principal(+)", "principal-"])
  return [
    *init_root_patterns(modifiers),
    *init_role_patterns(modifiers),
    *init_sudorole_patterns(modifiers),
  ]

TAGS: list[Tag] = [
  # EXACT
  *term_of_exp_patterns(),
  *term_exp_patterns(),

  # OTHER
  ExpTag("Intern", init_intern_patterns()),
  ExpTag("Junior", init_junior_patterns()),
  ExpTag("Middle", init_middle_patterns()),
  ExpTag("Senior", init_senior_patterns()),
  ExpTag("Principal", init_principal_patterns()),
]
