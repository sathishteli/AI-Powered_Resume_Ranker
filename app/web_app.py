"""
Flask web application for the AI-Powered Resume Ranker.

Allows users to:
1. Enter a job description.
2. Upload multiple PDF resumes.
3. Rank candidates using NLP and TF-IDF.
4. View matched and missing skills.
"""

import os
import tempfile

from flask import Flask, render_template, request

from app.ranker import rank_resume
from app.resume_parser import extract_text_from_pdf


app = Flask(__name__)

# Maximum request size: 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Display the resume ranking interface and process submissions.
    """

    results = []
    error = None
    job_description = ""

    if request.method == "POST":

        # --------------------------------------------------
        # Get job description
        # --------------------------------------------------

        job_description = request.form.get(
            "job_description",
            "",
        ).strip()

        print("\n" + "=" * 70)
        print("NEW RESUME RANKING REQUEST")
        print("=" * 70)

        print(
            "Job description characters:",
            len(job_description),
        )

        # --------------------------------------------------
        # Validate job description
        # --------------------------------------------------

        if not job_description:

            error = (
                "Job description is empty. "
                "Please paste a job description."
            )

            print("ERROR:", error)

            return render_template(
                "index.html",
                results=results,
                error=error,
                job_description=job_description,
            )

        # --------------------------------------------------
        # Get uploaded files
        # --------------------------------------------------

        uploaded_files = request.files.getlist(
            "resumes"
        )

        print(
            "Uploaded files:",
            len(uploaded_files),
        )

        # --------------------------------------------------
        # Filter PDF files
        # --------------------------------------------------

        valid_files = []

        for uploaded_file in uploaded_files:

            if (
                uploaded_file
                and uploaded_file.filename
                and uploaded_file.filename.lower().endswith(".pdf")
            ):
                valid_files.append(uploaded_file)

        print(
            "Valid PDF files:",
            len(valid_files),
        )

        if not valid_files:

            error = (
                "No PDF resumes were uploaded. "
                "Please select one or more PDF files."
            )

            print("ERROR:", error)

            return render_template(
                "index.html",
                results=results,
                error=error,
                job_description=job_description,
            )

        # --------------------------------------------------
        # Process each resume
        # --------------------------------------------------

        for uploaded_file in valid_files:

            temp_path = None

            try:

                print(
                    "\nProcessing:",
                    uploaded_file.filename,
                )

                # ------------------------------------------
                # Create temporary PDF
                # ------------------------------------------

                with tempfile.NamedTemporaryFile(
                    suffix=".pdf",
                    delete=False,
                ) as temp_file:

                    temp_path = temp_file.name

                uploaded_file.save(temp_path)

                # ------------------------------------------
                # Verify uploaded file
                # ------------------------------------------

                file_size = os.path.getsize(
                    temp_path
                )

                print(
                    "Temporary file:",
                    temp_path,
                )

                print(
                    "File size:",
                    file_size,
                    "bytes",
                )

                if file_size == 0:

                    raise ValueError(
                        "Uploaded PDF is empty."
                    )

                # ------------------------------------------
                # Extract resume text
                # ------------------------------------------

                resume_text = (
                    extract_text_from_pdf(
                        temp_path
                    )
                )

                print(
                    "Extracted characters:",
                    len(resume_text),
                )

                if not resume_text.strip():

                    raise ValueError(
                        "No text could be extracted "
                        "from this PDF."
                    )

                # ------------------------------------------
                # Calculate ranking
                # ------------------------------------------

                result = rank_resume(
                    resume_text,
                    job_description,
                )

                print(
                    "Skill score:",
                    result["skill_match_score"],
                )

                print(
                    "Text score:",
                    result["text_similarity_score"],
                )

                print(
                    "Overall score:",
                    result["overall_score"],
                )

                # ------------------------------------------
                # Candidate information
                # ------------------------------------------

                candidate_name = os.path.splitext(
                    uploaded_file.filename
                )[0]

                result["candidate_name"] = (
                    candidate_name
                )

                result["resume_file"] = (
                    uploaded_file.filename
                )

                results.append(result)

            except Exception as exc:

                print(
                    "ERROR processing",
                    uploaded_file.filename,
                    ":",
                    repr(exc),
                )

                if error is None:

                    error = (
                        f"Could not process "
                        f"{uploaded_file.filename}: "
                        f"{exc}"
                    )

            finally:

                # ------------------------------------------
                # Delete temporary file
                # ------------------------------------------

                if (
                    temp_path
                    and os.path.exists(temp_path)
                ):

                    os.remove(temp_path)

        # --------------------------------------------------
        # Sort candidates
        # --------------------------------------------------

        results.sort(
            key=lambda candidate:
            candidate["overall_score"],
            reverse=True,
        )

        # --------------------------------------------------
        # Add ranking numbers
        # --------------------------------------------------

        for position, result in enumerate(
            results,
            start=1,
        ):

            result["rank"] = position

        print(
            "\nSuccessfully processed:",
            len(results),
            "resume(s)",
        )

        print("=" * 70)

    return render_template(
        "index.html",
        results=results,
        error=error,
        job_description=job_description,
    )


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000,
    )