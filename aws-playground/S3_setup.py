import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

# Bucket banana
def create_bucket():
    s3.create_bucket(Bucket="my-fake-bucket")
    print("✅ Bucket Created: my-fake-bucket")

# File upload karna
def upload_file():
    s3.put_object(
        Bucket="my-fake-bucket",
        Key="hello.txt",
        Body="Hello from LocalStack!"
    )
    print("✅ File Uploaded: hello.txt")

# Files list karna
def list_files():
    response = s3.list_objects(Bucket="my-fake-bucket")
    print("\n📋 Bucket mein files:")
    for obj in response.get("Contents", []):
        print(f"  → {obj['Key']}")

create_bucket()
upload_file()
list_files()