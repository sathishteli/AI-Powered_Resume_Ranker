from pathlib import Path

import pytest

from app.resume_parser import (
    extract_candidate_name,
    extract_text_from_pdf,
)

from app.ranker import (
    generate_candidate_insights,
    get_recommendation,
)


# ==================================================
# RESUME PARSER TESTS
# ==================================================

def test_missing_pdf():

    with pytest.raises(
        FileNotFoundError
    ):

        extract_text_from_pdf(
            "tests/sample_resumes/missing.pdf"
        )


def test_invalid_file_type(
    tmp_path: Path,
):

    text_file = (
        tmp_path / "resume.txt"
    )

    text_file.write_text(
        "Sample resume",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Invalid file type",
    ):

        extract_text_from_pdf(
            str(text_file)
        )


def test_empty_pdf_file(
    tmp_path: Path,
):

    empty_pdf = (
        tmp_path / "empty.pdf"
    )

    empty_pdf.write_bytes(
        b""
    )

    with pytest.raises(
        ValueError,
        match="empty",
    ):

        extract_text_from_pdf(
            str(empty_pdf)
        )


def test_invalid_pdf_signature(
    tmp_path: Path,
):

    fake_pdf = (
        tmp_path / "fake.pdf"
    )

    fake_pdf.write_bytes(
        b"This is not a PDF file."
    )

    with pytest.raises(
        ValueError,
        match="Invalid PDF file",
    ):

        extract_text_from_pdf(
            str(fake_pdf)
        )


def test_sample_resume_extracts_text():

    sample_pdf = (
        "tests/sample_resumes/"
        "sample_resume.pdf"
    )

    text = extract_text_from_pdf(
        sample_pdf
    )

    assert text.strip()
    assert len(text) > 100


def test_candidate_name_extraction():

    resume_text = """
    ALEX JOHNSON

    alex@example.com

    Python Machine Learning Engineer

    Skills:
    Python, SQL, Machine Learning
    """

    assert (
        extract_candidate_name(
            resume_text
        )
        == "ALEX JOHNSON"
    )


def test_empty_candidate_name():

    assert (
        extract_candidate_name("")
        == "Unknown Candidate"
    )


# ==================================================
# RECOMMENDATION TESTS
# ==================================================

def test_highly_suitable_recommendation():

    assert (
        get_recommendation(80)
        == "Highly Suitable"
    )

    assert (
        get_recommendation(95)
        == "Highly Suitable"
    )


def test_suitable_recommendation():

    assert (
        get_recommendation(60)
        == "Suitable"
    )

    assert (
        get_recommendation(79.99)
        == "Suitable"
    )


def test_moderately_suitable_recommendation():

    assert (
        get_recommendation(40)
        == "Moderately Suitable"
    )

    assert (
        get_recommendation(59.99)
        == "Moderately Suitable"
    )


def test_low_match_recommendation():

    assert (
        get_recommendation(0)
        == "Low Match"
    )

    assert (
        get_recommendation(39.99)
        == "Low Match"
    )


# ==================================================
# CANDIDATE INSIGHT TESTS
# ==================================================

def test_candidate_insights_for_strong_candidate():

    insights = generate_candidate_insights(
        skill_match_score=100,
        text_similarity_score=56.39,
        matched_skills=[
            "Python",
            "Machine Learning",
        ],
        missing_skills=[],
        recommendation="Highly Suitable",
    )

    assert len(insights) == 4

    assert (
        "Matches 100% of the required skills."
        in insights
    )

    assert (
        "No required skills are missing."
        in insights
    )

    assert (
        "Overall profile is highly suitable "
        "for the role."
        in insights
    )


def test_candidate_insights_for_low_match():

    insights = generate_candidate_insights(
        skill_match_score=24,
        text_similarity_score=11.37,
        matched_skills=[
            "Python",
        ],
        missing_skills=[
            "Machine Learning",
            "Pandas",
            "NumPy",
        ],
        recommendation="Low Match",
    )

    assert (
        "Matches only 24% of the required skills."
        in insights
    )

    assert (
        "Missing 3 required skills."
        in insights
    )

    assert (
        "Low textual relevance to the "
        "job description."
        in insights
    )

    assert (
        "Overall profile has significant gaps "
        "for this role."
        in insights
    )