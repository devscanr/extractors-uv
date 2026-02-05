from ..tag import Company, Skill, Tech
from ..utils import dis_incontext, dis_namelike, dis_nounlike
from ...xpatterns import ver1

SKILLS: list[Skill] = [
  Company("Google", ["(@)google"], "Company"),

  Tech("Flax", ["flax"], "NN for Jax"),
  Tech("JAX", ["JAX"], "TensorFlow alternative"),
  Tech("JAX", ["jax"], disambiguate=[
    dis_incontext("google", "flax", "tensorflow"),
    dis_namelike(),
  ]),
  Tech("TensorFlow", ["tensorflow"]),
  Tech("TensorFlow-Lite", ["tf-lite"], "Edge AI deployment"),

  Tech("Flutter", ["flutter"]),

  # CLOUD
  Tech("Google-BigQuery", ["google-bigquery", "bigquery"]), # EE data warehouse
  Tech("Google-BigTable", ["google-bigtable", "bigtable"]), # fast flexible noSQL
  Tech("Google-Cloud", ["google=cloud", "gcp"]),
  Tech("Google-Cloud", ["gc"], disambiguate=[
    dis_incontext("aws", "azure"),
    dis_nounlike(),
  ]),
  Tech("Google-CloudStorage", ["google-cloud=storage", "gcs"]),
  Tech("Google-Firebase", ["google=firebase", "firebase"]),
  Tech("Google-Gemini", ["google=gemini", ver1("gemini")]),
  Tech("Google-Kubernetes", ["google-kubernetes-engine", "google=ke", "google=ks", "gke", "gks"]), # ~ Amazon-EKS
  Tech("Google-Pub/Sub", ["google-pub/sub", "google-pub=sub", "cloud pub/sub", "cloud-pub=sub"]),
  Tech("Google-Sheets", ["google=sheets"]),

  # Drive
  # GC Functions
  # GC Firestore (= AWS EFS)
  # GC Storage (= AWS S3)
  # GC SSD (= AWS EBS)
  # GC AI Platform
  # GC Kubernetes Engine (GKE)
  # GC Pub/Sub
  # GC Run
]

# computer science student majoring in MIT
