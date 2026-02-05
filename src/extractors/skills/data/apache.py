from ..tag import Company, Skill, Tech
from ..utils import dis_incontext, dis_nounlike

SKILLS: list[Skill] = [
  Company("Apache", ["(@)apache"]),

  Tech("Apache-Maven", ["apache-maven", "maven"]),

  # HADOOP
  Tech("Apache-Hadoop", ["apache-hadoop", "hadoop"]),
	Tech("Apache-Ambari", ["apache-ambari", "ambari"], "Running app manager"),
	Tech("Apache-Beam", ["apache-beam"], "Unified model and set of SDKs for defining and executing data processing workflows and data ingestion"),
	Tech("Apache-Beam", ["beam"], disambiguate=[
    dis_incontext("apache", "kafka"),
    dis_nounlike(),
  ]),
  Tech("Apache-Flume", ["apache-flume", "flume"], "Hadoop data ingestion (streams, logs) to HDFS"),
  Tech("Apache-Flink", ["apache-flink", "flink"], "Scalable batch and stream data processing"),
  Tech("Apache-Hive", ["apache-hive"], "Data warehouse with SQL querying"),
  Tech("Apache-Hive", ["hive"], disambiguate=[
    dis_incontext("apache", "kafka"),
    dis_nounlike(),
  ]),
  Tech("Apache-Kafka", ["apache-kafka", "kafka"]),
  Tech("Apache-Lucene", ["apache-lucene", "lucene"]),
  Tech("Apache-MapReduce", ["apache-mapreduce", "mapreduce"], "Hadoop data pipilene"),
  Tech("Apache-Mahout", ["apache-mahout"], "ML, substituted by Spark"),
  Tech("Apache-Pig", ["apache-pig"], "Used to analyze Hadoop data (higher-level MapReduce)"),
  Tech("Apache-Pig", ["pig"], disambiguate=[
    dis_incontext("apache", "kafka"),
    dis_nounlike(),
  ]),
  Tech("Apache-Sqoop", ["apache-sqoop", "sqoop"], "Hadoop data ingestion from relational databases to HDFS"),
  Tech("Apache-Spark", ["apache-spark", "spark", "pyspark", "sparksql"], "Distributed data processing engine, a MapReduce replacement"),
  Tech("Apache-Storm", ["apache-storm"], "Like Kafka but for real-time streaming"),
  Tech("Apache-Storm", ["storm"], disambiguate=[
    dis_incontext("apache", "kafka"),
    dis_nounlike(),
  ]),
  Tech("Apache-ZooKeeper", ["apache-zookeper"], "Centralized service for process configuration and distributed synchronization"),
  Tech("Apache-ZooKeeper", ["zookeper"], disambiguate=[
    dis_incontext("apache", "kafka"),
    dis_nounlike(),
  ]),

  # HADOOP + SECURITY
  Tech("Apache-Ranger", ["apache-ranger"], "Decide who can access what resources on a Hadoop cluster"),
  Tech("Apache-Ranger", ["ranger"], disambiguate=[
    dis_incontext("apache", "kafka"),
    dis_nounlike(),
  ]),
  Tech("Apache-Knox", ["apache-knox"], "Decides who can access a Hadoop cluster"),
  Tech("Apache-Knox", ["knox"], disambiguate=[
    dis_incontext("apache", "kafka"),
    dis_nounlike(),
  ]),

  # HADOOP + DATABASE
  Tech("Apache-Arrow", ["apache-arrow"], "Columnar memory format optimized for efficient analytics"),
  Tech("Apache-Arrow", ["arrow"], disambiguate=[
    dis_incontext("apache", "kafka"),
    dis_nounlike(),
  ]),
  Tech("Apache-Cassandra", ["apache-cassandra", "cassandra"]),
  Tech("Apache-DataFusion", ["apache-datafusion", "datafusion"], "Extensible SQL query engine that uses Apache Arrow"),
  Tech("Apache-HDFS", ["apache-hdfs", "hdfs"], "Hadoop drive FS"),
  Tech("Apache-HBase", ["apache-hbase", "hbase"], "Hadoop NoSQl key-value DB"),

  # HADOOP + INFRASTRUCTURE
  Tech("Apache-Airflow", ["apache-airflow", "airflow"], "ETL tool for planning, generating, and tracking processes"),
  Tech("Apache-Oozie", ["apache-oozie", "oozie"], "Hadoop jobs workflow scheduler (~ GitHub actions)"),
  Tech("Apache-ActiveMQ", ["apache-active=mq", "active=mq"], "Message broker"),

  # Apache-Drill
  # Apache-Kylin
]
