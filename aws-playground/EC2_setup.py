import boto3

# LocalStack EC2 client
ec2 = boto3.client(
    "ec2",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

# Create EC2 Instance 
def create_instance():
    response = ec2.run_instances(
        ImageId="ami-03cf127a",    # Fake AMI ID
        MinCount=1,
        MaxCount=2,
        InstanceType="t2.micro"
    )
    instances = response["Instances"]
    for instance in instances:
        print(f"✅ Instance Created! ID: {instance['InstanceId']}")
    return instances

# Instance List 
def list_instances():
    response = ec2.describe_instances()
    print("\n📋 Sare Instances:")
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            print(f"  → ID: {instance['InstanceId']} | State: {instance['State']['Name']}")

# Run EC2
create_instance()
list_instances()