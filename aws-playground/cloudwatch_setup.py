import boto3
from datetime import datetime

cloudwatch = boto3.client(
    "cloudwatch",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

# Fake Metric bhejna
def send_metric():
    cloudwatch.put_metric_data(
        Namespace="MyApp",
        MetricData=[
            {
                "MetricName": "CPUUsage",
                "Value": 75.0,
                "Unit": "Percent",
                "Timestamp": datetime.now()
            }
        ]
    )
    print("✅ Metric Sent: CPUUsage = 75%")

# Metrics padhna
def get_metrics():
    response = cloudwatch.list_metrics(Namespace="MyApp")
    print("\n📋 CloudWatch Metrics:")
    for metric in response["Metrics"]:
        print(f"  → {metric['MetricName']}")

send_metric()
get_metrics()