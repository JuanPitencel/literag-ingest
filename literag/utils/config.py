import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "documents")
    
    # Embedding model
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    
    # Chunking settings
    CHUNK_SIZE: int = 500  # tokens aprox
    CHUNK_OVERLAP: int = 50
    
    # Batch settings
    BATCH_SIZE: int = 100

config = Config()
