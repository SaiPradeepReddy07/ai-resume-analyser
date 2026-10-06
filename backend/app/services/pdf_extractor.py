"""
PDF Extraction Service
Extracts plaintext from uploaded PDF resume binaries using PyMuPDF (fitz).
Provides thorough validation for file format, size limits, and corrupted/empty content.
"""

import io
from typing import Tuple
import pymupdf as fitz  # PyMuPDF
from app.services.text_cleaner import clean_text
from app.core.config import settings


class PDFExtractionError(Exception):
    """Custom exception raised when PDF parsing or validation fails."""
    pass


def validate_pdf_bytes(file_bytes: bytes, filename: str) -> None:
    """
    Validates uploaded file size and PDF magic bytes.
    Raises PDFExtractionError if invalid.
    """
    # 1. Check file size
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if len(file_bytes) > max_bytes:
        raise PDFExtractionError(
            f"File '{filename}' exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB."
        )

    # 2. Check for empty file
    if len(file_bytes) == 0:
        raise PDFExtractionError("Uploaded file is empty (0 bytes).")

    # 3. Check for PDF magic header (%PDF-)
    if not file_bytes.startswith(b"%PDF-"):
        raise PDFExtractionError(
            f"File '{filename}' does not appear to be a valid PDF document (missing PDF header signature)."
        )


def extract_text_from_pdf(file_bytes: bytes, filename: str = "resume.pdf") -> Tuple[str, int]:
    """
    Extracts and cleans text from PDF binary bytes.
    
    Returns:
        Tuple[str, int]: (cleaned_text, page_count)
        
    Raises:
        PDFExtractionError: If PDF cannot be opened, is encrypted, or contains no readable text.
    """
    validate_pdf_bytes(file_bytes, filename)

    try:
        # Open in-memory byte stream with PyMuPDF
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as exc:
        raise PDFExtractionError(f"Unable to parse PDF '{filename}': {str(exc)}") from exc

    try:
        if doc.is_encrypted:
            # Attempt to authenticate with empty password in case of standard permissions encryption
            authenticated = doc.authenticate("")
            if not authenticated:
                raise PDFExtractionError(f"PDF '{filename}' is password protected. Please upload an unlocked PDF.")

        page_count = doc.page_count
        if page_count == 0:
            raise PDFExtractionError(f"PDF '{filename}' contains 0 pages.")

        extracted_pages = []
        for page_num in range(page_count):
            page = doc.load_page(page_num)
            # "text" extraction preserves logical reading order and layout blocks
            page_text = page.get_text("text")
            if page_text:
                extracted_pages.append(page_text)

        full_raw_text = "\n\n".join(extracted_pages)
        cleaned = clean_text(full_raw_text)

        # Verify that document contains readable text (detect scanned image-only PDFs)
        if len(cleaned.strip()) < 40:
            raise PDFExtractionError(
                f"PDF '{filename}' appears to be empty or contains only scanned images without selectable text. "
                "Please upload a text-searchable PDF."
            )

        return cleaned, page_count

    finally:
        doc.close()
