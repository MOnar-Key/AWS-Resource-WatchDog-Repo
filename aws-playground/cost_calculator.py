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

# AWS Pricing (per hour)
EC2_COST_PER_HOUR = 0.0116
S3_COST_PER_GB = 0.023

def calculate_ec2_cost():
    print("Calculating EC2 Cost...\n")
    response = ec2.describe_instances()
    total_cost = 0
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if instance["State"]["Name"] == "running":
                launch_time = instance["LaunchTime"]
                now = datetime.now(timezone.utc)
                running_hours = (now - launch_time).seconds // 3600
                if running_hours == 0:
                    running_hours = 1
                cost = running_hours * EC2_COST_PER_HOUR
                total_cost += cost
                print("  EC2 ID: " + instance["InstanceId"])
                print("  Hours Running: " + str(running_hours))
                print("  Cost: $" + str(round(cost, 4)) + "\n")
    return total_cost

def calculate_s3_cost():
    print("Calculating S3 Cost...\n")
    response = s3.list_buckets()
    total_size_gb = 0
    for bucket in response["Buckets"]:
        objects = s3.list_objects(Bucket=bucket["Name"])
        for obj in objects.get("Contents", []):
            total_size_gb += obj["Size"] / (1024 * 1024 * 1024)
    cost = total_size_gb * S3_COST_PER_GB
    print("  Total S3 Size: " + str(round(total_size_gb, 4)) + " GB")
    print("  Cost: $" + str(round(cost, 4)) + "\n")
    return cost

def total_cost_report():
    print("=" * 40)
    print("   AWS COST REPORT")
    print("=" * 40 + "\n")
    ec2_cost = calculate_ec2_cost()
    s3_cost = calculate_s3_cost()
    total = ec2_cost + s3_cost
    print("=" * 40)
    print("EC2 Total Cost  : $" + str(round(ec2_cost, 4)))
    print("S3 Total Cost   : $" + str(round(s3_cost, 4)))
    print("GRAND TOTAL     : $" + str(round(total, 4)))
    print("=" * 40)
    return total

total_cost_report()