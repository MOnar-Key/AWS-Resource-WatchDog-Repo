import boto3
from datetime import datetime, timezone

ec2 = boto3.client(
    "ec2",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

def scan_idle_ec2():
    print("Scanning EC2 Instances...\n")
    response = ec2.describe_instances()
    idle_instances = []
    running_instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            state = instance["State"]["Name"]
            instance_type = instance["InstanceType"]
            launch_time = instance["LaunchTime"]
            now = datetime.now(timezone.utc)
            running_hours = (now - launch_time).seconds // 3600
            instance_info = {
                "id": instance_id,
                "state": state,
                "type": instance_type,
                "running_hours": running_hours
            }
            if state == "running":
                running_instances.append(instance_info)
                if running_hours >= 1:
                    idle_instances.append(instance_info)
    print("Total Running Instances: " + str(len(running_instances)))
    print("Idle Instances: " + str(len(idle_instances)) + "\n")
    if running_instances:
        print("Running Instances:")
        for inst in running_instances:
            print("  ID: " + inst["id"] + " | Type: " + inst["type"] + " | Hours: " + str(inst["running_hours"]))
    if idle_instances:
        print("\nIdle Instances Found:")
        for inst in idle_instances:
            print("  ID: " + inst["id"] + " | Type: " + inst["type"])
    else:
        print("\nKoi Idle Instance Nahi Mila!")
    return idle_instances

scan_idle_ec2()