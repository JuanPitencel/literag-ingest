from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, 
    Distance, 
    PointStruct,
    CollectionInfo
)
from literag.core.embedder import EmbeddedChunk
from literag.utils.config import config


class Uploader:
    def __init__(self):
        self.client = None
    
    def connect(self):
        """Connect to Qdrant Cloud."""
        if self.client is None:
            self.client = QdrantClient(
                url=config.QDRANT_URL,
                api_key=config.QDRANT_API_KEY
            )
        return self.client
    
    def create_collection(self, collection_name: str = None):
        """Create collection if it doesn't exist."""
        client = self.connect()
        name = collection_name or config.COLLECTION_NAME
        
        collections = client.get_collections().collections
        exists = any(c.name == name for c in collections)
        
        if not exists:
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=config.EMBEDDING_DIMENSION,
                    distance=Distance.COSINE
                )
            )
            return True
        return False
    
    def upload_chunks(
        self, 
        chunks: list[EmbeddedChunk], 
        collection_name: str = None,
        progress_callback: callable = None
    ) -> int:
        """Upload embedded chunks to Qdrant."""
        client = self.connect()
        name = collection_name or config.COLLECTION_NAME
        total = len(chunks)
        uploaded = 0
        
        # Upload in batches
        for i in range(0, total, config.BATCH_SIZE):
            batch = chunks[i:i + config.BATCH_SIZE]
            
            points = [
                PointStruct(
                    id=chunk.chunk_index,
                    vector=chunk.embedding,
                    payload={
                        "text": chunk.text,
                        "page_number": chunk.page_number,
                        "chunk_id": chunk.id
                    }
                )
                for chunk in batch
            ]
            
            client.upsert(
                collection_name=name,
                points=points
            )
            
            uploaded += len(batch)
            
            if progress_callback:
                progress_callback(uploaded, total)
        
        return uploaded
    
    def get_collection_info(self, collection_name: str = None) -> CollectionInfo:
        """Get collection info."""
        client = self.connect()
        name = collection_name or config.COLLECTION_NAME
        return client.get_collection(name)


# Singleton instance
uploader = Uploader()
