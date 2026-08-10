from pathlib import Path

from fastapi import UploadFile
from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {".pdf", ".txt"}


class DocumentExtractionError(Exception):
    """Raised when document text extraction fails."""


async def extract_text(file: UploadFile) -> str:
    """
    Extract text from a PDF or TXT UploadFile.

    Supported formats:
    - PDF
    - TXT
    """

    if not file.filename:
        raise DocumentExtractionError("Uploaded file has no filename.")

    extension = Path(file.filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise DocumentExtractionError(
            f"Unsupported file type: {extension}. "
            f"Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    try:
        file_bytes = await file.read()
    except Exception as exc:
        raise DocumentExtractionError(
            "Failed to read uploaded file."
        ) from exc

    if not file_bytes:
        raise DocumentExtractionError("Uploaded file is empty.")

    if extension == ".txt":
        return _extract_txt(file_bytes)

    if extension == ".pdf":
        return _extract_pdf(file_bytes)

    raise DocumentExtractionError(
        f"Unsupported file type: {extension}"
    )


def _extract_txt(file_bytes: bytes) -> str:
    """Decode a TXT file into text."""

    try:
        text = file_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise DocumentExtractionError(
            "TXT file must be UTF-8 encoded."
        ) from exc

    return _clean_text(text)


def _extract_pdf(file_bytes: bytes) -> str:
    """Extract text from all pages of a PDF."""

    try:
        from io import BytesIO

        reader = PdfReader(BytesIO(file_bytes))

        pages: list[str] = []

        for page in reader.pages:
            page_text = page.extract_text() or ""

            if page_text.strip():
                pages.append(page_text)

    except Exception as exc:
        raise DocumentExtractionError(
            "Failed to extract text from PDF."
        ) from exc

    if not pages:
        raise DocumentExtractionError(
            "No extractable text was found in the PDF."
        )

    return _clean_text("\n\n".join(pages))


def _clean_text(text: str) -> str:
    """Normalize basic whitespace while preserving paragraph boundaries."""

    lines = [line.rstrip() for line in text.splitlines()]

    cleaned_lines: list[str] = []
    previous_blank = False

    for line in lines:
        line = line.strip()

        if not line:
            if not previous_blank:
                cleaned_lines.append("")

            previous_blank = True
            continue

        cleaned_lines.append(line)
        previous_blank = False

    return "\n".join(cleaned_lines).strip()