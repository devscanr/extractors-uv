from ...skills.utils import dis_incontext, dis_nounlike
from ...xpatterns import nounlike
from ..tag import Skill, Topic
from ..utils import dis_precisely

SKILLS: list[Skill] = [
  # ANALYSIS >
  Topic("AB-Testing", ["a/b-test(s)", "a/b-testing", "ab-test(s)", "ab-testing"]),

  # ENGINEERING / ARCHITECTURE >
  Topic("Accessibility", ["accessibility", "accessible"]),
  Topic("Availability", ["availability"]),
  Topic("Performance", [
    "performance", "performant",
    "benchmarking", "benchmark(s)",
  ]),
  Topic("Scalability", ["scalability", "scalable"]),
  Topic("Reliability", ["reliability", "reliable"]),
  Topic("Usability", ["usability", "usable"]),
  # Highly Available, High Availability
  # High Performance, High Traffic
  # Bandwidth, Throughput -- also specific to NETWORKS

  # SOFTWARE >
  Topic("Agile", ["agile", "kanban", "scrum"]),
  Topic("API", ["api(s)"], publicname="APIs"),
  Topic("Client-Server", ["client", "server(s)"]), # FPs for "clients"
  Topic("BDD", ["bdd"]),
  Topic("DDD", ["ddd"]),
  Topic("TDD", ["tdd"]),
  # YAGNI, DRY, KISS
  # (software) design patterns
  Topic("Algorithm", ["algorithm(s)", "algorithmic"], publicname="Algorithms"),
  Topic("Big-O", ["big-o"]),
  Topic("Data-Structure", ["data=structure(s)", "data=type(s)", "data=class(es)"], publicname="Data-Structures"),
  Topic("Debugging", ["debugging", "debugger"]),
  Topic("FP", ["functional=programming", "fp", "фп"]),
  Topic("I18n", ["i18n", "l10n"]),
  Topic("MVC", ["mvc", "mvvm", "model-view-controller"]),
  Topic("OOP", [
    "object=oriented( programming)", "oop",
    "S.O.L.I.D",
    # "SOLID",
    "ооп"
  ]),
  Topic("Open-Source", ["open=source", "oss"]),
  Topic("SDKs", ["sdk(s)"]),
  Topic("VCSs", ["version=control(=system)", "vcs(s)", "branching", "versioning"]),

  ## DESIGN >
  Topic("Animation", ["animation", "animated", "animating", "animator"]),
  Topic("Typography", ["typography"]),
  Topic("UI/UX", [
    "ui=ux", "ui/ux", "uix", "ui", "ux", "user=interface", "human=interface", "user=experience"
  ]),

  # BACKEND
  Topic("Backend", [
    "back=end", "backender",
    nounlike("BE")
  ]), # not detected as PROPN, needs to be retrained
  Topic("Access-Control", ["rbac", "abac", "acl"]), # also SECURITY
  Topic("Authentication", ["authentication", "auth", "sign=in", "sign=out"]), # also SECURITY
  Topic("Authorization", ["authorization"]), # also SECURITY
  Topic("BaaS", ["baas", "mbaas"]),
  Topic("Microservice", ["micro=service(s)"], publicname="Microservices"),
  Topic("Middleware", ["middleware(s)"], publicname="Middlewares"),
  Topic("OAuth", ["oauth", "oauth1", "oauth2"]), # also SECURITY
  Topic("OpenID", ["openid"]), # also SECURITY
  Topic("OpenAPI", ["openapi"]), # TODO more like this
  Topic("REST", ["rest=api", "restful"]),
  Topic("REST", ["rest"], disambiguate=[
    dis_precisely("REST"),
    dis_incontext("api", "graphql", "rpc", "framework", "#go", "php"),
    dis_nounlike(),
  ]),
  Topic("-REST", [
    "rest=in=peace"
  ]),
  Topic("RPC", ["rpc=api", "rpc"]),
  Topic("Serverless", ["serverless"]),
  Topic("SOAP", ["soap"]),
  Topic("SSG", ["ssg"]),
  Topic("SSR", ["ssr"]),
  Topic("SSO", ["sso"]), # also SECURITY

  # BLOCKCHAINS >
  Topic("Crypto", ["crypto"]),
  Topic("dApp", ["decentralized-application(s)", "dapp(s)"], publicname="dApps"),
  Topic("DeFi", ["decentralized-finance", "de=fi"]),
  Topic("P2P", ["peer=2=peer", "peer=to=peer", "p2p"]), # also NETWORKS
  Topic("Smart-Contract", ["smart=contract(s)"], publicname="Smart-Contracts"),
  Topic("Web3", ["web3"]),

  # DATA >
  Topic("Big-Data", ["big=data"]),
  Topic("Data-Mining", ["data=mining", "data=extraction"]),
  Topic("Data-Visualization", ["data=visualization(s)", "data=visualisation(s)", "data=viz"]),
  Topic("ETL", ["etl(s)", "elt"]),
  Topic("OCR", ["ocr", "optical=character=recognition"]),

  # DATABASES >
  Topic("Datalake", ["data=lake(s)"], publicname="Datalakes"),
  Topic("ORM", ["orm"]),
  Topic("NoSQL", ["nosql"]),
  Topic("Warehouse", ["warehouse(s)"], publicname="Warehouses"),

  # FRONTEND
  Topic("Frontend", [
    "front=end", "frontender",
    nounlike("FE"),
  ]),
  # BEM, БЭМ
  Topic("Browser", ["browser"]),
  Topic("Canvas", ["canvas"]),
  Topic("DevTool", ["dev=tool(s)"], publicname="DevTools"),
  Topic("DOM", ["dom"]),
  Topic("Flexbox", ["flex=box"]),
  Topic("MPA", ["mpa"]),
  Topic("SPA", ["spa"]),
  Topic("-SPA", ["med spa", "medical spa"]),
  Topic("Markup", ["markup"]),
  Topic("WebGL", ["webgl"]),
  Topic("Web-Component", ["web=component(s)"], publicname="Web-Components"),

  # GAMES >
  # Topic("Pixel", ["pixel(s)"]),
  # Topic("-Pixel", ["google=pixel"]),
  # Topic("Voxel", ["voxel(s)"]),
  # Polygon -- disambig.
  Topic("Shader", ["shader(s)"], publicname="Shaders"),
  Topic("Sprite", ["sprite(s)"], publicname="Sprites"),
  Topic("Texture", ["texture(s)"], publicname="Textures"),
  # TODO add game-specific non-graphic topics

  # HARDWARE >
  Topic("CPU", ["cpu", "central-processing-unit"]),  # also SYSTEMS
  Topic("CPU", ["micro=processor(s)"]),
  Topic("CPU", ["processor(s)"], disambiguate=[
    dis_incontext("amd", "intel", "arm", "arc", "risc", "x86", "x32", "x64"),
    dis_nounlike(),
  ]),
  Topic("Embedded", ["embedded"]),
  Topic("Firmware", ["firmware"]),
  Topic("GPU", ["gpu"]),         # also SYSTEMS
  Topic("HDD", ["hdd", "hmdd"]), # also SYSTEMS
  Topic("IoT", ["iot", "internet-of-things"]),
  Topic("Kernel", ["kernel"]), # also SYSTEMS
  Topic("Motherboard", ["motherboard(s)"], publicname="Motherboards"),
  Topic("PCB", ["pcb"]),
  Topic("PCI", ["pci"]), # also SYSTEMS
  Topic("RAM", ["RAM"]), # also SYSTEMS
  Topic("SSD", ["hdd"]), # also SYSTEMS

  # LOW-CODE
  Topic("Low-Code", ["low=code", "no=code"]),
  Topic("SaaS", ["saas"]),
  Topic("CMS", ["cms", "content=management=system"]),
  Topic("CRM", ["crm", "customer=relationship=management"]),
  Topic("ERP", ["erp"]),

  # MACHINE-LEARNING >
  Topic("AI", ["ai", "artificial-intelligence"]),
  Topic("Deep-Learning", ["deep=learning", "deep=reinforcement=learning", "dl"]), # not sure about FPs for "dl"
  Topic("Large-Language-Model", [
    "large-language-model(s)", "llm(s)",
    "multimodal-large-language-model(s)", "mllm(s)"
  ], publicname="Large-Language-Models"),
  Topic("Natural-Language-Processing", ["natural=language=processing", "nlp"]),
  Topic("Neural-Network", ["(deep=)neural-networks", "nn", "dnn"], publicname="Neural-Networks"), # not sure about FPs
  # Signal Processing, Face Detection

  # MOBILE >
  Topic("Cross-Platform", ["cross=platform"]), # also SYSTEMS
  Topic("Desktop", ["desktop"]),
  Topic("Device", ["device(s)"], publicname="Devices"),
  # TODO more topics

  # NETWORKS >
  Topic("Bluetooth", ["bluetooth"]), # also EMBEDDED
  Topic("CDN", ["cdn(s)"]),
  Topic("DNS", ["dns"]),
  Topic("Firewall", ["firewall(s)"], publicname="Firewalls"), # also SECURITY
  Topic("FTP", ["ftp"]),
  Topic("SFTP", ["sftp"]), # also SECURITY
  Topic("HighLoad", ["high=load"]),
  Topic("HTTP", ["http"]),   # also BACKEND and more
  Topic("HTTPS", ["https"]), # also SECURITY
  Topic("IP", ["ip", "ip(v)4", "ip(v)6"]),
  Topic("Proxy", ["proxy", "proxies"], publicname="Proxies"),
  Topic("SMTP", ["smtp"]),
  Topic("SOCKS", ["socks", "socks4", "socks5"]),
  Topic("SSL", ["ssl"]),
  Topic("TCP", ["tcp"]),
  Topic("UDP", ["udp"]),
  Topic("VLAN", ["vlan"]),
  Topic("VPN", ["vpn(s)"]), # also SECURITY
  Topic("Wi-Fi", ["wi=fi"]), # also EMBEDDED
  Topic("Wireless", ["wireless"]),

  # OPERATIONS >
  Topic("CI/CD", [
    "continuous=integration", "continuous=delivery", "continuous=deployment",
    "ci/cd", "ci",
  ]),
  Topic("Cloud", ["cloud(s)"]),
  Topic("Deployment", ["deployment(s)", "deploy(s)"]),
  Topic("Gitops", ["gitops"]),
  Topic("IaaS", ["iaas", "caas", "haas"]),
  Topic("PaaS", ["paas"]),
  Topic("IAC", ["iac", "infrastructure=as=code"]),
  Topic("Monorepo", ["mono=repo(s)", "mono=repository", "mono=repositories"], publicname="Monorepos"),
  Topic("Containerization", ["containerization", "containerized"]), # TODO container with disambig.
  Topic("Integration", ["integration(s)"], publicname="Integrations"),
  Topic("Orchestration", ["orchestration"]),
  Topic("Provisioning", ["provisioning"]),
  Topic("Virtualization", ["virtualization", "virtual=machine(s)", "vm(s)"]),
  Topic("VPC", ["vpc(s)"], publicname="VPCs"),
  # blue green deployments

  # ROBOTICS >
  Topic("Computer-Vision", ["computer=vision"]),
  Topic("RTOS", ["rtos"]),
  Topic("GPOS", ["gpos"]),
  Topic("Sensor", ["sensor(s)"], publicname="Sensors"),
  # Motion-Prediction
  # Sensor-Fusion
  # Radar, lidar, Quadro-Copters
  # Self-Driving cars

  # SECURITY >
  # offensive security, audit
  Topic("Cyber-Security", [
    "cyber=security", "cyber=sec", "cyber=defence",
    "exploit(s)", "malware", "malicious",
    "vulnerability", "vulnerabilities",
    "jailbreaking", "guardrails", "safety=alignment",
  ]),
  Topic("Info-Security", [
    "information=security", "info=security", "info=sec",
    "it=security", "it=sec",
  ]),
  # Identity and Access management
  Topic("Antivirus", ["anti=virus(es)"], publicname="Antiviruses"),
  Topic("Bruteforce", ["bruteforce"]),
  Topic("DDOS", ["ddos"]), # also NETWORKs
  Topic("Encryption", ["encryption"]), # also NETWORKs
  Topic("Phishing", ["phishing"]),
  Topic("Social-Engineering", ["social=engineering"]),
  Topic("VA/PT", [
    "penetration=testing", "penetration=test(s)", "penetration=tester",
    "pen=testing", "pen=test", "pen=tester",
    "vapt",
    "vulnerability=assessment",
    "vulnerability=scanning", "vulnerability=scan(ner)",
    "vulnerability=testing", "vulnerability=test(s)", "vulnerability=tester",
  ]), # also NETWORKs
  Topic("ISO-27001", ["iso-27001"]), # "Security Compliance"
  Topic("GDPR", ["gdpr"]), # "Security Compliance"
  Topic("NIST", ["nist"]), # "Security Compliance"
  # Familiarity with industry standards like MITRE ATT&CK and D3FEND,
  # the NIST Cybersecurity Framework, STIX/TAXII, and OpenIOC
  # "Privacy"

  # SYSTEMS
  Topic("System", ["system(s)"], publicname="Systems"), # TODO many FPs e.g. "information systems"
  Topic("ASTs", ["ast(s)"]),
  Topic("Compiler", ["compiler(s)", "compiling", "compilation", "compile-time", "run=time"], publicname="Compilers"),
  Topic("CLI", ["cli", "stdin", "stdout", "stderr", "command=line", "terminal"]),
  Topic("GUI", ["gui"]),
  Topic("Cron", ["cron(s)", "crond", "cronjob(s)"]),
  Topic("Decentralized", ["decentralized"]),
  Topic("Distributed", ["distributed"]),
  Topic("Logging", ["logging"]),       # also OPERATIONS
  Topic("Monitoring", ["monitoring"]), # also OPERATIONS
  Topic("Parser", ["parser(s)", "parsing"], publicname="Parsers"),
  Topic("Process", ["process(es)", "processing", "multi=processing"], publicname="Processes"),
  Topic("SSH", ["ssh"]), # also OPERATIONS
  Topic("Socket", ["socket(s)"], publicname="Sockets"),
  Topic("Stream", ["stream(s)", "streaming", "server-sent=events", "sse"], publicname="Streams"),
  Topic("Thread", ["thread(s)", "threading", "multi=threading"], publicname="Threads"),
  # Computer(s) (computing) (from CS)
  # Scheduler / Scheduling

  # TESTING & QA
  Topic("QA", ["quality-assurance", "qa"]),
  Topic("AQA", ["aqa"], resolve=["Automation", "QA"]),
  Topic("E2E-Testing", ["end=to=end=testing", "e2e=testing", "e2e=test(s)"]), # TODO capture split words
  Topic("Load-Testing", ["load=testing", "load=test(s)"]),
  Topic("Functional-Testing", ["functional=testing", "functional=test(s)"]),
  Topic("Regression-Testing", ["regression=testing", "regression=test(s)"]),
  Topic("Unit-Testing", ["unit=testing", "unit=test(s)"]),

  # WEB >
  Topic("CORS", ["cors"]), # also SECURITY
  Topic("WebSocket", ["websocket(s)", "ws"], publicname="WebSockets"), # also NETWORKS

  # UNSORTED
  Topic("AR/VR", [
    "augmented=reality", "mixed=reality", "virtual=reality",
    "vr/ar", "vr/mr", "ar/vr", "mr/vr", "vr",
  ]),
  Topic("Leadership", ["leadership", "leader", "lead", "leading role"]),
  # Topic("Modeling", ["datamodeling"]), - "database=modeling" is now translated to [Databases, Engineering]
  Topic("Scraping", ["scraping", "webscraping"]),
  Topic("Videography", ["videography", "videographer", "video(s)"]),
  # Audio, Sound, Image(s), Video(s)
  Topic("Visualization", ["visualization", "visualizer"], publicname="Visualizations"),
  # Bot(s)

  # Topic("2D", ["2d"]), -- too widespread
  # Topic("3D", ["3d"]), -- too widespread
  # Topic("Ray-Tracing", ["ray=tracing"]),

  # Topic("Entity-Component-System", ["entity-component-system", "ecs"]), -- conflicts with AWS-ECS

  # COMBINED ---------------------------------------------------------------------------------------
  Topic("Data-Warehouse", ["data=warehouse(s)", "dwh"], resolve=["Data", "Warehouse"]),
  Topic("Fullstack", ["full=stack(er)"], resolve=["Backend", "Frontend"]),
  Topic("SDET", ["sdet"], resolve=["Software", "Engineering", "Testing"]),
  Topic("SDLC", ["sdlc"], resolve=["Software", "Engineering", "Testing", "Deployment"]),
  Topic("SRE", ["SRE"], resolve=["Reliability", "Engineering"]),
  Topic("Web-API", ["webapi(s)"], resolve=["Web", "API"]),
]

# TODO phpdeveloper, webarchitect, phpcoder, dbadmin, rubydev

# TODO split into inside (dev) and outside topics

# malware-analysis = security-research

# Topic("Resilience", ["resilience", "resilient"]),
# Topic("Observability", ["observability", "observable"]),
# Clustering, Sharding, load balancing
# Replication, Partitioning | Enterprise, large-scale
# Topic("Resiliency", ["resiliency", "resilient"]),
# Topic("Cluster", ["cluster"]),
# 3D modeling
# Hacking
# Quantum Computing
# Threat-intelligence
# Grid, Layout(s), Responsive, Flexible

# Non-skills (words that look like skills but are not, might be useful to help with them in UI)
# SOTA: state of the art
# neuroscience, neuroscientist +1
# transportation industry
# digital illustration
# cognitive science, cog-sci
# "5 yrs teaching FinTech and Market Operations. 30 yrs PMO Digital Transformations of Wall St. Investment Banks
# Talend
# Crucible
# Involved with VNFs, Cloud, etc
# I automate the web and moble-web; making bots and working in the cloud. Lately, I have been hired to make some anti-bots.
# Trade Settlements Analyst
# A tech-savvy story teller who loves to tell stories, not verbally, but through data.
# I am a LINUX/UNIX Administratory
# Biomedical Engineer
# Interest in Bioinformatics/Biostatistics
# has worked as a Director, Cinematographer, Sound Mixer, Videographer, Editor, and Producer for 10 years.
# analytical
# sales
# implementation of COTS software
# CPA turned developer
# Information Science != Informatics (1st is broader)
# "Python, STATA, SQL, R, SPSS, NVivo.", -- STATA? SPSS? NVivo?
# Information Technology
# 'Rohit Kabra (Masters in information System)
# data extraction/modeling, visualization (Tableau, Power BI)
# edge (ambiguous)
# Astrophysics
# HRD term
# Real-Time x 2
# OCR models
# Familiarity with ConvNeXt and similar models
# • Extensive hands-on experience with BGP, OSPF, and EIGRP routing protocols in large-scale, enterprise environments.
# • In-depth knowledge of Layer 2 and Layer 3 network technologies, including VLANs, spanning-tree, and routing.
# • Proven expertise in SD-WAN architecture and deployment.
# • Proficiency with networking products and solutions from Cisco, Meraki, Fortinet, Palo Alto, and other leading vendors.
# • In-depth knowledge of VoIP protocols (e.g., SIP, RTP, H.323) and their application in diverse environments.
# • Strong experience in unified communications platforms (e.g., Cisco, Avaya, Asterisk, Microsoft Teams).
# • Advanced understanding of VoIP hardware and software, including PBX systems, softphones, and gateways.
# ISTQB Performance testing experience
# • Knowledge of DoD STIGs, STIG vulnerabilities, and remediation strategies
# President at Intellect Neurosciences, Inc. | Business Officer and Co-Founder at Various Life Science Companies | Former Chief Executive Officer at Immune Pharma
# Data Scientist actively looking for a position within the pharma/healthcare industry.
# I am currently a Ph.D. candidate in a Geosciences program, seismology in particular.
# I have a mixed background in Biology and Computer Science. I also work in an animal hospital and love being around my dogs and cats.
# I am a newbie Data Analyst who likes to explore data concerning cognitive neuroscience, psychology, gaming, anime and book publishing.
# News, publishing, and media industry experience.
# I am an oceanographer and climate scientist who investigates the interactions between the ocean, the atmosphere, and the rest of the Earth System.
# Astronomy PhD student and data scientist.
# Ph.D. Candidate in Systems Engineering with focus in Optimization of Distributed Spacecraft Missions.
# Electrical Engineer interested in the intersection of software and hardware to build better healthcare technologies including diagnostics, robotics, and devices
# Sensor Fusion and Navigation Engineer at Kearfott, previous experiences at @American-Robotics, @fdcl-gwu
# Design verification engineer working with ORAN/LTE/5g radio hardware
# HPC (high performance computing)
# Electrician by trade, Electrical & Computer Engineering Student, Programmer, Maker, Photographer by Hobby.
# Seasoned IT Storage Architect specializing in SAN and NAS infrastructure design , migration and deployment strategies
# Pro tinkerer- Odroid, Pi, Pine- ARM Boards. Virtualization, LXC
# I'm an ASU graduate with a degree in Graphic Information Technology.
# WordPress, PHP, Stellar Lumens, XDC, XRPL, Python and Solidity. Rodi Software.
# Software Developer, I like to use GNU Emacs and NixOS.

# HIREABLE
# "#OpenToWork"

# Counter-cases for "Architecture"
# licensed architect, architectural designer and web developer/programmer
