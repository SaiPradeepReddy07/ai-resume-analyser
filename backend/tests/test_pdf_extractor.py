"""
PDF Extractor and Text Cleaner Test Suite
Verifies validation checks, character sanitization, and PDF in-memory extraction.
"""

import pytest
import pymupdf as fitz
from app.services.text_cleaner import clean_text, tokenize_for_nlp
from app.services.pdf_extractor import (
    extract_text_from_pdf,
    validate_pdf_bytes,
    PDFExtractionError
)


def test_clean_text_normalizes_bullets_and_spacing():
    raw = "• Python  developer\n\n\n\u2022 Experience with  FastAPI\t\tand   Docker"
    cleaned = clean_text(raw)
    assert "•" not in cleaned
    assert "- Python developer" in cleaned
    assert "- Experience with FastAPI and Docker" in cleaned


def test_tokenize_preserves_special_tech_symbols():
    text = "Proficient in C++, C#, and .NET core with Python."
    tokenized = tokenize_for_nlp(text)
    assert "c++" in tokenized
    assert "c#" in tokenized
    assert ".net" in tokenized


def test_validate_pdf_rejects_empty():
    with pytest.raises(PDFExtractionError) as exc_info:
        validate_pdf_bytes(b"", "empty.pdf")
    assert "empty" in str(exc_info.value).lower()


def test_validate_pdf_rejects_invalid_magic_bytes():
    with pytest.raises(PDFExtractionError) as exc_info:
        validate_pdf_bytes(b"This is just a plain text file pretending to be pdf", "fake.pdf")
    assert "valid pdf document" in str(exc_info.value).lower()


def test_extract_text_from_valid_synthetic_pdf():
    # Build a small in-memory PDF using PyMuPDF
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text(
        (50, 72),
        "John Doe\nSoftware Engineer\nSkilled in Python, FastAPI, PostgreSQL, and Git."
    )
    pdf_bytes = doc.write()
    doc.close()

    extracted, pages = extract_text_from_pdf(pdf_bytes, filename="test_resume.pdf")
    assert pages == 1
    assert "John Doe" in extracted
    assert "FastAPI" in extracted
    assert "PostgreSQL" in extracted
