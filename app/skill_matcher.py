"""
Skill matching module for the AI-Powered Resume Ranker.

Compares candidate skills against the skills required
by a job description.
"""

from typing import Iterable


def normalize_skills(skills: Iterable[str]) -> set[str]:
    """
    Normalize a collection of skills.

    Parameters
    ----------
    skills : Iterable[str]
        Skills extracted from a resume or job description.

    Returns
    -------
    set[str]
        Normalized unique skills.
    """

    return {
        skill.strip().lower()
        for skill in skills
        if isinstance(skill, str) and skill.strip()
    }


def calculate_skill_match(
    candidate_skills: Iterable[str],
    required_skills: Iterable[str],
) -> dict:
    """
    Compare candidate skills with required job skills.

    Parameters
    ----------
    candidate_skills : Iterable[str]
        Skills found in the candidate resume.

    required_skills : Iterable[str]
        Skills required by the job description.

    Returns
    -------
    dict
        Matched skills, missing skills and match score.
    """

    candidate = normalize_skills(candidate_skills)
    required = normalize_skills(required_skills)

    if not required:
        return {
            "matched_skills": [],
            "missing_skills": [],
            "match_score": 0.0,
        }

    matched = sorted(candidate.intersection(required))
    missing = sorted(required.difference(candidate))

    score = (len(matched) / len(required)) * 100

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "match_score": round(score, 2),
    }


if __name__ == "__main__":

    candidate_skills = [
        "Python",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "NLP",
        "SQL",
        "Flask",
        "Git",
    ]

    required_skills = [
        "Python",
        "Scikit-learn",
        "Pandas",
        "NumPy",
        "Machine Learning",
        "NLP",
        "SQL",
        "Flask",
        "Git",
    ]

    result = calculate_skill_match(
        candidate_skills,
        required_skills,
    )

    print("=" * 60)
    print("SKILL MATCHING TEST")
    print("=" * 60)

    print("\nMatched Skills:")

    for skill in result["matched_skills"]:
        print(f"- {skill}")

    print("\nMissing Skills:")

    if result["missing_skills"]:
        for skill in result["missing_skills"]:
            print(f"- {skill}")
    else:
        print("- None")

    print(
        f"\nSkill Match Score: "
        f"{result['match_score']:.2f}%"
    )