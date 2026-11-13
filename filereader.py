from pathlib import Path
from typing import List

from langchain_core.documents import Document
from pypdf import PdfReader


def load_pdf_pages(pdf_path: str | Path) -> List[Document]:
    """Read a PDF file page by page and return a list of LangChain Documents (one per page)."""
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    reader = PdfReader(str(path))
    docs: List[Document] = []

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        metadata = {"source": str(path), "page": page_num}
        docs.append(Document(page_content=text, metadata=metadata))

    return docs


def load_multiple_pdfs(pdf_paths: List[str | Path]) -> List[Document]:
    """Read multiple PDF files page by page and return a list of LangChain Documents."""
    all_docs: List[Document] = []
    for path in pdf_paths:
        all_docs.extend(load_pdf_pages(path))
    return all_docs
