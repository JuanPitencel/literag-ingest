import fitz  # PyMuPDF
from pathlib import Path
from dataclasses import dataclass


@dataclass
class PageContent:
    page_number: int
    text: str


def extract_pdf(pdf_path: str) -> list[PageContent]:
    """Extract text from each page of a PDF."""
    path = Path(pdf_path)
    
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    if not path.suffix.lower() == ".pdf":
        raise ValueError(f"File is not a PDF: {pdf_path}")
    
    pages = []
    
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text().strip()
            if text:  # Skip empty pages
                pages.append(PageContent(page_number=page_num, text=text))
    
    return pages
