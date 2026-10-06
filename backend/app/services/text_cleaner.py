"""
Text Cleaning and Normalization Service
Prepares raw extracted PDF text and job descriptions for NLP processing.
Handles unicode artifacts, irregular bullet points, whitespace, and preserves critical technical tokens.
"""

import re
import unicodedata


def clean_text(text: str) -> str:
    """
    Cleans raw document text:
    - Normalizes unicode characters (e.g. smart quotes, em-dashes, accented letters)
    - Replaces bullet points and non-standard list delimiters with standard dashes
    - Removes unprintable and control characters
    - Normalizes excessive whitespace and blank lines
    """
    if not text:
        return ""

    # Normalize unicode to NFKC (Compatibility Decomposition followed by Canonical Composition)
    normalized = unicodedata.normalize("NFKC", text)

    # Replace common bullet point glyphs with standard dash
    bullet_pattern = r"[\u2022\u2023\u25E6\u2043\u2219\u25AA\u25AB\u25CF\u25CB\u25A0\u25A1\u25C6\u25C7\u25B6\u27A4\u2713\u2714\u25B8]"
    normalized = re.sub(bullet_pattern, " - ", normalized)

    # Replace non-breaking spaces and tab sequences with standard space
    normalized = normalized.replace("\u00a0", " ").replace("\t", " ")

    # Remove non-printable control characters (keep standard newlines and returns)
    normalized = "".join(char for char in normalized if char == "\n" or char == "\r" or (char.isprintable() and ord(char) < 65536))

    # Normalize line breaks (convert CRLF to LF)
    normalized = re.sub(r"\r\n|\r", "\n", normalized)

    # Collapse multiple consecutive empty lines to maximum 2
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)

    # Collapse multiple consecutive inline spaces to a single space
    lines = [re.sub(r"[ ]{2,}", " ", line).strip() for line in normalized.split("\n")]
    cleaned = "\n".join(lines).strip()

    return cleaned


def tokenize_for_nlp(text: str) -> str:
    """
    Converts cleaned text into a tokenized string safe for NLP processing.
    Preserves programming tokens like c++, c#, and .net while removing noisy punctuation.
    """
    if not text:
        return ""

    t = text.lower()
    # Retain alphanumeric characters, whitespace, and technical symbols (+, #, ., -)
    t = re.sub(r"[^\w\s+#.-]", " ", t)
    # Collapse consecutive whitespace
    return re.sub(r"\s+", " ", t).strip()
