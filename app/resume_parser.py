"""
Resume PDF Parser

Extracts text from PDF resumes using PyMuPDF.
"""

from pathlib import Path

import pymupdf


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from all pages of a PDF resume.

    Parameters
    ----------
    pdf_path : str
        Path to the PDF resume.

    Returns
    -------
    str
        Combined text extracted from the PDF.

    Raises
    ------
    FileNotFoundError
        If the PDF file does not exist.
    ValueError
        If the file is not a PDF.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("The uploaded file must be a PDF.")

    extracted_text = []

    with pymupdf.open(path) as document:
        for page in document:
            text = page.get_text()

            if text.strip():
                extracted_text.append(text.strip())

    return "\n".join(extracted_text)


if __name__ == "__main__":
    sample_pdf = "tests/sample_resumes/sample_resume.pdf"

    try:
        resume_text = extract_text_from_pdf(sample_pdf)

        print("=" * 60)
        print("RESUME TEXT EXTRACTION TEST")
        print("=" * 60)

        print(f"\nCharacters extracted: {len(resume_text)}")
        print("\nExtracted Text:\n")
        print(resume_text)

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")