"""
Resume PDF parsing utilities.

This module extracts text and basic candidate information
from PDF resumes.
"""

from pathlib import Path

import pymupdf


def extract_text_from_pdf(path: str) -> str:
    """
    Extract all text from a PDF file.

    Parameters
    ----------
    path : str
        Path to the PDF resume.

    Returns
    -------
    str
        Extracted text from the PDF.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.

    ValueError
        If the path is invalid, the file is not a PDF,
        the file is empty, the PDF is corrupted, or no
        text can be extracted.
    """

    pdf_path = Path(path)

    # --------------------------------------------------
    # Check that file exists
    # --------------------------------------------------

    if not pdf_path.exists():

        raise FileNotFoundError(
            f"PDF file not found: {path}"
        )

    # --------------------------------------------------
    # Check that it is a file
    # --------------------------------------------------

    if not pdf_path.is_file():

        raise ValueError(
            f"Path is not a file: {path}"
        )

    # --------------------------------------------------
    # Check file extension
    # --------------------------------------------------

    if pdf_path.suffix.lower() != ".pdf":

        raise ValueError(
            f"Invalid file type. "
            f"Expected a PDF file: {path}"
        )

    # --------------------------------------------------
    # Check file size
    # --------------------------------------------------

    file_size = pdf_path.stat().st_size

    if file_size == 0:

        raise ValueError(
            f"PDF file is empty: {path}"
        )

    # --------------------------------------------------
    # Check PDF file signature
    # --------------------------------------------------

    try:

        with pdf_path.open(
            "rb"
        ) as file:

            header = file.read(5)

    except OSError as error:

        raise ValueError(
            f"Unable to read PDF file: {path}"
        ) from error

    if header != b"%PDF-":

        raise ValueError(
            f"Invalid PDF file: {path}"
        )

    # --------------------------------------------------
    # Extract PDF text
    # --------------------------------------------------

    extracted_text = []

    try:

        with pymupdf.open(
            pdf_path
        ) as document:

            if document.page_count == 0:

                raise ValueError(
                    f"PDF contains no pages: {path}"
                )

            for page in document:

                text = page.get_text()

                if text:

                    extracted_text.append(
                        text
                    )

    except ValueError:

        raise

    except Exception as error:

        raise ValueError(
            f"Unable to read PDF file: {path}"
        ) from error

    # --------------------------------------------------
    # Combine extracted text
    # --------------------------------------------------

    result = "\n".join(
        extracted_text
    ).strip()

    # --------------------------------------------------
    # Validate extracted text
    # --------------------------------------------------

    if not result:

        raise ValueError(
            "No text could be extracted "
            f"from PDF: {path}"
        )

    return result


def extract_candidate_name(
    resume_text: str,
) -> str:
    """
    Extract a candidate name from resume text.

    The current implementation assumes that the
    candidate's name appears near the beginning
    of the resume.
    """

    if not resume_text.strip():

        return "Unknown Candidate"

    lines = [
        line.strip()
        for line in resume_text.splitlines()
        if line.strip()
    ]

    if not lines:

        return "Unknown Candidate"

    ignored_headings = {
        "resume",
        "curriculum vitae",
        "cv",
        "professional summary",
        "summary",
        "objective",
        "technical skills",
        "skills",
        "education",
        "experience",
        "work experience",
        "projects",
        "certifications",
        "achievements",
        "contact",
    }

    for line in lines[:10]:

        cleaned = line.strip()
        lower_line = cleaned.lower()

        if lower_line in ignored_headings:
            continue

        # Ignore contact information
        if "@" in cleaned:
            continue

        if "http://" in lower_line:
            continue

        if "https://" in lower_line:
            continue

        if "linkedin" in lower_line:
            continue

        if "github" in lower_line:
            continue

        if "phone" in lower_line:
            continue

        if "email" in lower_line:
            continue

        # Names normally don't contain digits
        if any(
            char.isdigit()
            for char in cleaned
        ):
            continue

        words = cleaned.split()

        # Typical candidate name length
        if not 2 <= len(words) <= 5:
            continue

        if len(cleaned) > 60:
            continue

        if not any(
            char.isalpha()
            for char in cleaned
        ):
            continue

        return cleaned

    return "Unknown Candidate"


if __name__ == "__main__":

    sample_pdf = (
        "tests/sample_resumes/"
        "sample_resume.pdf"
    )

    resume_text = extract_text_from_pdf(
        sample_pdf
    )

    candidate_name = extract_candidate_name(
        resume_text
    )

    print("=" * 60)
    print("RESUME PARSER TEST")
    print("=" * 60)

    print(
        "\nCandidate Name:",
        candidate_name,
    )

    print(
        "\nCharacters Extracted:",
        len(resume_text),
    )