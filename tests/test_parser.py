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

from app.ranker import (
    get_recommendation,
)


def test_highly_suitable_recommendation():
    assert get_recommendation(80) == "Highly Suitable"
    assert get_recommendation(95) == "Highly Suitable"


def test_suitable_recommendation():
    assert get_recommendation(60) == "Suitable"
    assert get_recommendation(79.99) == "Suitable"


def test_moderately_suitable_recommendation():
    assert get_recommendation(40) == "Moderately Suitable"
    assert get_recommendation(59.99) == "Moderately Suitable"


def test_low_match_recommendation():
    assert get_recommendation(0) == "Low Match"
    assert get_recommendation(39.99) == "Low Match"