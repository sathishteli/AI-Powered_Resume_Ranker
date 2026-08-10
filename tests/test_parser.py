from pathlib import Path

import pytest

from app.resume_parser import extract_text_from_pdf


def test_missing_pdf():
    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf("tests/sample_resumes/missing.pdf")


def test_invalid_file_type(tmp_path: Path):
    text_file = tmp_path / "resume.txt"
    text_file.write_text("Sample resume")

    with pytest.raises(ValueError):
        extract_text_from_pdf(str(text_file))