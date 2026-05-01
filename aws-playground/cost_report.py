import boto3
from datetime import datetime, timezone

ec2 = boto3.client(
    "ec2",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

EC2_COST_PER_HOUR = 0.0116
S3_COST_PER_GB = 0.023

def generate_report():
    report = []
    report.append("=" * 40)
    report.append("   AWS COST OPTIMIZER REPORT")
    report.append("   Date: " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    report.append("=" * 40)

    # EC2 Section
    report.append("\nEC2 INSTANCES:")
    report.append("-" * 40)
    ec2_total = 0
    response = ec2.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if instance["State"]["Name"] == "running":
                launch_time = instance["LaunchTime"]
                now = datetime.now(timezone.utc)
                running_hours = (now - launch_time).seconds // 3600
                if running_hours == 0:
                    running_hours = 1
                cost = running_hours * EC2_COST_PER_HOUR
                ec2_total += cost
                report.append("Instance ID : " + instance["InstanceId"])
                report.append("Type        : " + instance["InstanceType"])
                report.append("Hours       : " + str(running_hours))
                report.append("Cost        : $" + str(round(cost, 4)))
                report.append("")

    # S3 Section
    report.append("S3 BUCKETS:")
    report.append("-" * 40)
    s3_total = 0
    buckets = s3.list_buckets()["Buckets"]
    for bucket in buckets:
        objects = s3.list_objects(Bucket=bucket["Name"])
        contents = objects.get("Contents", [])
        size_gb = sum(obj["Size"] for obj in contents) / (1024 * 1024 * 1024)
        cost = size_gb * S3_COST_PER_GB
        s3_total += cost
        report.append("Bucket Name : " + bucket["Name"])
        report.append("Files       : " + str(len(contents)))
        report.append("Size        : " + str(round(size_gb, 4)) + " GB")
        report.append("Cost        : $" + str(round(cost, 4)))
        report.append("")

    # Total
    report.append("=" * 40)
    report.append("EC2 Total   : $" + str(round(ec2_total, 4)))
    report.append("S3 Total    : $" + str(round(s3_total, 4)))
    report.append("GRAND TOTAL : $" + str(round(ec2_total + s3_total, 4)))
    report.append("=" * 40)

    # File mein save karo
    with open("aws_cost_report.txt", "w") as f:
        f.write("\n".join(report))

    print("\n".join(report))
    print("\nReport saved to aws_cost_report.txt")

generate_report()