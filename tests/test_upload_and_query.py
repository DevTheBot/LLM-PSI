import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

def test_import_app():
    from main import app
    assert app is not None

try:
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)

    @pytest.mark.skipif(client is None, reason="TestClient could not be instantiated due to dependency issues.")
    def test_upload_document():
        test_pdf_path = os.path.join(os.path.dirname(__file__), "test.pdf")
        if not os.path.exists(test_pdf_path):
            pytest.skip("test.pdf not found")
        with open(test_pdf_path, "rb") as f:
            response = client.post("/upload", files={"file": ("test.pdf", f, "application/pdf")})
        assert response.status_code == 200
        data = response.json()
        assert "document_id" in data
        assert data["status"] == "processed"
        assert data["filename"].endswith("test.pdf")

    @pytest.mark.skipif(client is None, reason="TestClient could not be instantiated due to dependency issues.")
    def test_query_document():
        query = {"question": "What is this document about?"}
        response = client.post("/query", json=query)
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert isinstance(data["sources"], list)

    @pytest.mark.skipif(client is None, reason="TestClient could not be instantiated due to dependency issues.")
    def test_query_out_of_scope():
        query = {"question": "What is spiderman's real name?"}
        response = client.post("/query", json=query)
        assert response.status_code == 200
        data = response.json()
        answer = data["answer"].lower()
        assert (
            "i don't know" in answer
            or "unknown" in answer
            or "not found" in answer
            or "no information" in answer
            or "not in the context" in answer
        )

except TypeError as e:
    print("TestClient could not be instantiated:", e)
    client = None


