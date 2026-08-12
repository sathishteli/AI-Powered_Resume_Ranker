from pathlib import Path

import pytest

from app.resume_parser import (
    extract_candidate_name,
    extract_text_from_pdf,
)

from app.ranker import (
    calculate_overall_score,
    calculate_text_similarity,
    generate_candidate_insights,
    get_recommendation,
    rank_resume,
)

from app.skill_matcher import (
    calculate_skill_match,
    normalize_skills,
)

from app.batch_ranker import (
    rank_multiple_resumes,
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
# SKILL MATCHING TESTS
# ==================================================


def test_normalize_skills():

    skills = [
        "Python",
        " PYTHON ",
        "Machine Learning",
        "",
        "   ",
        None,
    ]

    normalized = normalize_skills(
        skills
    )

    assert normalized == {
        "python",
        "machine learning",
    }


def test_full_skill_match():

    result = calculate_skill_match(
        candidate_skills=[
            "Python",
            "Pandas",
            "NumPy",
        ],
        required_skills=[
            "Python",
            "Pandas",
            "NumPy",
        ],
    )

    assert result["match_score"] == 100.0

    assert result["matched_skills"] == [
        "numpy",
        "pandas",
        "python",
    ]

    assert result["missing_skills"] == []


def test_partial_skill_match():

    result = calculate_skill_match(
        candidate_skills=[
            "Python",
            "Pandas",
        ],
        required_skills=[
            "Python",
            "Pandas",
            "NumPy",
            "SQL",
        ],
    )

    assert result["match_score"] == 50.0

    assert result["matched_skills"] == [
        "pandas",
        "python",
    ]

    assert result["missing_skills"] == [
        "numpy",
        "sql",
    ]


def test_no_skill_match():

    result = calculate_skill_match(
        candidate_skills=[
            "Java",
            "C++",
        ],
        required_skills=[
            "Python",
            "Pandas",
        ],
    )

    assert result["match_score"] == 0.0

    assert result["matched_skills"] == []

    assert result["missing_skills"] == [
        "pandas",
        "python",
    ]


def test_empty_required_skills():

    result = calculate_skill_match(
        candidate_skills=[
            "Python",
            "Pandas",
        ],
        required_skills=[],
    )

    assert result["match_score"] == 0.0

    assert result["matched_skills"] == []

    assert result["missing_skills"] == []


def test_skill_matching_is_case_insensitive():

    result = calculate_skill_match(
        candidate_skills=[
            "PYTHON",
            "pAnDaS",
        ],
        required_skills=[
            "python",
            "PANDAS",
        ],
    )

    assert result["match_score"] == 100.0


# ==================================================
# TEXT SIMILARITY TESTS
# ==================================================


def test_text_similarity_empty_resume():

    assert (
        calculate_text_similarity(
            "",
            "Python Machine Learning",
        )
        == 0.0
    )


def test_text_similarity_empty_job_description():

    assert (
        calculate_text_similarity(
            "Python Machine Learning",
            "",
        )
        == 0.0
    )


def test_text_similarity_identical_text():

    text = (
        "Python machine learning "
        "with pandas and numpy"
    )

    score = calculate_text_similarity(
        text,
        text,
    )

    assert score == 100.0


def test_text_similarity_unrelated_text():

    score = calculate_text_similarity(
        "Python machine learning",
        "Cooking recipes and kitchen equipment",
    )

    assert score == 0.0


def test_text_similarity_is_symmetric():

    resume_text = (
        "Python machine learning pandas"
    )

    job_description = (
        "Python machine learning SQL"
    )

    first = calculate_text_similarity(
        resume_text,
        job_description,
    )

    second = calculate_text_similarity(
        job_description,
        resume_text,
    )

    assert first == second


# ==================================================
# OVERALL SCORE TESTS
# ==================================================


def test_overall_score_default_weights():

    score = calculate_overall_score(
        100,
        50,
    )

    assert score == 85.0


def test_overall_score_known_value():

    score = calculate_overall_score(
        100,
        56.39,
    )

    assert score == 86.92


def test_overall_score_custom_weights():

    score = calculate_overall_score(
        80,
        60,
        skill_weight=0.60,
        text_weight=0.40,
    )

    assert score == 72.0


def test_overall_score_invalid_skill_score():

    with pytest.raises(
        ValueError,
        match="Skill match score",
    ):

        calculate_overall_score(
            -1,
            50,
        )


def test_overall_score_skill_score_above_100():

    with pytest.raises(
        ValueError,
        match="Skill match score",
    ):

        calculate_overall_score(
            101,
            50,
        )


def test_overall_score_invalid_text_score():

    with pytest.raises(
        ValueError,
        match="Text similarity score",
    ):

        calculate_overall_score(
            50,
            -1,
        )


def test_overall_score_text_score_above_100():

    with pytest.raises(
        ValueError,
        match="Text similarity score",
    ):

        calculate_overall_score(
            50,
            101,
        )


def test_overall_score_invalid_weights():

    with pytest.raises(
        ValueError,
        match="must add up to 1",
    ):

        calculate_overall_score(
            80,
            60,
            skill_weight=0.50,
            text_weight=0.30,
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


def test_recommendation_invalid_negative_score():

    with pytest.raises(
        ValueError,
        match="Overall score",
    ):

        get_recommendation(-1)


def test_recommendation_invalid_score_above_100():

    with pytest.raises(
        ValueError,
        match="Overall score",
    ):

        get_recommendation(101)


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


# ==================================================
# COMPLETE RANKING TESTS
# ==================================================


def test_rank_resume_result_structure():

    result = rank_resume(
        "Python Pandas NumPy Machine Learning SQL",
        "Python Pandas NumPy Machine Learning SQL",
    )

    expected_keys = {
        "candidate_skills",
        "required_skills",
        "matched_skills",
        "missing_skills",
        "skill_match_score",
        "text_similarity_score",
        "overall_score",
        "recommendation",
        "candidate_insights",
        "skill_weight",
        "text_weight",
        "skill_contribution",
        "text_contribution",
    }

    assert expected_keys.issubset(
        result.keys()
    )


def test_rank_resume_perfect_skill_match():

    result = rank_resume(
        (
            "Python Pandas NumPy "
            "Machine Learning SQL"
        ),
        (
            "Python Pandas NumPy "
            "Machine Learning SQL"
        ),
    )

    assert (
        result["skill_match_score"]
        == 100.0
    )

    assert (
        result["text_similarity_score"]
        == 100.0
    )

    assert (
        result["overall_score"]
        == 100.0
    )

    assert (
        result["recommendation"]
        == "Highly Suitable"
    )


def test_rank_resume_contributions():

    result = rank_resume(
        (
            "Python Pandas NumPy "
            "Machine Learning SQL"
        ),
        (
            "Python Pandas NumPy "
            "Machine Learning SQL"
        ),
    )

    assert (
        result["skill_weight"]
        == 0.70
    )

    assert (
        result["text_weight"]
        == 0.30
    )

    assert (
        result["skill_contribution"]
        == 70.0
    )

    assert (
        result["text_contribution"]
        == 30.0
    )


def test_sample_resume_regression():

    sample_pdf = (
        "tests/sample_resumes/"
        "sample_resume.pdf"
    )

    resume_text = extract_text_from_pdf(
        sample_pdf
    )

    job_description = (
        "Python Machine Learning Engineer "
        "with Python, Scikit-learn, Pandas, "
        "NumPy, Machine Learning, Natural "
        "Language Processing, SQL, Flask, Git, "
        "Data Analysis, Data Preprocessing, "
        "Feature Engineering and Model Evaluation"
    )

    result = rank_resume(
        resume_text,
        job_description,
    )

    assert (
        result["skill_match_score"]
        == 100.0
    )

    assert (
        result["text_similarity_score"]
        == 47.64
    )

    assert (
        result["overall_score"]
        == 84.29
    )

    assert (
        result["recommendation"]
        == "Highly Suitable"
    )


# ==================================================
# BATCH RANKING TESTS
# ==================================================


def test_batch_ranking_invalid_directory():

    with pytest.raises(
        FileNotFoundError,
        match="Resume directory not found",
    ):

        rank_multiple_resumes(
            "tests/does_not_exist",
            "Python Machine Learning",
        )


def test_batch_ranking_path_is_not_directory(
    tmp_path: Path,
):

    file_path = (
        tmp_path / "resume.pdf"
    )

    file_path.write_bytes(
        b"sample"
    )

    with pytest.raises(
        NotADirectoryError,
        match="not a directory",
    ):

        rank_multiple_resumes(
            str(file_path),
            "Python Machine Learning",
        )


def test_batch_ranking_empty_job_description(
    tmp_path: Path,
):

    with pytest.raises(
        ValueError,
        match="Job description cannot be empty",
    ):

        rank_multiple_resumes(
            str(tmp_path),
            "",
        )


def test_batch_ranking_empty_directory(
    tmp_path: Path,
):

    results = rank_multiple_resumes(
        str(tmp_path),
        "Python Machine Learning",
    )

    assert results == []


def test_batch_ranking_sample_resumes():

    results = rank_multiple_resumes(
        "resumes",
        (
            "We are looking for a Machine "
            "Learning Engineer to design, "
            "develop, and deploy machine "
            "learning solutions."
        ),
    )

    assert isinstance(
        results,
        list,
    )

    # The repository should contain PDF
    # resumes for the batch demonstration.
    assert len(results) >= 1

    # Results must be sorted from highest
    # overall score to lowest.
    scores = [
        candidate["overall_score"]
        for candidate in results
    ]

    assert scores == sorted(
        scores,
        reverse=True,
    )

    # Ranking numbers must be sequential.
    ranks = [
        candidate["rank"]
        for candidate in results
    ]

    assert ranks == list(
        range(
            1,
            len(results) + 1,
        )
    )