from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'FASTAPI'))
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AWS Cost Optimizer API Running!"}

@patch("boto3.client")
def test_ec2(mock_boto):
    mock_ec2 = MagicMock()
    mock_ec2.describe_instances.return_value = {"Reservations": []}
    mock_boto.return_value = mock_ec2
    response = client.get("/ec2")
    assert response.status_code == 200

@patch("boto3.client")
def test_s3(mock_boto):
    mock_s3 = MagicMock()
    mock_s3.list_buckets.return_value = {"Buckets": []}
    mock_boto.return_value = mock_s3
    response = client.get("/s3")
    assert response.status_code == 200

@patch("boto3.client")
def test_cost(mock_boto):
    mock_client = MagicMock()
    mock_client.describe_instances.return_value = {"Reservations": []}
    mock_client.list_buckets.return_value = {"Buckets": []}
    mock_boto.return_value = mock_client
    response = client.get("/cost")
    assert response.status_code == 200