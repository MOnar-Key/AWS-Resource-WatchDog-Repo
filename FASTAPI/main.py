import boto3
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI()
Instrumentator().instrument(app).expose(app)
def get_client(service):
    return boto3.client(
        service,
        endpoint_url="http://localhost:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1"
    )

@app.get("/")
def home():
    return {"message": "AWS Cost Optimizer API Running!"}

@app.get("/ec2")
def get_ec2():
    ec2 = get_client("ec2")
    response = ec2.describe_instances()
    instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            launch_time = instance["LaunchTime"]
            now = datetime.now(timezone.utc)
            running_hours = (now - launch_time).seconds // 3600
            instances.append({
                "id": instance["InstanceId"],
                "state": instance["State"]["Name"],
                "type": instance["InstanceType"],
                "running_hours": running_hours,
                "cost": round(running_hours * 0.0116, 4)
            })
    return {"instances": instances}

@app.get("/s3")
def get_s3():
    s3 = get_client("s3")
    buckets = s3.list_buckets()["Buckets"]
    result = []
    for bucket in buckets:
        objects = s3.list_objects(Bucket=bucket["Name"]).get("Contents", [])
        size_gb = sum(obj["Size"] for obj in objects) / (1024 * 1024 * 1024)
        result.append({
            "name": bucket["Name"],
            "total_files": len(objects),
            "size_gb": round(size_gb, 4),
            "cost": round(size_gb * 0.023, 4)
        })
    return {"buckets": result}

@app.get("/cost")
def get_total_cost():
    ec2_data = get_ec2()
    s3_data = get_s3()
    ec2_total = sum(i["cost"] for i in ec2_data["instances"])
    s3_total = sum(b["cost"] for b in s3_data["buckets"])
    return {
        "ec2_total": round(ec2_total, 4),
        "s3_total": round(s3_total, 4),
        "grand_total": round(ec2_total + s3_total, 4)
    }