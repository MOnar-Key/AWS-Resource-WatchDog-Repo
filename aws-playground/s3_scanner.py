import boto3
from datetime import datetime, timezone

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

def scan_unused_s3():
    print("Scanning S3 Buckets...\n")
    response = s3.list_buckets()
    buckets = response["Buckets"]
    empty_buckets = []
    used_buckets = []
    for bucket in buckets:
        bucket_name = bucket["Name"]
        objects = s3.list_objects(Bucket=bucket_name)
        contents = objects.get("Contents", [])
        total_size = 0
        for obj in contents:
            total_size += obj["Size"]
        bucket_info = {
            "name": bucket_name,
            "total_files": len(contents),
            "total_size_kb": total_size / 1024
        }
        if len(contents) == 0:
            empty_buckets.append(bucket_info)
        else:
            used_buckets.append(bucket_info)
    print("Total Buckets: " + str(len(buckets)))
    print("Empty Buckets: " + str(len(empty_buckets)))
    print("Used Buckets: " + str(len(used_buckets)) + "\n")
    if used_buckets:
        print("Used Buckets:")
        for b in used_buckets:
            print("  Name: " + b["name"] + " | Files: " + str(b["total_files"]) + " | Size: " + str(round(b["total_size_kb"], 2)) + " KB")
    if empty_buckets:
        print("\nEmpty Buckets (Delete Kar Sakte Ho):")
        for b in empty_buckets:
            print("  Name: " + b["name"])
    else:
        print("\nKoi Empty Bucket Nahi Mila!")
    return empty_buckets

scan_unused_s3()