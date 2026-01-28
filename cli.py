import click
from pathlib import Path

from literag.core.extractor import extract_pdf
from literag.core.chunker import create_chunks
from literag.core.embedder import embedder
from literag.core.uploader import uploader
from literag.dashboard.progress import dashboard, console
from literag.utils.config import config


@click.group()
def main():
    """LiteRAG - Local ingestion pipeline for RAG."""
    pass


@main.command()
@click.argument("pdf_path", type=click.Path(exists=True))
@click.option("--collection", "-c", default=None, help="Collection name (default: from .env)")
def ingest(pdf_path: str, collection: str):
    """Ingest a PDF into Qdrant."""
    collection_name = collection or config.COLLECTION_NAME
    pdf_name = Path(pdf_path).name
    
    try:
        # Start dashboard
        dashboard.start(pdf_name)
        
        # Step 1: Extract
        console.print("[bold]Step 1/4:[/bold] Extracting text from PDF...")
        pages = extract_pdf(pdf_path)
        dashboard.show_extraction_result(len(pages))
        
        # Step 2: Chunk
        console.print("[bold]Step 2/4:[/bold] Creating chunks...")
        doc_id = Path(pdf_path).stem
        chunks = create_chunks(pages, doc_id)
        dashboard.show_chunking_result(len(chunks))
        
        # Step 3: Embed
        console.print("[bold]Step 3/4:[/bold] Generating embeddings...")
        with dashboard.create_progress() as progress:
            task = progress.add_task("Embedding chunks", total=len(chunks))
            
            def embed_progress(current, total):
                progress.update(task, completed=current)
            
            embedded_chunks = embedder.embed_chunks(chunks, embed_progress)
        
        console.print(f"✅ Generated [bold green]{len(embedded_chunks)}[/bold green] embeddings\n")
        
        # Step 4: Upload
        console.print("[bold]Step 4/4:[/bold] Uploading to Qdrant...")
        uploader.create_collection(collection_name)
        
        with dashboard.create_progress() as progress:
            task = progress.add_task("Uploading chunks", total=len(embedded_chunks))
            
            def upload_progress(current, total):
                progress.update(task, completed=current)
            
            uploader.upload_chunks(embedded_chunks, collection_name, upload_progress)
        
        # Complete
        dashboard.show_complete(collection_name, len(embedded_chunks))
        
    except Exception as e:
        dashboard.show_error(str(e))
        raise click.Abort()


@main.command()
@click.option("--collection", "-c", default=None, help="Collection name")
def info(collection: str):
    """Show collection info."""
    collection_name = collection or config.COLLECTION_NAME
    
    try:
        info = uploader.get_collection_info(collection_name)
        console.print(f"\n[bold]Collection:[/bold] {collection_name}")
        console.print(f"[bold]Points:[/bold] {info.points_count}")
        console.print(f"[bold]Status:[/bold] {info.status}\n")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


if __name__ == "__main__":
    main()
