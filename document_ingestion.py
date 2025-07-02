from fastapi import APIRouter, UploadFile, File, HTTPException
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from config import settings
import os
import uuid

router = APIRouter(tags=["Document Ingestion"])

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.CHUNK_SIZE,
    chunk_overlap=settings.CHUNK_OVERLAP,
    length_function=len
)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Validate file type
    if not file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(400, "Unsupported file type")
    
    # Save file
    file_id = str(uuid.uuid4())
    file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}_{file.filename}")
    
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Load document with error handling
    try:
        if file.filename.lower().endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file.filename.lower().endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        elif file.filename.lower().endswith(".txt"):
            loader = TextLoader(file_path)
        
        document = loader.load()
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(500, f"Document loading failed: {str(e)}")
    
    # Split into chunks
    chunks = text_splitter.split_documents(document)
    
    # Store in vector DB
    try:
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=settings.PERSIST_DIR
        )
        vector_db.persist()
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(500, f"Vector storage failed: {str(e)}")
    
    return {
        "document_id": file_id,
        "filename": file.filename,
        "chunk_count": len(chunks),
        "status": "processed"
    }
