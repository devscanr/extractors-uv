from ..tag import Certificate, Skill

SKILLS: list[Skill] = [
  Certificate("CompTIA-A+", ["comptia-a+"], "Certificate for tech support and IT ops"),
  Certificate("CompTIA-ITOps", ["cios"]),
  Certificate("CompTIA-Network+", ["network+", "comptia-net(work)+", "comptia-n+"]),
  Certificate("CompTIA-PenTest+", ["pentest+", "comptia-pentest+", "comptia-p+"]),
  Certificate("CompTIA-Security+", ["security+", "comptia-sec(urity)+", "comptia-s+"]),

  Certificate("Cisco-CNA", ["ccna"], "Certificate"), #
  Certificate("Cisco-CNP", ["ccnp"], "Certificate"), # TODO "CCNP or equivalent required; CCIE or other advanced certs are preferred."

  # TODO structure
  Certificate("RHCE", ["rhce"]),
  Certificate("RHCSA", ["rhcsa"]),
  Certificate("CKA", ["cka"]),
  Certificate("CKAD", ["ckad"]),
  Certificate("MCSA", ["mcsa"]),
  Certificate("MTCNA", ["mtcna"]),
  Certificate("CEH", ["ceh"]),
  Certificate("CISA", ["cisa"]),
  Certificate("CISM", ["cism"]),
  Certificate("CISSP", ["ciss", "cissp"], "Certified Information Systems Security Professional"),
  Certificate("CSSLP", ["csslp"], "Certified Secure Software Lifecycle Professional"),
  Certificate("CASE", ["CASE"], "Certified Application Security Engineer"),
  Certificate("GIAC-CIH", ["gcih"]),
  Certificate("GIAC-SEC", ["gsec"]),
  Certificate("GIAC-REM", ["grem"]),
  Certificate("GIAC-WAPT", ["gwapt"]),
  Certificate("OSCP/OSCE", ["oscp", "osce"]),
  Certificate("SSCP", ["sscp"]),
  # Relevant certifications (kept only new: CISSP-ISSAP, CCSP, SC-100, CRTSA, GDSA, TOGAF) are highly desirable.
  # SANS (GPEN, GXPN, GWAPT) -- wtf: SANS vs GIAC
  # certificates: AWS Certified Solutions Architect Professional, AWS Certified DevOps Engineer Professional
]
