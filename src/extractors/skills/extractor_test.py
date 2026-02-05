# mypy: disable-error-code=no-untyped-def
from collections.abc import Callable
import pytest
from spacy import Language
from ..utils import fix_grammar, normalize
from .data import SKILLS
from .extractor import SkillExtractor

class Test_SkillExtractor:
  @pytest.fixture(scope="class")
  def extract(self, nlp: Language):
    ex = SkillExtractor(nlp, SKILLS)
    def do(text: str) -> list[str]:
      return ex.extract(fix_grammar(normalize(text)))
    return do

  @pytest.fixture(scope="class")
  def extract_many(self, extract) -> Callable[[list[str]], list[list[str]]]:
    def do(texts: list[str]) -> list[list[str]]:
      return [extract(text) for text in texts]
    return do

  @pytest.fixture(scope="class")
  def extractset(self, extract) -> Callable[[str], set[str]]:
    def do(text: str) -> set[str]:
      return set(extract(text))
    return do

  # SMOKE
  def test_extract_smoke(self, extract) -> None:
    # TECHS
    assert extract("Joomla") == ["Joomla"]
    assert extract("modx") == ["MODx"]
    # LANGUAGES
    assert extract("objective-c") == ["Objective-C"]
    assert extract("foo") == []
    # TOPICS
    assert extract("computer") == ["Computers"]
    assert extract("Science") == ["Science"]
    assert extract("computer science") == ["Computer-Science"]
    assert extract("foo") == []
    # COMPANIES
    assert extract("Apple") == ["Apple"]
    # CERTIFICATES
    assert extract("CompTIA-A+") == ["CompTIA-A+"]

  def test_extract_many_smoke(self, extract_many) -> None:
    assert extract_many(["Joomla", "objective-c", "foo"]) == [
      ["Joomla"],
      ["Objective-C"],
      [],
    ]
    assert extract_many(["Science", "computer science"]) == [
      ["Science"],
      ["Computer-Science"],
    ]

  # KNOWN ISSUES
  def test_known_issues1(self, extractset):
    assert extractset("""
      LDM ball cube ball big cube ball next Rest In Peace niflheim vismuth slow wave fast robot keep going!
      slow, ship, go! slow ball Auto? fast dual ufo
    """) == {"Go"}

  # ADHOC
  def test_extract_adhoc1(self, extractset) -> None:
    assert extractset("computer") == {"Computers"}
    assert extractset("data") == {"Data"}
    assert extractset("my user data") == set()
    assert extractset("data science") == {"Data-Science"}
    assert extractset("computer science") == {"Computer-Science"}
    assert extractset("computer and data science") == {"Computer-Science", "Data-Science"}
    assert extractset("data & computer science") == {"Computer-Science", "Data-Science"}
    assert extractset("data, computer science") == {"Computer-Science", "Data"}
    # ^ Spacy bug
    assert extractset("science of data") == {"Data-Science"}
    assert extractset("art and science of data") == {"Art", "Data-Science"}
    # assert extractset("science and art of data") == {"Art", "Data-Science"} -- "art of data" wins over, either retrain or remove
    assert extractset("comp-sci") == {"Computer-Science"}
    assert extractset("Computer-Science") == {"Computer-Science"}
    assert extractset("Computer/Data Science") == {"Data-Science", "Computer-Science"}
    assert extractset("Data/Computer Science") == {"Data-Science", "Computer-Science"}
    assert extractset("computer scientist") == {"Computer-Science"}
    assert extractset("dataScience") == {"Data-Science"}
    assert extractset("data-scientist") == {"Data-Science"}

  def test_extract_adhoc2(self, extractset) -> None:
    assert extractset("programming") == {"Software"}
    assert extractset("computer programming") == {"Computers", "Software"}
    assert extractset("web programming") == {"Web", "Software"}
    assert extractset("php programming") == {"PHP", "Software"}
    assert extractset("programming with PHP") == {"Software", "PHP"}
    assert extractset("just programming on computers") == {"Software", "Computers"}

  def test_extract_adhoc3(self, extractset) -> None:
    assert extractset("software engineering") == {"Software", "Engineering"}
    assert extractset("software and hardware engineering") == {"Software", "Hardware", "Engineering"}
    assert extractset("engineer of software") == {"Engineering", "Software"}
    assert extractset("mobile engineer") == {"Mobile", "Engineering"}
    assert extractset("game engineering") == {"Games", "Engineering"}

  def test_extract_adhoc4(self, extractset) -> None:
    assert extractset("fullstack qa") == {"Backend", "Frontend", "QA"}
    # TODO more about QA

  def test_extract_adhoc5(self, extractset) -> None:
    assert extractset("Development") == {"Engineering"}
    assert extractset("Laravel Development") == {"Laravel", "Engineering"}
    assert extractset("PHP Development") == {"PHP", "Engineering"}
    assert extractset("PHP Tester") == {"PHP", "Testing"}
    assert extractset("Backend Development") == {"Backend", "Engineering"}
    assert extractset("Web (PHP) Development") == {"Web", "PHP", "Engineering"}
    assert extractset("Web and PHP programming") == {"Web", "PHP", "Software"}
    assert extractset("Web (PHP) Development. Some engineering") == {"Web", "PHP", "Engineering"}

  def test_extract_adhoc6(self, extractset) -> None:
    assert extractset("Mobile design and engineering") == {"Mobile", "Engineering"}
    assert extractset("Web engineering & design") == {"Web", "Engineering", "Design"}
    assert extractset("Game design/dev") == {"Games", "Design", "Engineering"}
    assert extractset("Game dev/design") == {"Games", "Design", "Engineering"}
    assert extractset("Game development/design") == {"Games", "Design", "Engineering"}
    assert extractset("Game design/dev") == {"Games", "Design", "Engineering"}
    assert extractset("Game design/development") == {"Games", "Design", "Engineering"}
    assert extractset("Design/dev of games") == {"Games", "Engineering"} # FN "Design"
    assert extractset("Dev/design of games") == {"Games", "Design", "Engineering"}

  def test_extract_adhoc7(self, extractset) -> None:
    assert extractset("analysis + analytics") == {"Analysis"}
    assert extractset("data and business analyst") == {"Data", "Business", "Analysis"}
    assert extractset("business/data analytics") == {"Business", "Data", "Analysis"}
    assert extractset("analytics for any business") == {"Analysis", "Business"}
    assert extractset("analizing data for a small business") == {"Data", "Business"} # "analyzing" is not a term for now

  def test_extract_adhoc8(self, extractset) -> None:
    assert extractset("devops") == {"Engineering", "Operations"}
    assert extractset("data-ops") == {"Data", "Operations"}
    assert extractset("data-ops") == {"Data", "Operations"}
    assert extractset("ml and data ops") == {"Machine-Learning", "Data", "Operations"}
    assert extractset("dev-sec-ops") == {"Engineering", "Security", "Operations"}
    assert extractset("dev/sec ops") == {"Engineering", "Security", "Operations"}
    assert extractset("1 sec to finish") == set()

  def test_extract_adhoc9(self, extractset) -> None:
    assert extractset("Websec") == {"Web", "Security"}
    assert extractset("Websecurity") == {"Web", "Security"}
    assert extractset("Web security") == {"Web", "Security"}
    assert extractset("Web & Network security") == {"Web", "Networks", "Security"}

  def test_extract_adhoc10(self, extractset) -> None:
    assert extractset("Kafka and Pig all the way") == {"Apache-Kafka", "Apache-Pig"}
    assert extractset("Guinea Pig loves Science.") == {"Science"}
    assert extractset("Guinea Pig loves Science. Hadoop!") == {"Science", "Apache-Hadoop"}
    assert extractset("Apache Guinea Pig loves Science.") == {"Apache", "Apache-Pig", "Science"}
    assert extractset("My name is Jax") == set()
    assert extractset("Jax, TensorFlow") == {"JAX", "TensorFlow"}
    assert extractset("Jax vs TensorFlow") == {"JAX", "TensorFlow"}

  def test_extract_adhoc11(self, extractset) -> None:
    assert extractset("I learn v.") == set() # v. is a special case in Spacy, like v.1 for version...
    assert extractset("I learn v lang") == {"V"}
    assert extractset("I learn v-lang") == {"V"}
    assert extractset("I learn v-language") == {"V"}
    assert extractset("I learn v-stuff") == set()
    assert extractset("V-JEPA") == set()
    assert extractset("I learn c lang") == {"C"}
    assert extractset("I learn stuff-c") == set()
    assert extractset("C. Objective-C. C++") == {"C", "Objective-C", "C++"}
    assert extractset("Ph.D. candidate, interested in software security") == {"Software", "Security"}

  def test_extract_adhoc12(self, extractset) -> None:
    assert extractset("Graphic Designer") == {"Graphics", "Design"}
    assert extractset("visual design") == {"Design"}

  def test_extract_adhoc13(self, extractset) -> None:
    assert extractset("system administration") == {"Systems", "Administration"}
    assert extractset("database administration") == {"Databases", "Administration"}
    assert extractset("senior dba") == {"Databases", "Administration"}

  def test_extract_adhoc14(self, extractset) -> None:
    assert extractset("automated test") == {"Automation", "Testing"}
    assert extractset("automated testing") == {"Automation", "Testing"}
    assert extractset("automated qa") == {"Automation", "QA"}
    assert extractset("test automation") == {"Testing", "Automation"}
    assert extractset("qa & automation") == {"QA", "Automation"}
    assert extractset("qa & testing") == {"QA", "Testing"}
    assert extractset("qa & automation testing") == {"QA", "Automation", "Testing"}
    assert extractset("tester and qa") == {"Testing", "QA"}
    assert extractset("automated tester and qa") == {"Automation", "Testing", "QA"}

  def test_extract_adhoc15(self, extractset) -> None:
    assert extractset("be lit") == set()
    assert extractset("#lit #react #go") == {"Lit", "React", "Go"}
    assert extractset("using Lit for fun and profit") == {"Lit"}
    assert extractset("react") == {"React"}
    assert extractset("go.") == {"Go"}

  def test_extract_adhoc16(self, extractset) -> None:
    assert extractset("AWS-VPC") == {"AWS-VPC"}
    assert extractset("AWS something something VPC") == {"AWS", "AWS-VPC"}

  # BIOS
  def test_extract_bios1(self, extractset) -> None:
    assert extractset("Self-employed web engineer. #Rust #Wasm #Go #TypeScript #React #REST") == {
      "Web", "Engineering", "Rust", "WebAssembly", "Go", "TypeScript", "React", "REST"
    }
    assert extractset("I like Postgres, Kubernetes, Docker, DevOps.") == {
      "PostgreSQL", "Kubernetes", "Docker", "Engineering", "Operations"
    }
    assert extractset("working with React, Node, Go, and the rest") == {
      "React", "NodeJS", "Go"
    }

  def test_extract_bios2(self, extractset) -> None:
    assert extractset("Po of Open棟梁 Pj / PMP / .NET, .NET Core ≫ OAuth / OIDC, FAPI, FIDO, SAML") == {
      ".NET", "OAuth", "SAML"
    }
    assert extractset("≫ IdMaaS, mBaaS / JavaScript ≫ Frontend, IoT Edge. 静岡 → 新潟 → 東京 → 広島") == {
      "BaaS", "JavaScript", "Frontend", "IoT"
    }
    assert extractset("Node.js, Angular, React.js, PHP, Apollo Data Graph, OpenAPI, More...") == {
      "NodeJS", "Angular", "React", "PHP", "Apollo", "OpenAPI"
    }
    assert extractset("With no desire，at rest and still. All things go right as of their will") == set()

  def test_extract_bios3(self, extractset) -> None:
    assert extractset("Fullstack web developer with focus on front end services.") == {
      "Backend", "Frontend", "Web", "Engineering"
    }
    assert extractset("Experienced with React/React Native, PHP, MySQL, GraphQL, Angularjs, Prisma, Expo") == {
      "React", "React-Native", "PHP", "MySQL", "GraphQL", "Angular", "Prisma"
    }
    assert extractset("developer with expertise in ASP.Net (Legacy, Core), Angular, Ionic, NativeScript") == {
      "Engineering", "ASP.NET", "Angular", "Ionic", "Native-Script"
    }
    assert extractset("#Python #Jupyter #pandas #docker") == {
      "Python", "Jupyter", "Pandas", "Docker"
    }
    assert extractset("""
      I have no idea how far I can go, but I`m sure I don`t like to stay here for the rest of my life
    """) == set()

  def test_extract_bios4(self, extractset) -> None:
    assert extractset("Web & Blockchain Developer 🎨React(Next), Vue(Nuxt), 🎄Laravel") == {
      "Web", "Blockchains", "Engineering", "React", "NextJS", "VueJS", "NuxtJS", "Laravel"
    }
    assert extractset("NumPy, SciPy, Numba, Conda, PyData, NumFocus, Anaconda, Quansight, OpenTeams") == {
      "NumPy", "SciPy", "Numba", "Anaconda"
    }
    assert extractset("✐Python ✎Jupyter Notebook, Flutter 🎈Smart Contract(Solidity)=") == {
      "Python", "Jupyter", "Flutter", "Smart-Contracts", "Solidity"
    }
    assert extractset("Debugger debugger at WebStorm JetBrains MSE student at ITMO University") == {"Debugging"}

  def test_extract_bios5(self, extractset) -> None:
    assert extractset("Software Engineer, Tech Lead in Rust, WASM, TypeScript") == {
      "Software", "Engineering", "Leadership", "Rust", "WebAssembly", "TypeScript",
    }
    assert extractset("React | Node JS | REST") == {
      "NodeJS", "REST", # "React",
    }
    assert extractset("REST | MEAN Stack developer") == {
      "REST", "MongoDB", "Express", "Angular", "NodeJS", "Engineering"
    }
    assert extractset("Senior Backend Developer (.NET) at Dow Jones") == {
      "Backend", "Engineering", ".NET",
    }
    assert extractset("cosmologist | @conda-forge core | @conda steering (emeritus)") == set()
    assert extractset("Ce qui mérite d'être") == set()

  def test_extract_bios6(self, extractset) -> None:
    assert extractset("Go/Python/Java, Web/K8S") == {
      "Go", "Python", "Java", "Web", "Kubernetes"
    }
    assert extractset("NIT Robocon Member 🥰 Arduino / OpenSiv3D / Qt / WindowsAPI / C / C++ / Roblox") == {
      "Robotics", "Arduino", "Qt", "C", "C++", "Roblox"
    }
    assert extractset("Community-supported HTML5 CSS3 platform extension for Unreal Engine 4") == {
      "HTML", "CSS", "Unreal-Engine"
    }
    assert extractset("@jupyter | @jupyterhub | @ipython | @jupyter-incubator") == set()
    assert extractset("@jupyter-resources | @jupytercalpoly | @jupyter-attic") == set()

  def test_extract_bios7(self, extractset) -> None:
    assert extractset("Ruby/Rails JavaScript Ember.js Clojure Node.js") == {
      "Ruby", "Ruby-on-Rails", "JavaScript", "EmberJS", "Clojure", "NodeJS"
    }
    assert extractset("Ethereum | Flutter | Hyperledger Fabric") == {
      "Ethereum", "Flutter"
    }
    assert extractset("Unity, ECS EC2, Node.JS Android") == {
      "Unity", "AWS-ECS", "AWS-EC2", "NodeJS", "Android"
    }
    assert extractset("Dev & Speaker • Microsoft MVP Azure, .NET, Blazor 🥔 Couch potato") == {
      "Engineering", "Microsoft", "Microsoft-Azure", ".NET", "Blazor"
    }
    assert extractset("far better rest I go to than I have ever known") == set()

  def test_extract_bios8(self, extractset) -> None:
    assert extractset("Engineer on Azure-AWS, Kubernetes AKS-EKS-GKE") == {
      "Engineering", "Microsoft-Azure", "AWS", "Kubernetes",
      "Azure-Kubernetes", "AWS-EKS", "Google-Kubernetes"
    }
    assert extractset("Terraform, Golang, Ansible, HashiCorp Vault") == {
      "Terraform", "Go", "Ansible", "HashiCorp", "Vault"
    }
    assert extractset("Angular || React (NextJs) || Svelte kit || Node || Nest || PHP5 || Couch CMS") == {
      "Angular", "React", "NextJS", "SvelteKit", "NodeJS", "NestJS", "PHP", "CMS"
    }
    assert extractset("Full-stack developer Vue, Nuxt, Wordpress+GraphQL") == {
      "Backend", "Frontend", "Engineering", "VueJS", "NuxtJS", "WordPress", "GraphQL"
    }
    assert extractset("I'm learning #go and #rest") == {"Go", "REST"}
    assert extractset("I'm learning the rest as I go on") == set()
    assert extractset("Where projects go to rest") == set()

  def test_extract_bios9(self, extractset) -> None:
    assert extractset("""
      FULL STACK JAVA | NETBEANS | C# | MICROSOFT MANAGEMENT STUDIO | VISUAL CODE | JUPYTER NOTEBOOK | PYTHON & RUBY
    """) == {
      "Backend", "Frontend", "Java", "C#", "MS-SQLServer", "Jupyter", "Python", "Ruby"
    }
    assert extractset("Learning ReactJS & Next.js to become a proficient frontender") == {
      "React", "NextJS", "Frontend"
    }
    assert extractset("Power BI, my-sql-manager, Dotnet, Django/Python") == {
      "Power-BI", "MySQL", ".NET", "Django", "Python"
    }
    assert extractset("The java.lang.Math") == {"Mathematics"} # FP, we can't differentiate non-code module names from text :(
    assert extractset("hey are a bi person, my@sql") == set()
    assert extractset("PHP phper, Python pythonista") == {"PHP", "Python"}
    assert extractset("Where old projects go to live out the rest of their days") == set()

  def test_extract_bios10(self, extractset) -> None:
    assert extractset("I'm Julia, a marketing manager") == {"Marketing", "Management"}
    assert extractset("I learn Julia language") == {"Julia"}
    assert extractset("developer:iOS,Robot,Fintech") == {"Engineering", "iOS", "Finance"}
    assert extractset("C Plus Plus programmar from India") == {"C++"}
    assert extractset("hey are a bi person, my@sql") == set()
    assert extractset("PHP phper, Python pythonista") == {"PHP", "Python"}
    assert extractset("Where old projects go to live out the rest of their days") == set()

  def test_extract_bios11(self, extractset) -> None:
    assert extractset("Keen user of d3.js, and Raspberry Pi's.") == {"D3JS", "Raspberry-Pi"}
    assert extractset("Arduino addict. Java programmer in real life") == {"Arduino", "Java", "Software"}
    assert extractset("C#,C++,Firebase,Unity") == {"C#", "C++", "Google-Firebase", "Unity"}
    assert extractset("R, Matlab, Tableau") == {"R", "Matlab", "Tableau"}
    assert extractset("Pulumi, Kotlin, PowerShell | Postgres") == {"Pulumi", "Kotlin", "PowerShell", "PostgreSQL"}
    assert extractset("MariaDB for backend | Scss for the FE") == {"MariaDB", "Backend", "SASS", "Frontend"}
    assert extractset("To be or not to BE") == set() # no FP!

  def test_extract_bios12(self, extractset) -> None:
    assert extractset("ARM processors") == {"ARM", "CPU"}
    assert extractset("Hi, my name is Arm") == set()
    assert extractset("My left arm is stronger than my right arm") == set()
    assert extractset("I’m doing high-performance computing work on CPU, including x86, arm.") == {
      "Performance", "Computers", "CPU", "x86", "ARM"
    }
    assert extractset("Embrace AI-IoT | RISC-V | ARM | ARC") == {"AI", "IoT", "RISC", "ARM", "ARC"}
    assert extractset("PERN afficianado") == {"PostgreSQL", "Express", "React", "NodeJS"}

  def test_extract_bios13(self, extractset) -> None:
     assert extractset("My favorite language is Jax") == set()
     assert extractset("My name is Jax") == set()
     assert extractset("Hi, I'm Jax, an avid computer sorcerer") == {"Computers"}
     assert extractset("CUDA C++ , Pytorch RT, JAX(JIT,Haiku enjoyer, FLAX Flexer)") == {"CUDA", "C++", "PyTorch", "JAX", "Flax"}
     assert extractset("JAX @NVIDIA") == {"JAX", "NVidia"}
     assert extractset("Scientist @ JAX") == {"Science", "JAX"}
     assert extractset("I like learning | JAX | Google Brain") == {"JAX", "Google"}
     assert extractset("Software Engineer at Google DeepMind working on JAX/Flax") == {
       "Software", "Engineering", "Google", "JAX", "Flax"
     }
     assert extractset("Jax + Haiku fan. Self-attention for the win") == {"JAX"}
     assert extractset("Julia, GraalVM, LLVM, NVidia, CNCF, Program Synthesis, 3D-QSAR") == {"Julia", "LLVM", "NVidia"}
     assert extractset("Sample for UE5's CommonConversation Feature") == {"Unreal-Engine"}

  def test_extract_bios14(self, extractset) -> None:
    assert extractset("Android(Kotlin) | iOS(Swift) | Spring Boot(Java) | Python(Django)") == {
      "Android", "Kotlin", "iOS", "Swift", "Spring", "Java", "Python", "Django"
    }
    assert extractset("ClickHouse, linux, perl, python, C++, kafka") == {
      "ClickHouse", "Linux", "Perl", "Python", "C++", "Apache-Kafka"
    }
    assert extractset("Software Eng @ClickHouse") == {"Software", "Engineering"}
    assert extractset("Love making games") == {"Games"}
    # I'm a 21 year old embedded systems electronics engineer.
    assert extractset("""
      Mostly interested in robotics, low-level coding and homebrew.
    """) == {"Robotics", "Software"}
    assert extractset("""
      Programmer, cybersecurity expert, and 2017 penetration tester
    """) == {"Software", "Cyber-Security", "VA/PT"}

  def test_extract_bios15(self, extractset) -> None:
    assert extractset("Blockchain developer, bulding for DeFi.") == {"Blockchains", "Engineering", "DeFi"}
    assert extractset("""
      FullStack Web Developer | Penetration Tester
    """) == {"Backend", "Frontend", "Web", "Engineering", "VA/PT"}
    assert extractset("""
      Student in saylani mass it training program and learn web and app
      development and I'm completed my content management system WordPress course.
    """) == {"Web", "Engineering", "CMS", "WordPress"}

  def test_extract_bios16(self, extractset) -> None:
    assert extractset("NVIDIA Technologies for game and application developers") == {"NVidia", "Games"}
    assert extractset("Open source continuous integration for games") == {"Open-Source", "CI/CD", "Games"}
    assert extractset("Game developer.") == {"Games", "Engineering"}
    assert extractset("Game Server Programmer :)") == {"Games", "Client-Server", "Software"}
    assert extractset("I'm a JS / TS specialist focused on web and game development.") == {
      "JavaScript", "TypeScript", "Web", "Games", "Engineering"
    }
    assert extractset("Game-related tidbits + bytes found on GitHub") == {"Games", "GitHub"}
    assert extractset("Working on a Game Engine") == {"Games"}
    assert extractset("Game Security & Realtime Rendering") == {"Games", "Security"}
    assert extractset("game of game") == {"Games"}
    assert extractset("Like world and game") == {"Games"}
    assert extractset("Father, hacker, blogger, gamer, & nerd. Bounty Hunter") == {"Games"} # "Hacking"

  def test_extract_bios17(self, extractset) -> None:
    assert extractset("3D game engine development amateur") == {"Games", "Engineering"}
    assert extractset("Deep Learning Student | Game Dev") == {"Deep-Learning", "Games", "Engineering"}
    assert extractset("Game Hacking") == {"Games"} # , "Hacking"
    assert extractset("ex-game developer") == {"Games", "Engineering"}
    assert extractset("Like world and game") == {"Games"}
    assert extractset("Gaming the game is Gabe's game.") == {"Games"}
    assert extractset("Computational Game Theory Research") == {"Research"}

  def test_extract_bios18(self, extractset) -> None:
    assert extractset("CS-sophomore | Game-dev (Unity & C#)") == {"Computer-Science", "Games", "Engineering", "Unity", "C#"}
    assert extractset("Game assets, software and games") == {"Games", "Software"}
    assert extractset("JavaScript, the BEST game") == {"JavaScript", "Games"}
    assert extractset("I'm a Professional C++ Game and Software Developer from New York.") == {
      "C++", "Games", "Software", "Engineering"
    }
    assert extractset("Gamedev and shite") == {"Games", "Engineering"}
    assert extractset("The Game") == {"Games"}

  def test_extract_bios19(self, extractset) -> None:
    assert extractset("I love to research malware, viruses, and other types of malicious files.") == {
      "Research", "Cyber-Security"
    }
    assert extractset("CS PhD student at Stony Brook University, new to Distributed System.") == {
      "Computer-Science", "Distributed", "Systems"
    }
    assert extractset("Building Distributed SQL Database") == {
      "Distributed", "SQL", "Databases"
    }
    assert extractset("Computer science student with an interest in data science.") == {
      "Computer-Science", "Data-Science"
    }
    # ^ Spacy parsing bug
    assert extractset("""
      Dive into the world of sophistication with U-Glam NYC,
      your quintessential destination for luxury jewelry, headbands, and pearls.
      Based in the heart of New York.
    """) == set()
    assert extractset("Salesforce Guru") == {"SalesForce"}
    assert extractset("Aspiring Machine Learning / Data Engineer") == {
      "Machine-Learning", "Data", "Engineering"
    }
    assert extractset("Healthcare data analyst freelancer") == {
      "Healthcare", "Data", "Analysis" # "Health",
    }
    assert extractset("looking to help clients use their data to the fullest.") == set()

  def test_extract_bios20(self, extractset) -> None:
    assert extractset("data-backed decision making: statistical analysis, Computational Fluid Dynamics") == {
      "Data", "Statistics", "Analysis"
    }
    assert extractset("Campaign Lead, Data Scientist, Statistician") == {
      "Leadership", "Data-Science", "Statistics"
    }
    assert extractset("Website Developer and Software Developer with a Bachelor of Science in Informatics.") == {
      "Web", "Engineering", "Software", "Science", "Informatics"
    }
    assert extractset("a Microsoft Technical Trainer specializing in Data & AI") == {
      "Microsoft", "Data", "AI"
    }
    assert extractset("SQL Server/Cloud DBA") == {
      "MS-SQLServer", "Cloud", "Databases", "Administration"
    }

  def test_extract_bios21(self, extractset) -> None:
    assert extractset("I love making games with Godot") == {"Games", "Godot"}
    assert extractset("""
      Experience with infrastructure as code (IaC) tools like Terraform, Ansible,
      or Azure Resource Manager (ARM) templates.
    """) == {
      "ARM", "IAC", "Terraform", "Ansible", "Microsoft-Azure"
    }
    assert extractset("""
      Developing software 50 years from Business&Scientific (Fortran IV, COBOL),
      to desktop (PowerBuilder, Visual Basic), Web Cloud, to Mixed Reality (Unity/C#)
    """) == {
      "Software", "Business", "Science", "Fortran", "Cobol",
      "Desktop", "Visual-Basic", "Web", "Cloud", "AR/VR", "Unity", "C#"
    }
    assert extractset("""
      React.js/Next.js/Vue.js/Nuxt.js/Nest.js/Express.js/flutter/react-native
    """) == {
      "React", "NextJS", "VueJS", "NuxtJS", "NestJS",
      "Express", "Flutter", "React-Native"
    }

  # SLUGS
  def test_extract_slug1(self, extractset) -> None:
    assert extractset("chartjs-chart-matrix") == {"ChartJS"}
    assert extractset("""
      Chart.js module for creating matrix charts
    """) == {"ChartJS"}

  def test_extract_slug2(self, extractset) -> None:
    assert extractset("supertokens-core") == set()
    assert extractset("""
      Open source alternative to Auth0 / Firebase Auth / AWS Cognito
      #authentication
      #session-management
      #login
      #supertokens
      #java
      #signin
      #password
      #social-login
      #email-password
      #email-password-login
      #auth0
      #keycloak
      #firebase-auth
      #aws-cognito
      #passwordless
      #passwordless-authentication
      #passwordless-login
      #oauth
      #hacktoberfest
    """) == {"Open-Source", "Auth0", "Google-Firebase", "Authentication", "AWS-Cognito", "Java", "OAuth"}
