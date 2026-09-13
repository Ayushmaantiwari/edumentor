import re
import pymupdf


# ======================================================
# CLEAN PDF TEXT
# ======================================================

def clean_text(text: str) -> str:
    """
    Clean extracted PDF text before storing it in PostgreSQL.

    PostgreSQL TEXT fields cannot contain NUL (\x00) bytes.
    PDF extraction can occasionally produce NUL/control characters.

    This function:
    - Removes NUL bytes
    - Removes problematic control characters
    - Preserves newline, carriage return and tab
    - Preserves normal Unicode characters
    """

    if not text:
        return ""

    # Remove NUL bytes
    text = text.replace("\x00", "")

    # Remove problematic control characters while
    # preserving useful whitespace.
    cleaned_chars = []

    for char in text:

        code = ord(char)

        # Preserve newline, carriage return and tab
        if char in ("\n", "\r", "\t"):
            cleaned_chars.append(char)

        # Preserve normal printable Unicode characters
        elif code >= 32:
            cleaned_chars.append(char)

    return "".join(cleaned_chars)


# ======================================================
# EXTRACT TEXT FROM PDF
# ======================================================

def extract_text_from_pdf(file_path: str) -> list[dict]:
    """
    Extract text from every page of a PDF.

    Returns:

    [
        {
            "page_number": 1,
            "text": "..."
        },
        ...
    ]
    """

    pages = []

    # Open PDF
    pdf = pymupdf.open(file_path)

    try:

        # Process every page
        for page_number, page in enumerate(
            pdf,
            start=1
        ):

            # ------------------------------------------
            # Extract raw text
            # ------------------------------------------

            raw_text = page.get_text()

            # ------------------------------------------
            # Clean extracted text
            # ------------------------------------------

            cleaned_text = clean_text(
                raw_text
            )

            # ------------------------------------------
            # Store page
            # ------------------------------------------

            pages.append(
                {
                    "page_number": page_number,
                    "text": cleaned_text
                }
            )

    finally:

        # Always close the PDF
        pdf.close()

    return pages


# ======================================================
# CHUNK TEXT
# ======================================================

def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
) -> list[str]:
    """
    Split text into overlapping chunks.

    Default:
        chunk size = 1000 characters
        overlap = 200 characters
    """

    # Clean the text again before chunking.
    # This provides an additional safety layer.
    text = clean_text(text)

    chunks = []

    start = 0

    text_length = len(text)

    # ------------------------------------------
    # Validate configuration
    # ------------------------------------------

    if chunk_size <= 0:

        raise ValueError(
            "chunk_size must be greater than 0"
        )

    if overlap < 0:

        raise ValueError(
            "overlap cannot be negative"
        )

    if overlap >= chunk_size:

        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    # ------------------------------------------
    # Create overlapping chunks
    # ------------------------------------------

    while start < text_length:

        end = start + chunk_size

        chunk = text[
            start:end
        ].strip()

        if chunk:

            chunks.append(
                chunk
            )

        start += (
            chunk_size -
            overlap
        )

    return chunks