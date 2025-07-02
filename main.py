from fastapi import FastAPI
from document_ingestion import router as ingestion_router
from rag_pipeline import router as query_router

app = FastAPI(title="RAG System with BGE Embeddings")

app.include_router(ingestion_router)
app.include_router(query_router)

@app.get("/")
def health_check():
    return {
        "status": "active",
        "message": "FastAPI RAG system is running"
    }
