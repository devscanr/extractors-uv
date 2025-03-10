from ...xpatterns import ver1
from ..tag import Language, Skill
from ..utils import dis_incontext, dis_letterlike, dis_namelike, dis_nounlike, dis_precisely, dis_verblike

SKILLS: list[Skill] = [
  # QUERY LANGUAGES
  Language("GraphQL", ["graphql", "graphiql"]),
  Language("SQL", ["sql"]),

  # PROGRAMMING LANGUAGES
  Language("Ada", ["ada"]),
  Language("Apex", ["apex"]),
  Language("Assembly", ["assembly", "asm"], "An umbrella term for low-level languages where instructions in the language are basically CPU instructions"),
  Language("C", ["c-lang"]),
  Language("C", ["c(.)"], disambiguate=dis_letterlike()), # disambiguate from "c." like in "c. 1, c. 2" (chapter)
  Language("C++", ["c++", "cpp", "c=plus=plus"]),
  Language("C#", ["c#", "csharp"]),
  Language("Clojure", ["clojure", "clojurian"]),
  Language("ClojureScript", ["clojure=script"]),
  Language("Cobol", ["cobol"]),
  Language("Crystal", ["crystal-lang", "crystal"]),
  Language("D", ["d=lang"]),
  Language("D", ["d"], disambiguate=dis_letterlike()),
  Language("Dart", ["dart"]),
  Language("Delphi", ["delphi"]),
  Language("Elixir", ["elixir"]),
  Language("Elm", ["elm"]),
  Language("Erlang", ["erlang"]),
  Language("Fortran", ["fortran"]),
  Language("F#", ["f#", "f=lang", "fsharp"]),
  Language("Gleam", ["gleam"]),
  Language("Go", ["golang", "gopher"]),
  Language("Go", ["go"], disambiguate=dis_verblike()),
  Language("Groovy", ["groovy"]),
  Language("Haskell", ["haskell"]),
  Language("Java", [ver1("java"), "java-se"]),
  Language("JavaScript", ["java=script", "js"]),
  Language("Julia", ["julia"], disambiguate=dis_namelike()),
  Language("Kotlin", ["kotlin"]),
  Language("Lisp", ["lisp"]),
  Language("Lua", ["lua"]),
  Language("Nim", ["nim"]),
  Language("Matlab", ["matlab"]),
  Language("Mojo", ["mojo"]),
  Language("Objective-C", ["objective=c(.)", "objective=c++", "objective=cpp"]),
  Language("Ocaml", ["ocaml"]),
  Language("Odin", ["odin"]),
  Language("-Odin", ["odin-project"]),
  Language("Perl", [ver1("perl")]),
  Language("PHP", [ver1("php"), "phper"]),
  Language("PowerShell", ["power=shell"]),
  Language("Prolog", ["prolog"]),
  Language("Python", [ver1("python"), "py", "pythonist(a)"]),
  Language("R", ["r=lang"], "Programming language for statistical computing and data visualization"),
  Language("R", ["r"], disambiguate=dis_letterlike()),
  Language("Ruby", ["ruby=lang", "ruby", "rubyist", "rubist"]),
  Language("Rust", ["rust", "rustacean"]),
  Language("Scala", ["scala"]),
  Language("TypeScript", ["type=script", "ts"]),
  Language("Shell", ["shell", "bash", "zsh"]),
  Language("V", ["vlang"]),
  Language("V", ["v"], disambiguate=dis_letterlike()),
  Language("Vala", ["vala"]),
  Language("Visual-Basic", ["visual=basic", "vb(a)", "vb.net"]),
  Language("Zig", ["zig"]),

  # CONTRACT LANGUAGES
  Language("Cairo", ["cairo"]),
  Language("Solidity", ["solidity"]),
  Language("Vyper", ["vyper"]),

  # OTHER LANGUAGES
  Language("CSS", [ver1("css")]),
  Language("CSV", ["csv"]),
  Language("GQL", ["gql"]), # TODO Cypher
  Language("HTML", [ver1("html")]),
  Language("JSON", ["json", "json5"]),
  Language("LESS", ["less"], disambiguate=[
    dis_precisely("LESS"),
    dis_incontext("sass", "scss"),
    dis_nounlike(),
  ]),
  Language("Makefile", ["makefile"]),
  Language("Markdown", ["markdown", "md"]),
  Language("SASS", ["sass", "scss"]),
  Language("SVG", ["svg"]),
  Language("WebAssembly", ["wasm", "web=assembly"]),
  Language("XML", ["xml"]),
  Language("YAML", ["yaml"]),
]
