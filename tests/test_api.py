from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'FASTAPI'))
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_ec2():
    response = client.get("/ec2")
    assert response.status_code == 200

def test_s3():
    response = client.get("/s3")
    assert response.status_code == 200

def test_cost():
    response = client.get("/cost")
    assert response.status_code == 200