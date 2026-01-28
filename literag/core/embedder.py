from sentence_transformers import SentenceTransformer
from literag.core.chunker import Chunk
from literag.utils.config import config
from dataclasses import dataclass


@dataclass
class EmbeddedChunk:
    id: str
    text: str
    page_number: int
    chunk_index: int
    embedding: list[float]


class Embedder:
    def __init__(self):
        self.model = None
    
    def load_model(self):
        """Load the embedding model (lazy loading)."""
        if self.model is None:
            self.model = SentenceTransformer(config.EMBEDDING_MODEL)
        return self.model
    
    def embed_chunks(
        self, 
        chunks: list[Chunk], 
        progress_callback: callable = None
    ) -> list[EmbeddedChunk]:
        """Generate embeddings for a list of chunks."""
        model = self.load_model()
        embedded_chunks = []
        total = len(chunks)
        
        # Process in batches
        for i in range(0, total, config.BATCH_SIZE):
            batch = chunks[i:i + config.BATCH_SIZE]
            texts = [chunk.text for chunk in batch]
            
            # Generate embeddings
            embeddings = model.encode(texts, show_progress_bar=False)
            
            for chunk, embedding in zip(batch, embeddings):
                embedded_chunks.append(EmbeddedChunk(
                    id=chunk.id,
                    text=chunk.text,
                    page_number=chunk.page_number,
                    chunk_index=chunk.chunk_index,
                    embedding=embedding.tolist()
                ))
            
            if progress_callback:
                progress_callback(len(embedded_chunks), total)
        
        return embedded_chunks


# Singleton instance
embedder = Embedder()
