from __future__ import annotations

from typing import List

from pypdf import PdfReader

from .shared import WORKSPACE, _ensure_pdf, _safe_path


def list_pdfs() -> List[str]:
    """List PDF files available in the workspace."""
    return sorted(str(p.relative_to(WORKSPACE)) for p in WORKSPACE.rglob("*.pdf"))


def pdf_info(pdf_path: str) -> dict:
    """Return basic information about a PDF file."""
    path = _safe_path(pdf_path)
    _ensure_pdf(path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(str(path))
    metadata = reader.metadata or {}
    return {
        "file": pdf_path,
        "pages": len(reader.pages),
        "title": metadata.get("/Title", ""),
        "author": metadata.get("/Author", ""),
        "subject": metadata.get("/Subject", ""),
        "creator": metadata.get("/Creator", ""),
        "producer": metadata.get("/Producer", ""),
        "encrypted": reader.is_encrypted,
    }


def register_workspace_tools(mcp):
    mcp.tool()(list_pdfs)
    mcp.tool()(pdf_info)
