"""
HR report generation module.

Creates a downloadable text report from resume ranking results.
"""

from datetime import datetime
from typing import Any


def generate_hr_report(
    results: list[dict[str, Any]],
    job_description: str,
) -> str:
    """
    Generate a human-readable HR evaluation report.

    Parameters
    ----------
    results : list[dict]
        Ranked resume results.

    job_description : str
        Job description used for ranking.

    Returns
    -------
    str
        Formatted HR report.
    """

    lines = []

    lines.append("=" * 80)
    lines.append("AI-POWERED RESUME RANKER")
    lines.append("HR CANDIDATE EVALUATION REPORT")
    lines.append("=" * 80)

    lines.append("")
    lines.append(
        f"Generated: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    lines.append("")
    lines.append("JOB DESCRIPTION")
    lines.append("-" * 80)
    lines.append(job_description.strip())

    lines.append("")
    lines.append("SUMMARY")
    lines.append("-" * 80)

    lines.append(
        f"Candidates evaluated: {len(results)}"
    )

    if results:

        average_score = sum(
            candidate["overall_score"]
            for candidate in results
        ) / len(results)

        lines.append(
            f"Average overall score: "
            f"{average_score:.2f}%"
        )

    lines.append("")
    lines.append("=" * 80)
    lines.append("RANKING SUMMARY")
    lines.append("=" * 80)

    for candidate in results:

        lines.append("")

        lines.append(
            f"#{candidate['rank']} "
            f"{candidate['candidate_name']}"
        )

        lines.append(
            f"Overall Score: "
            f"{candidate['overall_score']:.2f}%"
        )

        lines.append(
            f"Recommendation: "
            f"{candidate.get('recommendation', 'N/A')}"
        )

        lines.append(
            f"Skill Match: "
            f"{candidate['skill_match_score']:.2f}%"
        )

        lines.append(
            f"Text Similarity: "
            f"{candidate['text_similarity_score']:.2f}%"
        )

    lines.append("")
    lines.append("=" * 80)
    lines.append("DETAILED CANDIDATE EVALUATION")
    lines.append("=" * 80)

    for candidate in results:

        lines.append("")
        lines.append(
            f"RANK #{candidate['rank']}: "
            f"{candidate['candidate_name']}"
        )

        lines.append("-" * 80)

        lines.append(
            f"Resume File: "
            f"{candidate.get('resume_file', 'N/A')}"
        )

        lines.append(
            f"Recommendation: "
            f"{candidate.get('recommendation', 'N/A')}"
        )

        lines.append("")

        lines.append(
            f"Overall Score: "
            f"{candidate['overall_score']:.2f}%"
        )

        lines.append(
            f"Skill Match: "
            f"{candidate['skill_match_score']:.2f}%"
        )

        if "skill_contribution" in candidate:

            lines.append(
                f"Skill Contribution: "
                f"{candidate['skill_contribution']:.2f}"
            )

        lines.append(
            f"Text Similarity: "
            f"{candidate['text_similarity_score']:.2f}%"
        )

        if "text_contribution" in candidate:

            lines.append(
                f"Text Contribution: "
                f"{candidate['text_contribution']:.2f}"
            )

        # --------------------------------------------------
        # Candidate insights
        # --------------------------------------------------

        lines.append("")
        lines.append("WHY THIS CANDIDATE?")

        candidate_insights = candidate.get(
            "candidate_insights",
            [],
        )

        if candidate_insights:

            for insight in candidate_insights:
                lines.append(f"- {insight}")

        else:

            lines.append(
                "- No additional insights available."
            )

        # --------------------------------------------------
        # Matched skills
        # --------------------------------------------------

        lines.append("")
        lines.append("MATCHED SKILLS")

        matched_skills = candidate.get(
            "matched_skills",
            [],
        )

        if matched_skills:

            for skill in matched_skills:
                lines.append(f"- {skill}")

        else:

            lines.append("- None")

        # --------------------------------------------------
        # Missing skills
        # --------------------------------------------------

        lines.append("")
        lines.append("MISSING SKILLS")

        missing_skills = candidate.get(
            "missing_skills",
            [],
        )

        if missing_skills:

            for skill in missing_skills:
                lines.append(f"- {skill}")

        else:

            lines.append("- None")

        lines.append("")
        lines.append("=" * 80)

    lines.append("")
    lines.append("END OF REPORT")
    lines.append("=" * 80)

    return "\n".join(lines)