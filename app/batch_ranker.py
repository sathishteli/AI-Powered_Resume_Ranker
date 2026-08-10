"""
Batch resume ranking module.

Ranks multiple PDF resumes against a single job description.
"""

from pathlib import Path

from app.ranker import rank_resume
from app.resume_parser import extract_text_from_pdf


def rank_multiple_resumes(
    resumes_directory: str,
    job_description: str,
) -> list[dict]:
    """
    Rank all PDF resumes in a directory.

    Parameters
    ----------
    resumes_directory : str
        Directory containing PDF resumes.

    job_description : str
        Job description text.

    Returns
    -------
    list[dict]
        Ranked candidate results.
    """

    resume_dir = Path(resumes_directory)

    if not resume_dir.exists():
        raise FileNotFoundError(
            f"Resume directory not found: {resumes_directory}"
        )

    pdf_files = sorted(resume_dir.glob("*.pdf"))

    if not pdf_files:
        return []

    ranked_candidates = []

    for pdf_file in pdf_files:

        try:
            resume_text = extract_text_from_pdf(
                str(pdf_file)
            )

            result = rank_resume(
                resume_text,
                job_description,
            )

            result["candidate_name"] = pdf_file.stem
            result["resume_file"] = pdf_file.name

            ranked_candidates.append(result)

        except Exception as error:

            print(
                f"Error processing {pdf_file.name}: {error}"
            )

    ranked_candidates.sort(
        key=lambda candidate: candidate["overall_score"],
        reverse=True,
    )

    for rank, candidate in enumerate(
        ranked_candidates,
        start=1,
    ):
        candidate["rank"] = rank

    return ranked_candidates


def print_ranking_table(
    ranked_candidates: list[dict],
) -> None:
    """
    Display ranked candidates in a readable table.
    """

    if not ranked_candidates:
        print("No resumes found.")
        return

    print("\n")
    print("=" * 90)
    print("RESUME RANKING RESULTS")
    print("=" * 90)

    print(
        f"{'Rank':<8}"
        f"{'Candidate':<25}"
        f"{'Skill Match':<18}"
        f"{'Text Similarity':<20}"
        f"{'Overall':<10}"
    )

    print("-" * 90)

    for candidate in ranked_candidates:

        print(
            f"{candidate['rank']:<8}"
            f"{candidate['candidate_name']:<25}"
            f"{candidate['skill_match_score']:.2f}%"
            f"{'':<12}"
            f"{candidate['text_similarity_score']:.2f}%"
            f"{'':<14}"
            f"{candidate['overall_score']:.2f}%"
        )

    print("=" * 90)


if __name__ == "__main__":

    # --------------------------------------------------
    # Configuration
    # --------------------------------------------------

    resumes_directory = "resumes"

    job_description_file = (
        "job_descriptions/"
        "machine_learning_engineer.txt"
    )

    # --------------------------------------------------
    # Load job description
    # --------------------------------------------------

    job_description_path = Path(
        job_description_file
    )

    if not job_description_path.exists():

        raise FileNotFoundError(
            "Job description file not found: "
            f"{job_description_file}"
        )

    job_description = (
        job_description_path
        .read_text(encoding="utf-8")
    )

    # --------------------------------------------------
    # Rank resumes
    # --------------------------------------------------

    ranked_candidates = rank_multiple_resumes(
        resumes_directory,
        job_description,
    )

    # --------------------------------------------------
    # Display results
    # --------------------------------------------------

    print("=" * 90)
    print("AI-POWERED RESUME RANKER")
    print("=" * 90)

    print(
        f"\nJob Description: "
        f"{job_description_path.name}"
    )

    print(
        f"Resumes Found: "
        f"{len(ranked_candidates)}"
    )

    print_ranking_table(
        ranked_candidates
    )

    # --------------------------------------------------
    # Display detailed results
    # --------------------------------------------------

    for candidate in ranked_candidates:

        print("\n" + "-" * 90)

        print(
            f"Rank #{candidate['rank']}: "
            f"{candidate['candidate_name']}"
        )

        print(
            f"Overall Score: "
            f"{candidate['overall_score']:.2f}%"
        )

        print(
            f"Skill Match: "
            f"{candidate['skill_match_score']:.2f}%"
        )

        print(
            f"Text Similarity: "
            f"{candidate['text_similarity_score']:.2f}%"
        )

        print("\nMatched Skills:")

        if candidate["matched_skills"]:

            for skill in candidate["matched_skills"]:
                print(f"- {skill}")

        else:
            print("- None")

        print("\nMissing Skills:")

        if candidate["missing_skills"]:

            for skill in candidate["missing_skills"]:
                print(f"- {skill}")

        else:
            print("- None")