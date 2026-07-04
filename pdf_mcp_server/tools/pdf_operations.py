from __future__ import annotations

from typing import List

from pypdf import PdfReader, PdfWriter

from .shared import WORKSPACE, _ensure_pdf, _safe_path


def extract_text(pdf_path: str, start_page: int = 1, end_page: int | None = None) -> str:
    """Extract text from a PDF. Pages are 1-based and inclusive."""
    path = _safe_path(pdf_path)
    _ensure_pdf(path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(str(path))
    total_pages = len(reader.pages)
    if end_page is None:
        end_page = total_pages

    start = max(1, start_page)
    end = min(total_pages, end_page)
    if start > end:
        raise ValueError("start_page must be less than or equal to end_page.")

    chunks: list[str] = []
    for page_number in range(start, end + 1):
        text = reader.pages[page_number - 1].extract_text() or ""
        chunks.append(f"\n--- Page {page_number} ---\n{text}")
    return "\n".join(chunks).strip()


def merge_pdfs(input_pdfs: List[str], output_pdf: str) -> str:
    """Merge multiple PDFs into one output PDF."""
    if not input_pdfs:
        raise ValueError("input_pdfs cannot be empty.")

    output_path = _safe_path(output_pdf)
    _ensure_pdf(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    writer = PdfWriter()
    for item in input_pdfs:
        input_path = _safe_path(item)
        _ensure_pdf(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"PDF not found: {item}")
        reader = PdfReader(str(input_path))
        for page in reader.pages:
            writer.add_page(page)

    with output_path.open("wb") as f:
        writer.write(f)

    return f"Merged {len(input_pdfs)} PDFs into {output_pdf}"


def split_pdf(pdf_path: str, output_prefix: str) -> List[str]:
    """Split one PDF into separate single-page PDFs."""
    path = _safe_path(pdf_path)
    _ensure_pdf(path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    output_prefix_path = _safe_path(output_prefix)
    output_prefix_path.parent.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(str(path))
    outputs: list[str] = []

    for index, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        out_path = output_prefix_path.parent / f"{output_prefix_path.name}_page_{index}.pdf"
        with out_path.open("wb") as f:
            writer.write(f)
        outputs.append(str(out_path.relative_to(WORKSPACE)))

    return outputs


def select_pages(pdf_path: str, pages: List[int], output_pdf: str) -> str:
    """Create a new PDF with selected pages. Pages are 1-based."""
    path = _safe_path(pdf_path)
    output_path = _safe_path(output_pdf)
    _ensure_pdf(path)
    _ensure_pdf(output_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(str(path))
    writer = PdfWriter()
    total_pages = len(reader.pages)

    for page_number in pages:
        if page_number < 1 or page_number > total_pages:
            raise ValueError(f"Invalid page number {page_number}. PDF has {total_pages} pages.")
        writer.add_page(reader.pages[page_number - 1])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as f:
        writer.write(f)

    return f"Created {output_pdf} with {len(pages)} selected pages."


def rotate_pages(pdf_path: str, output_pdf: str, pages: List[int], degrees: int = 90) -> str:
    """Rotate selected pages and save as a new PDF. Pages are 1-based."""
    if degrees not in (90, 180, 270, -90, -180, -270):
        raise ValueError("degrees must be one of 90, 180, 270, -90, -180, -270.")

    path = _safe_path(pdf_path)
    output_path = _safe_path(output_pdf)
    _ensure_pdf(path)
    _ensure_pdf(output_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(str(path))
    writer = PdfWriter()
    pages_to_rotate = set(pages)

    for index, page in enumerate(reader.pages, start=1):
        if index in pages_to_rotate:
            page.rotate(degrees)
        writer.add_page(page)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as f:
        writer.write(f)

    return f"Saved rotated PDF as {output_pdf}."


def optimize_pdf_basic(pdf_path: str, output_pdf: str) -> str:
    """Basic PDF optimization by compressing content streams where possible."""
    path = _safe_path(pdf_path)
    output_path = _safe_path(output_pdf)
    _ensure_pdf(path)
    _ensure_pdf(output_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(str(path))
    writer = PdfWriter()

    for page in reader.pages:
        try:
            page.compress_content_streams()
        except Exception:
            pass
        writer.add_page(page)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as f:
        writer.write(f)

    before = path.stat().st_size
    after = output_path.stat().st_size
    return f"Saved optimized PDF as {output_pdf}. Size: {before} bytes -> {after} bytes."


def register_pdf_operations(mcp):
    mcp.tool()(extract_text)
    mcp.tool()(merge_pdfs)
    mcp.tool()(split_pdf)
    mcp.tool()(select_pages)
    mcp.tool()(rotate_pages)
    mcp.tool()(optimize_pdf_basic)
