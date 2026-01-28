from dataclasses import dataclass
from literag.core.extractor import PageContent
from literag.utils.config import config


@dataclass
class Chunk:
    id: str
    text: str
    page_number: int
    chunk_index: int


def split_into_sentences(text: str) -> list[str]:
    """Split text into sentences (simple approach)."""
    separators = [". ", "? ", "! ", ".\n", "?\n", "!\n"]
    sentences = [text]
    
    for sep in separators:
        new_sentences = []
        for s in sentences:
            parts = s.split(sep)
            for i, part in enumerate(parts):
                if i < len(parts) - 1:
                    new_sentences.append(part + sep.strip())
                else:
                    new_sentences.append(part)
        sentences = new_sentences
    
    return [s.strip() for s in sentences if s.strip()]


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into chunks respecting sentence boundaries."""
    sentences = split_into_sentences(text)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_length = len(sentence.split())
        
        if current_length + sentence_length > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            
            # Keep overlap
            overlap_words = []
            overlap_length = 0
            for s in reversed(current_chunk):
                s_len = len(s.split())
                if overlap_length + s_len <= overlap:
                    overlap_words.insert(0, s)
                    overlap_length += s_len
                else:
                    break
            
            current_chunk = overlap_words
            current_length = overlap_length
        
        current_chunk.append(sentence)
        current_length += sentence_length
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks


def create_chunks(pages: list[PageContent], doc_id: str = "doc") -> list[Chunk]:
    """Create chunks from extracted pages."""
    all_chunks = []
    chunk_counter = 0
    
    for page in pages:
        text_chunks = chunk_text(
            page.text,
            config.CHUNK_SIZE,
            config.CHUNK_OVERLAP
        )
        
        for chunk_text_content in text_chunks:
            all_chunks.append(Chunk(
                id=f"{doc_id}_chunk_{chunk_counter}",
                text=chunk_text_content,
                page_number=page.page_number,
                chunk_index=chunk_counter
            ))
            chunk_counter += 1
    
    return all_chunks
