from ...xpatterns import IN, LOWER, OP, propn, ver1
from ..tag import Skill, Tech
from ..utils import dis_incontext, dis_namelike, dis_nounlike, dis_precisely, dis_verblike
from .ai import SKILLS as AI_SKILLS
from .adobe import SKILLS as ADOBE_SKILLS
from .amazon import SKILLS as AMAZON_SKILLS
from .apache import SKILLS as APACHE_SKILLS
from .apple import SKILLS as APPLE_SKILLS
from .cisco import SKILLS as CISCO_SKILLS
from .google import SKILLS as GOOGLE_SKILLS
from .hashicorp import SKILLS as HASHICORP_SKILLS
from .meta import SKILLS as META_SKILLS
from .microsoft import SKILLS as MICROSOFT_SKILLS
from .yandex import SKILLS as YANDEX_SKILLS
# ...
from .certificates import SKILLS as CERTIFICATES_SKILLS
from .companies import SKILLS as COMPANIES_SKILLS
from .industries import SKILLS as INDUSTRIES_SKILLS
from .topics import SKILLS as TOPICS_SKILLS
from .languages import SKILLS as LANGUAGE_SKILLS

SKILLS: list[Skill] = [
  *AI_SKILLS,
  *ADOBE_SKILLS,
  *AMAZON_SKILLS,
  *APACHE_SKILLS,
  *APPLE_SKILLS,
  *CISCO_SKILLS,
  *GOOGLE_SKILLS,
  *HASHICORP_SKILLS,
  *META_SKILLS,
  *MICROSOFT_SKILLS,
  *YANDEX_SKILLS,
  # ...
  *CERTIFICATES_SKILLS,
  *COMPANIES_SKILLS,
  *INDUSTRIES_SKILLS,
  *TOPICS_SKILLS,
  *LANGUAGE_SKILLS,

  # ANALYSIS
  Tech("Tableau", ["tableau"]),

  # CLOUD
  Tech("Cloudflare", ["cloudflare"]),
  Tech("Heroku", ["heroku"]),
  Tech("Netlify", ["netlify"]),

  # TOOLS (should mostly be discouraged in UI)
  Tech("Confluence", ["confluence"]), # FP, exclude "confluence of" pattern
  Tech("GitHub", ["github"]),
  Tech("GitLab", ["gitlab"]),
  Tech("Jira", ["jira"]),
  Tech("Postman", ["postman"]),
  Tech("Swagger", ["swagger"]),

  # MOBILE & CROSS-PLATFORM
  # notification, ui, gui, interface, native, web
  # Bluetooth, TCP, USB
  Tech("Android", ["android"]),
  Tech("CMake", ["cmake"]),
  Tech("Cocoa", ["cocoa"]),
  Tech("Cordova", ["cordova", "phonegap"]),
  Tech("Dagger2", ["dagger=2"], "Programmable CI/CD engine that runs pipelines in containers"),
  Tech("GTK", ["gtk", "gtk+"]),
  Tech("Ionic", ["ionic"]),
  Tech("Capacitor", ["capacitor"]),
  Tech("Jetpack-Compose", ["jetpack=compose", "jetpack=navigation", "android=compose"]), # just Jetpack is ambiguous

  Tech("Lottie", ["lottie"]),
  Tech("Onsen UI", ["onsen", "onsen=ui"]),
  Tech("Native-Script", ["native=script"]),
  Tech("Novu", ["novu"]), # open-source notification platform, framework, CMS https://github.com/novuhq/novu
  Tech("QML", ["qml"]), # Qt modeling language
  Tech("Qt", ["pyqt", "pyside", "qtruby", "qtjambi", "php=qt", ver1("qt")]),
  Tech("React-Native", ["react=native"]),
  Tech("Retrofit", ["retrofit"]),
  Tech("SDL", ["sdl"]),
  Tech("SFML", ["sfml"]),
  Tech("Xcode", ["xcode"]),
  # Titanium -- disambiguate
  Tech("VoIP", ["voip"]), # voice over IP
  Tech("Vue-Native", ["vue=native"]),
  Tech("WebRTC", ["webrtc"]), # web real-time communication

  # DATABASE, DWH
  Tech("CouchBase", ["couchbase"]),
  Tech("CouchDB", ["couch=db"]),
  Tech("Elasticsearch", ["elastic=search"]),
  Tech("Greenplum", ["greenplum"]),
  Tech("MariaDB", ["maria=db"]),
  Tech("Memcached", ["memcache(d)"]),
  Tech("MongoDB", ["mongo=db", ver1("mongo")]),
  Tech("MySQL", ["my-sql", "my sql", ver1("mysql"), "(my=)sql=manager"]),
  Tech("Neo4j", ["neo4j", "neo4j=db"]),
  Tech("Opensearch", ["opensearch"], "Community-driven Elasticsearch fork"),
  Tech("Oracle", ["oracle=db", "oracle", "pl(/)sql"]), # Oracle Database or Oracle RDBMS TODO split DB and COMPANY
  Tech("PouchDB", ["pouch=db"]),
  Tech("Presto", ["presto"]),
  Tech("PostgreSQL", [
    "postgre=sql", "postgres=sql", ver1("postgres"),
    "pgadmin",
    "psql", "pgsql"
  ]),
  Tech("Redis", ["redis"]),
  Tech("ScyllaDB", ["scylladb"]),
  Tech("Supabase", ["supabase"]),
  Tech("SQLite", [ver1("sqlite")]),
  Tech("Trino", ["trino"]), # also ANALYTICS (https://trino.io/ Fast distributed SQL query engine for big data analytics)
  # orms
  Tech("Django-ORM", ["django=orm"]),
  Tech("Drizzle", ["drizzle=orm", "drizzle"]),
  Tech("Hibernate", ["hibernate"]),
  Tech("Prisma", ["prisma=orm", "prisma"]), # Popular word, some FPs
  Tech("Sequelize", ["sequelize"]),
  Tech("SQLAlchemy", ["sql=alchemy"]),
  Tech("TypeORM", ["type=orm"]),

  # DATA SCIENCE
  Tech("Anaconda", ["anaconda", "miniconda", "conda"]),
  Tech("Beautiful-Soup", ["beautiful=soup"]),
  Tech("IPython", ["ipython"]), # interactive shell
  Tech("Jupyter", ["jupyter=lab", "jupyter-notebook(s)", "jupyter"]),
  Tech("Matplotlib", ["matplotlib"]),
  Tech("NLTK", ["nltk"]),
  Tech("Numba", [[{LOWER: "numba"}, {OP: "!", LOWER: {IN: ["1", "one", "wan"]}}]]),
  Tech("NumPy", ["numpy"]),
  Tech("Pandas", ["pandas"]),
  Tech("PyTorch", ["pytorch"]),
  Tech("Keras", ["keras"]),
  Tech("RAPIDS", [propn("rapids")]), # also GAMES (`https://rapids.ai/`)
  Tech("Scikit-Learn", ["scikit=learn", "sklearn"]),
  Tech("SciPy", ["scipy"]),
  Tech("Seaborn", ["seaborn"]),
  Tech("ShowFlake", ["snowflake"]), # ~ MS Databricks, ~ AWS Redshift
  Tech("Spacy", ["spacy"]),
  Tech("Stan", ["stan"], disambiguate=[
    dis_incontext("r", "python"),
    dis_namelike(),
  ]),
  Tech("Stata", ["stata"]),
  Tech("TensorRT", ["tensorrt"]), # NVidia

  # GAME
  Tech("BabylonJS", ["babylon.=js"], "Game and rendering engine packed into a JavaScript framework"),
  Tech("CUDA", ["cuda"]), # also ROBOTICS, EMBEDDED (GPU computing, NVIDIA)
  Tech("Godot", ["godot=engine", "godot", "gd=script"]),
  Tech("Phaser", ["phaser.=js", "phaser"]),
  Tech("PixiJS", ["pixi.=js", "pixi"]),
  Tech("PlayStation", ["playstation", "ps4", "ps5"]),
  Tech("PyGame", ["pygame"]),
  Tech("Roblox", ["roblox"]),
  Tech("Solar2D", ["solar2d"]),
  Tech("Unreal-Engine", ["unreal=engine", "unreal=script", "unreal", "ue-4", "ue-5", "ue4", "ue5"]),
  Tech("ThreeJS", ["three.=js"]),

  Tech("OpenGL", ["opengl"]),

  # WEB BACKEND
  Tech("Auth0", ["auth0"]), # also SECURITY
  Tech("Bun", ["bun"]),
  Tech("CakePHP", ["cake=php"]),
  Tech("CherryPy", ["cherry=py"]),
  Tech("CodeIgniter", ["code=igniter"]),
  Tech("Deno", ["deno"]),
  Tech("Django", ["django", "drf"]), # django-rest-framework
  Tech("Express", ["express.=js", "express"]),
  Tech("FastAPI", ["fast=api"]),
  Tech("Fastify", ["fastify"]),
  Tech("Flask", ["flask"]),
  Tech("Jakarta-EE", ["jakarta(=ee)", "java-ee", "j2ee", "java-platform"]),
  Tech("JVM", ["jvm"], "Java Virtual Machine enables a computer to run Java (Kotlin, etc.) programs"),
  Tech("Hasura", ["hasura"]),
  Tech("Koa", ["koa"]),
  Tech("Laravel", ["laravel"]),
  Tech("NestJS", ["nest.=js", propn("nest")]),
  Tech("Nginx", ["nginx"]),
  Tech("Phoenix", ["phoenix"]),
  Tech("Ruby-on-Rails", ["ruby-on-rails", "rails", "ror"]),
  Tech("SailsJS", ["sails.=js"]),
  Tech("Spring", [
    ver1("spring"), "spring-framework", "spring-boot", "spring-cloud",
    "spring-mvc", "spring-security", "spring-webflux"
  ]),
  Tech("Symfony", [ver1("symfony")]),
  Tech("Yii", [ver1("yii")]),

# #   Key Components of J2EE:
# #
# # Java Servlets: Server-side Java programs that handle requests and responses, enabling dynamic web content generation.
# # JavaServer Pages (JSP): A technology that allows for the creation of dynamic web pages using HTML and Java code.
# # Enterprise JavaBeans (EJB): A server-side component architecture that allows for the development of scalable, transactional, and multi-user applications.
# # Java Message Service (JMS): A messaging standard that allows applications to communicate asynchronously.
# # Java Naming and Directory Interface (JNDI): An API that provides naming and directory functionality to applications, allowing them to look up resources like databases and EJBs.
# # Java Transaction API (JTA): A specification that allows for the management of transactions across multiple resources.

  Tech("Micronaut", ["micronaut"]),
  Tech("RabbitMQ", ["rabbit=mq", "rmq"]),
  Tech("Vert-X", ["vert.=x"]),

  # WEB FRONTEND
  Tech("Angular", ["angular.=js", "angular"], "Web framework for SPA, mobile, PWA development with focus on modularity"),
  Tech("Astro", ["astro.=js", "astro"], "Web framework for content-driven websites, server-first"),
  Tech("Bootstrap", ["bootstrap"]),
  Tech("Chakra-UI", ["chakra=ui", "chakra"]),
  Tech("ChartJS", ["chart.=js"]),
  Tech("D3JS", ["d3.=js", "d3"]),
  Tech("EmberJS", ["ember.=js", "ember"]),
  Tech("Figma", ["figma"]),
  Tech("Framer", ["framer"]),
  Tech("jQuery", ["jquery"]),
  Tech("Lit", [propn("lit")]),
  Tech("Material-UI", ["material=ui", "mui", propn("material")]),
  Tech("Materialize", ["materialize"]),
  Tech("NgRx", ["ngrx"], "Reactive state management for Angular apps inspired by Redux"),
  Tech("Pinia", ["pinia"]),
  Tech("React", ["react.=js"]),
  Tech("React", ["react"], disambiguate=dis_verblike()),
  Tech("Redux", ["redux.=js", "redux"]),
  Tech("Remix", ["remix.=js", "remix"]),
  Tech("RiotJS", ["riot.=js"]),
  Tech("SolidJS", ["solid.=js", propn("solid")]),
  Tech("Svelte", ["svelte.=js", "svelte"]),
  Tech("Tailwind-CSS", ["tailwind.=css", "tailwind"]),
  Tech("VueJS", ["vue.=js", ver1("vue")]),
  Tech("VueX", ["vuex"], "State management pattern + library for VueJS applications"),

  # WEB FULLSTACK
  Tech("Gulp", ["gulp"]),
  Tech("Vaadin", ["vaadin"]),
  Tech("Vite", ["vite"]),
  Tech("Webpack", ["webpack"]),

  Tech("JAM-Stack", ["jam=stack"], resolve=["JavaScript", "API", "Markup"]),
  Tech("MEAN-Stack", ["mean=stack", propn("mean")], resolve=["MongoDB", "Express", "Angular", "NodeJS"]),
  Tech("MERN-Stack", ["mern=stack", "mern"], resolve=["MongoDB", "Express", "React", "NodeJS"]),
  Tech("MEVN-Stack", ["mevn=stack", "mevn"], resolve=["MongoDB", "Express", "VueJS", "NodeJS"]),
  Tech("PERN-Stack", ["pern=stack", "pern"], resolve=["PostgreSQL", "Express", "React", "NodeJS"]),
  Tech("LAMP-Stack", ["lamp=stack", propn("LAMP")], resolve=["Linux", "MySQL", "PHP"]), # Apache

  Tech("Chrome", ["chrome"]),
  Tech("Firefox", ["firefox"]),
  Tech("Safari", ["safari"]),
  Tech("WebKit", ["webkit"]), # browser engine

  Tech("Apollo", ["apollo.=js", "apollo=client", "apollo=server", "apollo"], "GraphQL-centric fullstack tools for web and mobile"),
  Tech("HTMX", ["htmx"]),
  Tech("Meteor", ["meteor", "meteor.=js"]),
  Tech("Ktor", ["ktor"]), # fullstack framework in Kotlin
  Tech("NextJS", ["next.=js"]),
  Tech("NextJS", ["next"], disambiguate=[
    dis_incontext("framework", "nuxt", "react"),
    dis_nounlike(),
  ]),
  Tech("NuxtJS", ["nuxt.=js", propn("nuxt")]),
  Tech("NodeJS", ["node.=js", propn("node")]),
  Tech("SvelteKit", ["svelte=kit"]),

  # LOW-CODE
  Tech("1C", ["1c"]), # ??
  Tech("Bitrix", [
    "bitrix",
    "1c=bitrix", "bitrix=1c", "1с-битрикс", "битрикс-1с",
    "bitrix=24", "битрикс=24",
  ]), # so rare it makes sense to merge them...
  Tech("Airtable", ["airtable"]),
  Tech("Drupal", ["drupal"]),
  Tech("Gatsby", ["gatsby"]),
  Tech("Hygraph", ["hygraph", "graph=cms"]),
  Tech("Jekyll", ["jekyll"]),
  Tech("Joomla", ["joomla"]),
  Tech("MODx", ["modx"]),
  Tech("Shopify", ["shopify"]),
  Tech("Strapi", ["strapi"]),
  Tech("WebFlow", ["webflow"]),
  Tech("Wix", ["wix"]),
  Tech("WooCommerce", ["woo=commerce"]),
  Tech("WordPress", ["wordpress"]),

  # OPERATIONS
  Tech("Celery", ["celery"]),
  Tech("ELK-Stack", ["elk=stack", "elk"], resolve=["Elasticsearch", "Logstash", "Kibana"]), # , "Beats"
  Tech("Ansible", ["ansible"], "Automation engine for configuration management, application deployment, and task automation"),
  # Tech("Dagger", ["dagger"], "Programmable CI/CD engine that runs pipelines in containers"),
  Tech("CircleCI", ["circleci"]),
  Tech("Docker", ["docker", "dockerfile"]),
  Tech("Docker-Compose", ["docker=compose"]),
  Tech("Docker-Swarm", ["docker=swarm"]),
  Tech("Dokku", ["dokku"]), # also Cloud
  Tech("GitHub-Actions", ["github=actions"]),
  Tech("GitLab-CI", ["gitlab=ci"]),
  Tech("Grafana", ["grafana"], "Monitoring"),
  Tech("Helm", ["helm"]),
  Tech("Jaeger", ["jaeger"], "Distributed tracing platform, CNCF"),
  Tech("Jenkins", ["jenkins"]),
  Tech("Kibana", ["kibana"]),
  Tech("Kubernetes", ["kubernetes", "k8s", "k3s"]),
  Tech("Logstash", ["logstash"]),
  Tech("OpenShift", ["openshift"], "Cloud platform, a set of tools and services for application lifecycle"),
  Tech("Prometheus", ["prometheus"]),
  Tech("Pulumi", ["pulumi"]),
  Tech("Puppet", ["puppet"]),
  Tech("Quarkus", ["quarkus"]),
  Tech("Spinnaker", ["spinnaker"]),
  Tech("Splunk", ["splunk"]), # also SECURITY
  Tech("TeamCity", ["teamcity"]),
  Tech("Vagrant", ["vagrant"]),
  # Good to have Knowledge of modern monitoring solutions (e.g. Nagios, Zabbix, Prometheus, Splunk).
  # Familiarity with monitoring tools such as SolarWinds, Nagios, or similar.

  # QA-n-AUTOMATION (tech & platforms)
  Tech("Appium", ["appium"]),
  Tech("Codeception", ["codeception"]),
  Tech("Cucumber", ["cucumber"]),
  Tech("Cypress", ["cypress", "cypress.=js"]),
  Tech("Jasmine", ["jasmine"], disambiguate=[
    dis_incontext("Jest", "Karma", "QA"),
    dis_namelike(),
  ]),
  Tech("Jest", ["jest"]),
  Tech("JUnit", ["junit"]),
  Tech("Karma", ["karma"], disambiguate=[
    dis_incontext("Jasmine", "Jest", "QA"),
    dis_nounlike(),
  ]),
  Tech("PHPUnit", ["php=unit"]),
  Tech("Playwright", ["playwright"]),
  Tech("Protractor", ["protractor"]),
  Tech("PyTest", ["pytest"]),
  Tech("Selenium", ["selenium"]),
  Tech("Sentry", ["sentry"], "Monitoring"),
  Tech("TestCafe", ["testcafe"]),
  Tech("TestNg", ["testng"]),
  Tech("WebdriverIO", ["webdriverio"]),

  # BLOCKCHAIN
  Tech("Arweave", ["arweave"], "A permanent and decentralized web inside an open ledger"),
  Tech("Bitcoin", ["bitcoin"]),
  Tech("Ethereum", ["ethereum"]),
  Tech("EthersJS", ["eithers.=js"]),
  Tech("EVM", ["evm"], "Ethereum Virtual Machine"),
  Tech("Solana", ["solana"]),
  Tech("Web3JS", ["web3.=js"]),
  # Tech("SVM", ["svm"]), TODO disambiguate Support-Vector-Machine vs Solana-Virtual-Machine

  # MEDIA
  Tech("FFmpeg", ["ffmpeg"], "Cross-platform solution to record, convert and stream audio and video"),

  # NETWORKS
  Tech("F5-Networks", ["f5-networks", "f5"]), # Company
  Tech("LoRa", [propn("LoRa")]), # transmission tech
  Tech("MQTT", ["mqtt"]),      # IoT messaging standard, also CLOUD
  Tech("Netconf", ["netconf"], "Protocol"),
  Tech("Nmap", ["nmap"]),             # also SECURITY
  Tech("Netcat", ["netcat", "ncat"]), # also SECURITY
  Tech("Proxyman", ["proxyman"]),   # also SECURITY
  Tech("Wireshark", ["wireshark"]),   # also SECURITY
  Tech("YANG", ["YANG"], "Data modeling language"),
  Tech("Zigbee", ["zigbee"]), # protocol spec. also EMBEDDED

  # SECURITY
  Tech("Burp-Suite", ["burp=suite"], "Proprietary vulnerability scanning, penetration testing, and webapp security platform"),
  Tech("Cobalt-Strike", ["cobalt=strike"]),
  Tech("JWT", ["jwt"]),
  Tech("Metasploit", ["metasploit"]),
  Tech("Nessus", ["nessus"]),
  Tech("SAML", ["saml"]),
  Tech("Snort", [propn("snort")]),
  # CANVAS, Empire, Core Impact -- attack frameworks

  # ROBOTICS
  # Tech("ABB", ["abb"]),           # robot brand
  Tech("Fanuc", ["fanuc"]),       # robot brand
  Tech("iCub", ["icub"]),         # robot brand
  Tech("HyQ", ["hyq"]),           # robot brand
  Tech("KUKA", ["kuka"]),         # robot brand
  Tech("OpenCV", ["opencv"]),     # open source Computer Vision library
  # Tech("Omron", ["omron"]),       # electronics corporation
  Tech("FreeRTOS", ["freertos"]), # OS, also EMBEDDED-n-SYSTEM
  Tech("ROS", ["ros"]),           # OS, also EMBEDDED-n-SYSTEM
  # Tech("SLAM", ["slam", "vslam"]), # simultaneous localization and mapping
  # Tech("Yaskawa", ["yaskawa"]), # electric and robotics corporation

  Tech("Simulink", ["simulink"]), # some lang.

  # SYSTEM
  Tech("FreeBSD", ["freebsd"]), # also CROSS-PLATFORM
  Tech("Linux", [
    "linux", "debian", "ubuntu",
  ]), # also CROSS-PLATFORM
  Tech("MacOS", ["macos", "osx"]), # also CROSS-PLATFORM
  Tech("Unix", ["unix", "*nix"]),   # also CROSS-PLATFORM
  Tech("Windows", ["windows", "win32", "win64"]), # also CROSS-PLATFORM

  Tech("Clang", ["clang"]),
  Tech("MicroPython", ["micropython"]), # compiler
  Tech("GCC", ["gcc"]), # compiler
  Tech("LLVM", ["llvm"]),

  # HARDWARE & EMBEDDED
  # Tech("HPC", ["hpc"], "High performance computing"),
  Tech("Arduino", ["arduino"], "Controller brand"),
  Tech("ASIC", ["asic"]), # ASICs are custom-designed circuits for specific applications, offering high performance and efficiency
  Tech("ARC", ["arc"], "CPU family", disambiguate=[
    dis_precisely("ARC"),
    dis_incontext("cpu", "arm", "processor(s)"),
    dis_nounlike(),
  ]),
  Tech("AutoCAD", ["autocad"]),
  Tech("AVR", ["avr"], "Controller family"),
  Tech("Elbrus-2000", ["elbrus=2000", "e2k"], "CPU"),
  Tech("Embox", ["embox"]), # Embox is a configurable RTOS designed for resource constrained and embedded systems
  Tech("ESP32", ["esp=32"]), # controller family
  Tech("ESP8266", ["esp=8266"]), # controller family
  Tech("FPGA", ["fpga"]), # FPGAs are reprogrammable devices that provide flexibility and rapid prototyping capabilities
  Tech("i.MX6", ["i.mx=6"]), # platform
  Tech("LabVIEW", ["labview"]),
  Tech("KiCad", ["kicad=eda", "kicad"]),
  Tech("MicroBlaze", ["microblaze"]), # soft core
  Tech("MIPS", ["mips"]), # CPU architecture
  Tech("MSP430", ["msp=430"]), # controller family
  Tech("PowerPC", ["powerpc"]), # CPU architecture
  Tech("Raspberry-Pi", ["raspberry", "rasp=pi", "raspberry=pi(s)", "rpi"]), # platform
  Tech("RISC", ["risc", "risc-v"]), # CPU architecture
  Tech("SPARC", ["sparc"]), # platform
  Tech("Altium-Designer", ["altium=designer"]), # tool
  Tech("Altium-365", ["altium=365"]), # tool
  Tech("Autodesk-Fusion", ["autodesk-fusion", "fusion=360"]), # tool
  Tech("Autodesk-Eagle", ["autodesk-eagle"]), # tool
  Tech("Autodesk-Eagle", ["eagle"], disambiguate=[
    dis_incontext("Autodesk", "AutoCAD"),
    dis_nounlike(),
  ]),
  Tech("Touchdesigner", ["touchdesigner"], "Visual development platform"), #
  Tech("Solidworks", ["solidworks-pcb", "solidworks"], "CB design tool"),
  Tech("STM32", ["stm=32"]), # platform
  Tech("Verilog", ["verilog", "sysverilog", "systemverilog"], "Specialized PL"),
  Tech("VHDL", ["vhdl"], "Specialized PL"),
  Tech("VLIW", ["vliw"], "CPU architecture"),
  Tech("x32", ["x32"], "CPU architecture"),
  Tech("x64", ["x64"], "CPU architecture"),
  Tech("x86", ["x86", "x86-32", "x86-64", "i286", "i386"], "Intel CPU architecture"),
  Tech("Yosys", ["yosys"]), # https://github.com/YosysHQ/yosys
  Tech("Z80", ["z=80"], "CPU brand"),

  # DESKTOP
  Tech("ElectronJS", ["electron=js"]), # tons of FPs for just "electron"

  # UNSORTED
  Tech("Blender", ["blender"]),
  Tech("RxJS", ["rxjs"]),
  Tech("Git", ["git"]),
  Tech("SVN", ["svn"]),
  Tech("gRPC", ["grpc"], "Skill"),
  Tech("tRPC", ["trpc"], "Skill"),
]

# // SECURITY TOOLS
# // Aircrack-ng: 454 repos, 5 users
# // Nikto: 352 repos -- too many false positives
# // John the Ripper: 210 repos, 7 ysers
#
# export const rawSkillTable: Dict<SkillRow> = {
#   "Chef": {pattern: "chef", category: "platform", role: "Engineer"},
#   // should we add new char like "css𝐕" or should we consume numbers after EACH term?
#   "Native Android": {pattern: "native=android", category: "platform", role: "Engineer"},
#   "Native iOS": {pattern: "native-ios", category: "platform", role: "Engineer"},
#   "Octave": {pattern: "octave", category: "lang"},
#   // "Polygon": {pattern: "polygon", category: "tech", role: "Engineer"},
#   "Prisma": {pattern: "prisma", category: "tech", role: "Engineer"},
#   "OpenAuth": {pattern: "open=auth2?, oauth2?", category: "tech"},
#   "RxJS": {pattern: "rx.=js, RX", category: "tech", role: "Engineer"},
#   "Salt": {pattern: "salt", category: "platform", role: "Engineer"},
#   "Web3.js": {pattern: "web3.js", category: "tech"},
#
#   // TOPICS ----------------------------------------------------------------------------------------
#   "Vulnerability": {pattern: "vulnerability, penetration, VA/PT", category: "topic"},
#   "E-commerce": {pattern: "e=commerce", category: "topic"},
#   "Open Source": {pattern: "open=source, fl?oss, f?oss", category: "topic"},
#   "Mathematics": {pattern: "mathematics, maths?", category: "topic"},
#   "CI/CD": {pattern: "ci/=cd", category: "topic"},
#   "Photography": {pattern: "photography", category: "topic"},
#   "2D": {pattern: "2d", category: "topic"},
#   "3D": {pattern: "3d", category: "topic"},
#   // "Font": {pattern: "fonts?", category: "topic"}, // disambiguate?
#   "Animation": {pattern: "animation, motion", category: "topic"},
#   "Enterprise": {pattern: "enterprise", category: "topic"},
#
#   // Role-agnostic (multi-role) topics
#   "Manual": {pattern: "manual", category: "topic"},
#   "R&D": {pattern: "r ?& ?d", category: "topic"},
#   "Sales": {pattern: "sales", category: "topic"}, // another problematic word @_@
#   "Team": {pattern: "!Teams?", category: "topic"},
#   "Functional Programming": {pattern: "functional-programming, fp", category: "topic"},
#   "Crypto": {pattern: "crypto, defi, web=3", category: "topic"}, // crypto enthusiast = crypto-currencies + decentralized finance (DeFi)
#   // Crypto vs Blockchain?!?!
#   // should nopCommerce -> eCommerce? But then NodeJS -> js, are there INVALID precedents like that?
#
#   /*
#   UI/UX specific words
#   menu
#   button
#   mouse
#   keyboard (can be WEB or CLI)
#   screen
#   scroll, scrollbar
#   form (?)
#   theme
#   animation
#
#   FRONTEND specific words
#   image, img, gif, jpg, jpeg, png, woff
#   svg
#
# OS specific words
#   filesystem
#   shell, runtime
#
#   SECURITY specific words
#   ssh, tls, ssl
#   token, authentication, authorization, jwt, cookie
#   ddos, session
#
#   DEVOPS specific words
#   development, production, staging
#
#   ARCHITECT specific words
#   monolith, monorepo, Event-Driven, Vertical Slice
#   Distributed
#   large-scale
#   architectures?
#   self-hosted
#
#   QA specific words
#   Reliability
#
#   SWE specific words
#   datastructure, algorithm, oop, fp, !SOLID
#   dependency injection middleware, concept, pattern, anti-patter, idiom, best practice
#   deploy, build, compiler
#   roadmap, computer science
#
#   TODO
#   CQRS
#   ecommerce
#   Vulnerability
#   scanner
#   OpenID Connect Identity Provider
#   network
#   command
#
#   ???
#   client, server
#   */
# }
#
# // TODO should we have `ruby=lang` variations if we parse `ruby` nevertheless?
# // Or `=platform` if we really parse without it...
# // It all slows down the parser...
#
# // TODO GitHub Actions, GitLab CI/CD -- how to avoid false positives with GitHub
#
# //     {name: "Architecture", role: "Architect"},
# //     {name: "Analysis", role: "Analyst"},
# //     {name: "Analytics", role: "Analyst"},
# //     {name: "Engineering", role: "Engineer"},
# //     {name: "Development", role: "Engineer"},
#
# // TODO consider to capture "Web Frontend" as just "Frontend" because in such cases "Web"
# // simply clarifies "Frontend". Such person is not a "Web Developer" in the same sense.
#
# // https://github.com/ivan-kleshnin/devscanr/issues/701
#
# // 4. Terms that are useful in repositories but confusing in user bios
# // E.g. toast, menu, carousel, chartjs, palette, flexbox, bundler, webpack, vite, scrollbar
#
# // http://localhost:3000/platform/search/adw0rd
# // Why this profile has experienceYears: undefined?
# Experience with OP Stack and Arbitrum works is preferred
# Experience with service mesh technologies like Istio or Linkerd.
# + Room (persistence in SQLite library)
# + SAP MM, SAP PM, and SAP EWM
# Kubeflow, Vertex AI Pipelines, TFX
# Kubeflow, Step Functions, MLflow, TFX
# such as Scikit-learn, XGBoost, MXNet, TensorFlow or PyTorch
# exposition to GenAI and solid understanding of multimodal AI via HuggingFace, Llama, VertexAI, AWS Bedrock or GPT
# + Dask
# • Strong proficiency with CI/CD pipelines and distributed computing frameworks like Ray or Dask.
# • Familiarity with model monitoring, logging, and versioning tools (e.g., MLflow, Weights & Biases).
# • Proficient in designing and deploying agentic systems with modern model serving frameworks (e.g., LangChain, vLLM, FastAPI, or KServe).
# Facebook Instant Games SDK
# hypervisor, hyper-v, vmware (also a company)
# ITIL Service Operation frameworks.
