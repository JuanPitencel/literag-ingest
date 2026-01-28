# LiteRAG Ingest

A local PDF processing pipeline for RAG (Retrieval-Augmented Generation) applications. Process documents locally and upload embeddings to a vector database without expensive cloud infrastructure.

## 🎯 The Problem

Most RAG tutorials show the "happy path" with small documents. In production, you face:
- Server memory limits when processing large PDFs
- Timeout issues on cheap hosting
- High costs for processing infrastructure

## 💡 The Solution

**Process locally, serve in the cloud.**

- Run the heavy PDF processing on your local machine
- Upload only the embeddings to Qdrant Cloud (free tier)
- Deploy a lightweight query server for pennies

## 🚀 Features

- 📄 Extract text from PDFs (supports 400+ pages)
- ✂️ Smart chunking with sentence boundary detection
- 🧠 Generate embeddings with sentence-transformers (local, free)
- ☁️ Upload to Qdrant Cloud
- 📊 Real-time progress dashboard with Rich

## 📦 Installation
```bash
git clone https://github.com/JuanPitencel/literag-ingest.git
cd literag-ingest
pip install -e .
```

## ⚙️ Configuration

Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
QDRANT_URL=https://your-cluster.cloud.qdrant.io:6333
QDRANT_API_KEY=your_api_key
COLLECTION_NAME=your_collection
```

## 📖 Usage

### CLI Commands

#### Ingest a PDF
```bash
python cli.py ingest <path-to-pdf>
```

Example with included sample document:
```bash
python cli.py ingest docs/toyota_corolla_cross.pdf
```

Example with your own document:
```bash
python cli.py ingest docs/your_document.pdf --collection my_collection
```

Output:
```
╭─────── 📄 Document Ingestion ────────╮
│ LiteRAG Ingest                       │
│                                      │
│ Processing: your_document.pdf        │
╰──────────────────────────────────────╯
Step 1/4: Extracting text from PDF...
✅ Extracted 468 pages

Step 2/4: Creating chunks...
✅ Created 476 chunks

Step 3/4: Generating embeddings...
  Embedding chunks ━━━━━━━━━━━━━━━━━━━━ 100% 0:00:34

Step 4/4: Uploading to Qdrant...
  Uploading chunks ━━━━━━━━━━━━━━━━━━━━ 100% 0:00:01

         ✅ Ingestion Complete         
┌──────────────┬──────────────────────┐
│ Collection   │ your_collection      │
│ Total chunks │ 476                  │
│ Status       │ Ready for queries    │
└──────────────┴──────────────────────┘
```

#### Check collection info
```bash
python cli.py info
```

Or for a specific collection:
```bash
python cli.py info --collection my_collection
```

### CLI Options

| Command | Option | Description |
|---------|--------|-------------|
| `ingest` | `<pdf_path>` | Path to the PDF file to process |
| `ingest` | `--collection, -c` | Collection name (default: from .env) |
| `info` | `--collection, -c` | Collection name to check |

## 📁 Project Structure
```
literag-ingest/
├── literag/
│   ├── core/
│   │   ├── extractor.py    # PDF text extraction
│   │   ├── chunker.py      # Text chunking
│   │   ├── embedder.py     # Embedding generation
│   │   └── uploader.py     # Qdrant upload
│   ├── dashboard/
│   │   └── progress.py     # Rich progress display
│   └── utils/
│       └── config.py       # Configuration
├── docs/
│   └── toyota_corolla_cross.pdf  # Sample document (replace with your own)
├── cli.py                  # Command line interface
├── pyproject.toml
├── .env.example
└── README.md
```

## 📂 Using Your Own Documents

The `docs/` folder contains a sample PDF (Toyota Corolla Cross Owner's Manual) used for the demo. You can replace it with any PDF you want to process:

1. Add your PDF to the `docs/` folder
2. Run the ingest command:
```bash
   python cli.py ingest docs/your_document.pdf --collection your_collection_name
```
3. Update the related projects to use your new collection

## 🏗️ Architecture
```
PDF Document
    │
    ▼
┌─────────────┐
│  Extractor  │  PyMuPDF - Extract text from pages
└─────────────┘
    │
    ▼
┌─────────────┐
│   Chunker   │  Split text respecting sentence boundaries
└─────────────┘
    │
    ▼
┌─────────────┐
│  Embedder   │  sentence-transformers (all-MiniLM-L6-v2)
└─────────────┘
    │
    ▼
┌─────────────┐
│  Uploader   │  Qdrant Cloud
└─────────────┘
```

## 🔧 Tech Stack

- **Python 3.10+**
- **PyMuPDF** - PDF processing
- **sentence-transformers** - Local embeddings (all-MiniLM-L6-v2, 384 dimensions)
- **Qdrant** - Vector database
- **Rich** - Terminal UI
- **Click** - CLI framework

## 📊 Performance

| Document Size | Pages | Chunks | Processing Time |
|--------------|-------|--------|-----------------|
| Toyota Manual | 468   | 476    | ~35 seconds     |

*Tested on Intel i5 with 8GB RAM, no GPU required*

## 🤝 Related Projects

This is part of a complete RAG system:

- **[ragquery-server](https://github.com/JuanPitencel/ragquery-server)** - Lightweight FastAPI server for queries
- **[toyota-corolla-cross-bot](https://github.com/JuanPitencel/toyota-corolla-cross-bot)** - Frontend React application

## 📄 License

MIT

## 👤 Author

**Juan Pitencel**
- GitHub: [@JuanPitencel](https://github.com/JuanPitencel)
