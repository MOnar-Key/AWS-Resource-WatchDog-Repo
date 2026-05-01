import boto3

# LocalStack se connect karne ka base setup
def get_client(service_name):
    return boto3.client(
        service_name,
        endpoint_url="http://localhost:4566",  # LocalStack URL
        aws_access_key_id="test",              # Fake credentials
        aws_secret_access_key="test",          # Fake credentials
        region_name="us-east-1"
    )

# Connection Test
def test_connection():
    try:
        s3 = get_client("s3")
        ec2 = get_client("ec2")
        cloudwatch = get_client("cloudwatch")
        
        print("✅ S3 Connected!")
        print("✅ EC2 Connected!")
        print("✅ CloudWatch Connected!")
        print("\n🎉 LocalStack se successfully connect ho gaye!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

test_connection()