from ...xpatterns import ver1, propn
from ..tag import Company, Skill, Tech
from ..utils import dis_incontext, dis_namelike, dis_nounlike, dis_precisely

SKILLS: list[Skill] = [
  Company("Microsoft", ["(@)microsoft"], "Company"),

  Tech("MS-Access", ["microsoft-access", "ms-access"]),
  Tech("MS-Excel", ["microsoft-excel", "ms-excel", propn("excel")]),
  Tech("MS-SQLServer", [
    "microsoft-sql(=server)", "(ms=)sql=server", "ms=sql",
    "(sql=server-)management-studio",
    "(microsoft-)management-studio",
  ]),
  # TODO T-SQL
  Tech("MS-Sharepoint", ["microsoft-sharepoint", "ms-sharepoint", "sharepoint"]),
  Tech("MS-365", ["microsoft=365", "ms=365"], "New name for MS-Office"),
  Tech("MS-365", ["365"], disambiguate=[
    dis_incontext("microsoft", "office"),
  ]),

  Tech("Power-Platform", ["power-platform"]),
  Tech("Power-Apps", ["power=apps"]),
  Tech("Power-Automate", ["power-automate"]),
  Tech("Power-BI", ["power=bi"]),
  Tech("Power-Pivot", ["power-pivot"]),
  Tech("Power-Query", ["power-query"]),

  # .NET
  Tech(".NET", [ver1(".net"), "dotnet", "dot.net"], "Cross-platform, open source dev. platform"),

  Tech("ASP.NET", ["asp.net", "asp"], ".NET-based web framework that allows to build dynamic sites, apps and services"),
  Tech("ML.NET", ["ml.net"], "ML framework for .NET"),
  Tech(".NET MAUI", [".net maui", "maui"], "Multi-platform app UI, evolution of Xamarin.Forms"),
  Tech("Blazor", ["blazor"], ".NET-based framework to create fullstack apps"),
  Tech("Unity", ["unity-engine", "unity-platform", "unity=3d"], "Gamedev engine"), # , propn("unity")
  Tech("Unity", ["unity"], disambiguate=[
    dis_incontext("c#", "microsoft", "framework"),
    dis_nounlike()
  ]),
  Tech("WCF", ["wcf"], "Windows Communication Foundation: framework for service-oriented apps"),
  Tech("WPF", ["wpf"], "Windows Presentation Foundation: UI framework for desktop apps"),
  Tech("Xamarin", ["xamarin"], "Cross-platform and mobile app development"),

  # SUSPENDED
  # Mono -- non-Windows runtime, acquired together with Xamarin, essentialy a part of .NET now
  # Entity Framework -- ORM for .NET

  # AZURE
  Tech("Microsoft-Azure", [
    "microsoft-azure", "azure",
    "log-analytics", "application-insights",
  ]),
  Tech("Azure-Databricks", ["azure-databricks"]), # uses Apache-Spark | unified, open analytics platform for building, deploying, sharing, and maintaining EE data
  Tech("Azure-DataExplorer", ["azure-data=explorer", propn("adx")]), # big data platform optimized for analytical queries
  Tech("Azure-CosmosDB", ["azure-cosmosdb"]), # noSQL + relational DB
  Tech("Azure-IoT", ["azure-iot"]), # IoT platform
  Tech("Azure-Kubernetes", ["azure-kubernetes-service", "azure-ks", "aks"]), # ~ Amazon-EKS
  Tech("Azure-OpenAI", ["azure-openai"]), # enterprise OpenAI instances
  Tech("Azure-Relay", ["azure-relay"]), # enables to securely expose services that run in corporate network to the public cloud
  Tech("Azure-SQL", ["azure-sql"]), # Managed Cloud Database Service
  Tech("Azure-Synapse", ["azure-synapse"]), # service that brings together enterprise data warehousing and bigdata analytics

  # Azure Blob Storage (= AWS S3)
  # Azure Cognitive
  # Azure Container Instances (ACI)
  # Azure DevOps
  # Azure Files (= AWS EFS)
  # Azure Functions -- AWS Lambda
  # Azure Kubernetes Service (AKS)
  # Azure Managed Disks (= AWS EBS)
  # Azure Pipelines

  # HARDWARE
  Tech("ARM", [
    "aarch32", "arm32",
    "aarch64", "arm64",
  ], "CPU family"),
  Tech("ARM", ["arm"], disambiguate=[
    dis_precisely("ARM"),
    dis_incontext("microsoft", "cpu", "x86", "x32", "x64", "risc", "arc", "processor(s)"),
    dis_namelike(),
  ]),
]
