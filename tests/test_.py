import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient
from main import app
import pytest


client = TestClient(app)

def test_upload_and_query_pdf():
    # Upload the PDF
    with open("tests/test.pdf", "rb") as f:
        upload_response = client.post("/upload", files={"file": ("test.pdf", f, "application/pdf")})
    assert upload_response.status_code == 200
    upload_json = upload_response.json()
    assert "document_id" in upload_json
    assert upload_json["status"] == "processed"

    # Query the uploaded document
    query = {"question": "What is this document about?"}
    query_response = client.post("/query", json=query)
    assert query_response.status_code == 200
    query_json = query_response.json()
    assert "answer" in query_json
    assert "sources" in query_json
    assert upload_json["filename"] in query_json["sources"][0] or upload_json["document_id"] in query_json["sources"][0]

def test_query_out_of_scope():
    # Query something not in the document
    query = {"question": "What is spiderman's real name?"}
    query_response = client.post("/query", json=query)
    assert query_response.status_code == 200
    query_json = query_response.json()
    answer = query_json["answer"].lower()
    assert (
        "i don't know" in answer
        or "unknown" in answer
        or "not found" in answer
        or "no information" in answer
        or "not in the context" in answer
    )
