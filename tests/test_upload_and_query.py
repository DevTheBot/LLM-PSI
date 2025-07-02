import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload_endpoint():
    with open("tests/test.pdf", "rb") as f:
        response = client.post("/upload", files={"file": ("test.pdf", f, "application/pdf")})
    assert response.status_code == 200

def test_query_endpoint():
    response = client.post("/query", json={"question": "Test?"})
    assert response.status_code == 200
