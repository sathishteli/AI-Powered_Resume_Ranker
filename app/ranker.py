"""
Resume ranking module.

Combines:
1. Skill matching
2. TF-IDF cosine similarity
3. Candidate insights

to calculate an overall resume score and explain the result.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.skill_matcher import calculate_skill_match
from app.nlp_processor import extract_skills
from app.resume_parser import extract_text_from_pdf


def calculate_text_similarity(
    resume_text: str,
    job_description: str,
) -> float:
    """
    Calculate similarity between a resume and job description
    using TF-IDF and cosine similarity.

    Returns:
        float: Similarity score between 0 and 100.
    """

    if not resume_text.strip() or not job_description.strip():
        return 0.0

    documents = [
        resume_text,
        job_description,
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2],
    )[0][0]

    return round(similarity * 100, 2)


def calculate_overall_score(
    skill_match_score: float,
    text_similarity_score: float,
    skill_weight: float = 0.70,
    text_weight: float = 0.30,
) -> float:
    """
    Calculate the overall resume score.

    Default weighting:
        Skill matching = 70%
        Text similarity = 30%
    """

    if not 0 <= skill_match_score <= 100:
        raise ValueError(
            "Skill match score must be between 0 and 100."
        )

    if not 0 <= text_similarity_score <= 100:
        raise ValueError(
            "Text similarity score must be between 0 and 100."
        )

    if abs((skill_weight + text_weight) - 1.0) > 1e-9:
        raise ValueError(
            "Skill weight and text weight must add up to 1."
        )

    score = (
        skill_match_score * skill_weight
        + text_similarity_score * text_weight
    )

    return round(score, 2)


def get_recommendation(overall_score: float) -> str:
    """
    Convert the overall resume score into a
    human-readable recommendation.

    Score thresholds:
        >= 80: Highly Suitable
        >= 60: Suitable
        >= 40: Moderately Suitable
        < 40: Low Match
    """

    if not 0 <= overall_score <= 100:
        raise ValueError(
            "Overall score must be between 0 and 100."
        )

    if overall_score >= 80:
        return "Highly Suitable"

    if overall_score >= 60:
        return "Suitable"

    if overall_score >= 40:
        return "Moderately Suitable"

    return "Low Match"


def generate_candidate_insights(
    skill_match_score: float,
    text_similarity_score: float,
    matched_skills: list[str],
    missing_skills: list[str],
    recommendation: str,
) -> list[str]:
    """
    Generate deterministic, human-readable explanations
    for a candidate's ranking.

    The insights are based only on the existing ranking
    scores, matched skills, missing skills and recommendation.

    Returns:
        list[str]: Candidate ranking explanations.
    """

    insights = []

    # --------------------------------------------------
    # Skill match insight
    # --------------------------------------------------

    if skill_match_score >= 90:

        insights.append(
            f"Matches {skill_match_score:.0f}% of the "
            "required skills."
        )

    elif skill_match_score >= 70:

        insights.append(
            f"Matches {skill_match_score:.0f}% of the "
            "required skills."
        )

    elif skill_match_score >= 50:

        insights.append(
            f"Matches {skill_match_score:.0f}% of the "
            "required skills, with several gaps."
        )

    else:

        insights.append(
            f"Matches only {skill_match_score:.0f}% of the "
            "required skills."
        )

    # --------------------------------------------------
    # Missing skills insight
    # --------------------------------------------------

    if not missing_skills:

        insights.append(
            "No required skills are missing."
        )

    elif len(missing_skills) == 1:

        insights.append(
            "Missing 1 required skill."
        )

    else:

        insights.append(
            f"Missing {len(missing_skills)} "
            "required skills."
        )

    # --------------------------------------------------
    # Text similarity insight
    # --------------------------------------------------

    if text_similarity_score >= 60:

        insights.append(
            "Strong textual relevance to the "
            "job description."
        )

    elif text_similarity_score >= 40:

        insights.append(
            "Moderate textual relevance to the "
            "job description."
        )

    else:

        insights.append(
            "Low textual relevance to the "
            "job description."
        )

    # --------------------------------------------------
    # Recommendation insight
    # --------------------------------------------------

    if recommendation == "Highly Suitable":

        insights.append(
            "Overall profile is highly suitable "
            "for the role."
        )

    elif recommendation == "Suitable":

        insights.append(
            "Overall profile is suitable, "
            "with some skill gaps."
        )

    elif recommendation == "Moderately Suitable":

        insights.append(
            "Overall profile shows moderate suitability "
            "for the role."
        )

    else:

        insights.append(
            "Overall profile has significant gaps "
            "for this role."
        )

    return insights


def rank_resume(
    resume_text: str,
    job_description: str,
) -> dict:
    """
    Perform complete resume scoring.

    Steps:
        1. Extract candidate skills.
        2. Extract required job skills.
        3. Calculate skill match.
        4. Calculate TF-IDF similarity.
        5. Calculate score contributions.
        6. Calculate overall score.
        7. Generate recommendation.
        8. Generate candidate insights.
    """

    candidate_skills = extract_skills(
        resume_text
    )

    required_skills = extract_skills(
        job_description
    )

    skill_result = calculate_skill_match(
        candidate_skills,
        required_skills,
    )

    skill_score = skill_result["match_score"]

    text_score = calculate_text_similarity(
        resume_text,
        job_description,
    )

    skill_weight = 0.70
    text_weight = 0.30

    skill_contribution = round(
        skill_score * skill_weight,
        2,
    )

    text_contribution = round(
        text_score * text_weight,
        2,
    )

    overall_score = calculate_overall_score(
        skill_score,
        text_score,
        skill_weight=skill_weight,
        text_weight=text_weight,
    )

    recommendation = get_recommendation(
        overall_score
    )

    candidate_insights = generate_candidate_insights(
        skill_match_score=skill_score,
        text_similarity_score=text_score,
        matched_skills=skill_result["matched_skills"],
        missing_skills=skill_result["missing_skills"],
        recommendation=recommendation,
    )

    return {
        "candidate_skills": candidate_skills,
        "required_skills": required_skills,
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"],
        "skill_match_score": skill_score,
        "text_similarity_score": text_score,
        "overall_score": overall_score,
        "recommendation": recommendation,
        "candidate_insights": candidate_insights,
        "skill_weight": skill_weight,
        "text_weight": text_weight,
        "skill_contribution": skill_contribution,
        "text_contribution": text_contribution,
    }


if __name__ == "__main__":

    # --------------------------------------------------
    # Load sample resume
    # --------------------------------------------------

    sample_pdf = (
        "tests/sample_resumes/sample_resume.pdf"
    )

    resume_text = extract_text_from_pdf(
        sample_pdf
    )

    # --------------------------------------------------
    # Sample Job Description
    # --------------------------------------------------

    job_description = """
    We are looking for a Python Machine Learning Engineer.

    Required skills:
    Python, Scikit-learn, Pandas, NumPy,
    Machine Learning, Natural Language Processing,
    SQL, Flask, Git.

    Experience with Data Analysis, Data Preprocessing,
    Feature Engineering and Model Evaluation is preferred.
    """

    # --------------------------------------------------
    # Calculate Resume Score
    # --------------------------------------------------

    result = rank_resume(
        resume_text,
        job_description,
    )

    # --------------------------------------------------
    # Display Results
    # --------------------------------------------------

    print("=" * 60)
    print("AI-POWERED RESUME RANKER")
    print("=" * 60)

    print("\nCandidate Skills:")

    for skill in result["candidate_skills"]:
        print(f"- {skill}")

    print("\nRequired Skills:")

    for skill in result["required_skills"]:
        print(f"- {skill}")

    print("\nMatched Skills:")

    for skill in result["matched_skills"]:
        print(f"- {skill}")

    print("\nMissing Skills:")

    if result["missing_skills"]:

        for skill in result["missing_skills"]:
            print(f"- {skill}")

    else:

        print("- None")

    print("\n" + "-" * 60)

    print(
        f"Skill Match Score: "
        f"{result['skill_match_score']:.2f}%"
    )

    print(
        f"Text Similarity Score: "
        f"{result['text_similarity_score']:.2f}%"
    )

    print(
        f"Overall Resume Score: "
        f"{result['overall_score']:.2f}%"
    )

    print(
        f"Recommendation: "
        f"{result['recommendation']}"
    )

    print("\nCandidate Insights:")

    for insight in result["candidate_insights"]:
        print(f"- {insight}")

    print("-" * 60)