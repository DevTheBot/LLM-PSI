# RAG LLM

A Retrieval-Augmented Generation (RAG) pipeline using FastAPI, supporting document upload, semantic search, and querying with different LLM providers.

---

## 1. Setup and Installation

### Prerequisites
- Python 3.11+
- `pip` (Python package manager)
- (Optional) [Anaconda](https://www.anaconda.com/products/distribution) for environment management

### Installation
1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd RAG-llm
   ```
2. **Create and activate a virtual environment (recommended):**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install --upgrade pip
   pip install --upgrade --upgrade-strategy eager -r requirements.txt
   ```

4. **(Optional) Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in any required secrets or API keys.

---

## 2. API Usage and Testing Guidelines

### Running the API
Start the FastAPI server with:
```sh
uvicorn main:app --reload
```
- The API will be available at `http://localhost:8000`.
- Interactive docs: `http://localhost:8000/docs`

### Endpoints
- `POST /upload` — Upload a document (PDF, DOCX, TXT)
  - **Form field:** `file` (the document to upload)
  - **Response:** `{ "document_id": ..., "status": "processed", "filename": ... }`

- `POST /query` — Query the uploaded documents
  - **Body:** `{ "question": "..." }`
  - **Response:** `{ "answer": "...", "sources": [ ... ] }`

#### Example: Upload a PDF
```sh
curl -F "file=@tests/test.pdf" http://localhost:8000/upload
```

#### Example: Query
```sh
curl -X POST -H "Content-Type: application/json" \
     -d '{"question": "What is this document about?"}' \
     http://localhost:8000/query
```

### Running Tests
- Place a sample `test.pdf` in the `tests/` directory.
- Run all tests with:
  ```sh
  pytest tests/
  ```
- The test suite includes:
  - Import test (always runs)
  - Integration tests for upload and query (run only if dependencies are compatible)

---

## 3. Configuration: Using Different LLM Providers

The LLM provider and related settings are managed in `config.py`.

### Example: Switching Providers
Edit `config.py` to set your desired provider and credentials. For example:
```python
LLM_PROVIDER = "openai"  # or "azure", "huggingface", etc.
OPENAI_API_KEY = "sk-..."
# Add other provider-specific settings as needed
```

### Supported Providers
- **OpenAI**: Set `LLM_PROVIDER = "openai"` and provide `OPENAI_API_KEY`.
- **Azure OpenAI**: Set `LLM_PROVIDER = "azure"` and provide Azure credentials.
- **HuggingFace**: Set `LLM_PROVIDER = "huggingface"` and provide model details.
- **Others**: Extend `config.py` and the pipeline as needed.

### Environment Variables
You can also use a `.env` file to store sensitive keys and load them in `config.py` using `python-dotenv`.

---

## 4. Troubleshooting
- If you see errors about `TestClient` or `httpx`, ensure all dependencies are up to date and compatible.
- For integration tests, make sure `test.pdf` exists in the `tests/` directory.
- For LLM provider issues, double-check your API keys and config settings.

---

## 5. License
MIT License