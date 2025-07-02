from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from config import settings
import requests

router = APIRouter(tags=["RAG Pipeline"])

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

rag_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""Answer using ONLY this context:
    
Context:
{context}

Question: {question}
Answer:"""
)

class QueryRequest(BaseModel):
    question: str
    top_k: int = settings.TOP_K

@router.post("/query")
def query_documents(request: QueryRequest):
    # Initialize vector DB
    try:
        vector_db = Chroma(
            persist_directory=settings.PERSIST_DIR,
            embedding_function=embeddings
        )
    except:
        raise HTTPException(500, "Vector database not initialized")
    
    # Retrieve relevant chunks
    results = vector_db.similarity_search(
        request.question,
        k=request.top_k
    )
    context = "\n\n".join([doc.page_content for doc in results])
    
    # Generate response with LLM
    prompt = rag_prompt.format(
        context=context,
        question=request.question
    )
    
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": settings.LLM_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(
        settings.LLM_API_URL,
        headers=headers,
        json=data
    )
    if response.status_code != 200:
        print("LLM API error:", response.status_code, response.text)
        raise HTTPException(502, f"LLM API error: {response.text}")

    result = response.json()
    if "choices" in result:
        answer = result["choices"][0]["message"]["content"]
    else:
        answer = result.get("error", {}).get("message", "Unknown error")
    
    return {
        "question": request.question,
        "answer": answer,
        "sources": [doc.metadata.get("source", "") for doc in results]
    }
