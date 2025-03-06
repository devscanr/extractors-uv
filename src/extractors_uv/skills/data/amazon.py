from ..tag import Company, Skill, Tech
from ..utils import dis_incontext, dis_namelike, dis_nounlike

SKILLS: list[Skill] = [
  Company("Amazon", ["(@)amazon"]),

  Tech("AWS-CDK", ["aws=cdk", "cdk"], "Framework for defining and provisioning cloud IAC"),

  # AWS
  Tech("AWS", ["amazon-web=services", "aws"], "AWS"),
  Tech("AWS-Athena", ["aws=athena", "amazon=athena"], "Analytics, ML + SQL over S3"),
  Tech("AWS-Athena", ["athena"], disambiguate=[
    dis_incontext("amazon", "aws"),
    dis_namelike(),
  ]),
  Tech("AWS-Aurora", ["aws=aurora", "amazon=aurora"], "Managed DB"),
  Tech("AWS-Aurora", ["aurora"], disambiguate=[
    dis_incontext("amazon", "aws"),
    dis_namelike(),
  ]),
  Tech("AWS-Beanstalk", ["aws=beanstalk", "amazon=beanstalk", "beanstalk"], "Webapp deployment"),
  Tech("AWS-CloudFormation", ["aws=cloudformation", "amazon=cloudformation", "cloudformation"], "IAC provisioning"),
  Tech("AWS-CloudFront", ["aws=cloudfront", "amazon=cloudfront", "cloudfront"], "CDN"),
  Tech("AWS-CloudWatch", ["aws=cloudwatch", "amazon=cloudwatch", "cloudwatch"], "Monitoring umbrella"),
  Tech("AWS-Cognito", ["aws=cognito", "amazon=cognito", "cognito"], "Authentication and authorization for web and mobile applications"),
  Tech("AWS-DynamoDB", ["aws=dynamo=db", "amazon=dynamo=db", "dynamo=db"], "Distributed NoSQL DB"),
  Tech("AWS-EC2", ["aws=ec2", "amazon=ec2", "ec2"], "Elastic compute cloud"),
  Tech("AWS-ECS", ["aws=ecs", "amazon=ecs", "ecs"], "Elastic container services"),
  Tech("AWS-EBS", ["aws=ebs", "amazon=ebs", "ebs"], "Elastic block store"),
  Tech("AWS-EKS", ["aws=eks", "amazon=eks", "eks"], "Elastic kubernetes service"),
  Tech("AWS-ElastiCache", ["aws=elasticache", "amazon=elasticache", "elasticache"], "Caching"),
  Tech("AWS-Glue", ["aws=glue", "amazon=glue"], "Batch data ingestion, data pipeline orchestration"),
  Tech("AWS-Glue", ["glue"], disambiguate=[
    dis_incontext("amazon", "aws"),
    dis_nounlike(),
  ]),
  Tech("AWS-IAM", ["aws=iam", "amazon=iam"], "Identity and access management"),
  Tech("AWS-IAM", ["iam"], disambiguate=[
    dis_incontext("amazon", "aws"),
    dis_nounlike(),
  ]),
  Tech("AWS-Lambda", ["aws=lambda", "amazon=lambda"], "Lambda service"),
  Tech("AWS-Lambda", ["lambda"], disambiguate=[
    dis_incontext("amazon", "aws"),
    dis_nounlike(),
  ]),
  Tech("AWS-KMS", ["aws=kms", "amazon=kms"], "Streaming data ingestion & analytics"),
  Tech("AWS-KMS", ["kms"], disambiguate=[
    dis_incontext("amazon", "aws"),
    dis_nounlike(),
  ]),
  Tech("AWS-Kinesis", ["aws=kinesis", "amazon=kinesis", "kinesis"], "Streaming data ingestion & analytics"),
  Tech("AWS-Neptune", ["aws=neptune", "amazon=neptune", "neptune"], "Graph DB"),
  Tech("AWS-SNS", ["aws=sns", "amazon=sns", "sns"], "Simple notification service"),
  Tech("AWS-SQS", ["aws=sqs", "amazon=sqs", "sqs"], "Simple queue service"),
  Tech("AWS-S3", ["aws=s3", "amazon=s3", "s3"], "Object storage"), # should we disambiguate S3?
  Tech("AWS-RDS", ["aws=rds", "amazon=rds", "rds"], "Relational database service"),
  Tech("AWS-Redshift", ["aws=redshift", "amazon=redshift", "redshift"], "Data warehouse & BI"),
  Tech("AWS-SageMaker", ["aws=sagemaker", "amazon=sagemaker", "sagemaker"], "Deploy ML"),
  Tech("AWS-VPC", ["aws=vpc", "amazon=vpc"], "Virtual private cloud"),
  Tech("AWS-VPC", ["vpc"], disambiguate=[
    dis_incontext("amazon", "aws"),
    dis_nounlike(),
  ]),

  # SUSPENDED (for now)
  # Autoscale
  # API Gateway
  # App Load Balancer
  # CloudTrail
  # EMR
  # EventBridge
  # QuickSight -- data analytics, dashboards
  # Rekognition
  # Route 53
  # SageMaker
  # Step Functions -- data pipeline orchestration
]
