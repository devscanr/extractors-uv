from ..tag import Skill, Company, Tech

SKILLS: list[Skill] = [
  Company("HashiCorp", ["(@)hashicorp"], "Company"),

  # OPS
  Tech("Consul", ["consul"], "Service-based networking"),
  Tech("HCL", ["hcl"], "Configuration language for infrastructure automation"),
  Tech("Nomad", ["nomad"], "Workload scheduling and orchestration"),
  Tech("Packer", ["packer"], "Build and manage images as code"),
  Tech("Terraform", ["terraform"], "Cloud infrastructure provisioning using a common workflow"),
  Tech("Vault", ["vault"], "Identity-based secrets management"),
]
