from ..tag import Skill, Company, Tech

SKILLS: list[Skill] = [
  Company("Yandex", ["(@)yandex"], "Company"),

  Tech("ClickHouse", ["clickhouse"]),

  # CLOUD
  # Skill("?", ["yt"], ""), # many FPs
  Tech("YDB", ["ydb"], "Distributed SQL database with high availability, scalability, and strong consistency"), # https://ydb.tech/
]
