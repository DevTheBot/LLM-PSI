from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    UPLOAD_DIR: str = "uploads"
    PERSIST_DIR: str = "chroma_db"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K: int = 3
    HF_API_TOKEN: str = ""
    LLM_API_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
