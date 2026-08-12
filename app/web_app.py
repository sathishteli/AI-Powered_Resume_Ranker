"""
Flask web application for the AI-Powered Resume Ranker.

Allows users to:
1. Enter a job description.
2. Upload multiple PDF resumes.
3. Extract candidate names.
4. Rank candidates using NLP and TF-IDF.
5. View matched and missing skills.
6. View candidate ranking insights.
7. Download HR evaluation reports.
"""

import os
import tempfile

from flask import (
    Flask,
    render_template,
    request,
    session,
    send_file,
)

from io import BytesIO

from app.ranker import rank_resume

from app.resume_parser import (
    extract_candidate_name,
    extract_text_from_pdf,
)

from app.report_generator import generate_hr_report
from app.pdf_report_generator import generate_pdf_report


app = Flask(__name__)

# --------------------------------------------------
# Application configuration
# --------------------------------------------------

app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "ai-resume-ranker-development-key",
)

# Maximum total HTTP request size: 10 MB
app.config["MAX_CONTENT_LENGTH"] = (
    10 * 1024 * 1024
)

# Maximum number of resume files per request.
MAX_RESUME_FILES = 10

# Maximum size of one individual PDF.
MAX_RESUME_SIZE = 5 * 1024 * 1024


# ==================================================
# ERROR HANDLERS
# ==================================================

@app.errorhandler(413)
def request_too_large(error):
    """
    Handle uploads that exceed MAX_CONTENT_LENGTH.
    """

    return render_template(
        "index.html",
        results=[],
        error=(
            "The upload is too large. "
            "Please keep the total upload size below 10 MB."
        ),
        job_description="",
    ), 413


# ==================================================
# MAIN PAGE
# ==================================================

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Display the resume ranking interface
    and process submissions.
    """

    results = []
    error = None
    job_description = ""

    # ==================================================
    # PROCESS POST REQUEST
    # ==================================================

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

        # Prevent extremely large job descriptions.
        if len(job_description) > 100_000:

            error = (
                "Job description is too long. "
                "Please keep it below 100,000 characters."
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
        # Validate number of files
        # --------------------------------------------------

        if not uploaded_files:

            error = (
                "No resumes were uploaded. "
                "Please select one or more PDF files."
            )

            print("ERROR:", error)

            return render_template(
                "index.html",
                results=results,
                error=error,
                job_description=job_description,
            )

        if len(uploaded_files) > MAX_RESUME_FILES:

            error = (
                f"Too many resumes were uploaded. "
                f"Please upload no more than "
                f"{MAX_RESUME_FILES} PDF files at a time."
            )

            print("ERROR:", error)

            return render_template(
                "index.html",
                results=results,
                error=error,
                job_description=job_description,
            )

        # --------------------------------------------------
        # Validate file extensions
        # --------------------------------------------------

        invalid_files = []

        valid_files = []

        for uploaded_file in uploaded_files:

            if (
                not uploaded_file
                or not uploaded_file.filename
            ):
                continue

            filename = uploaded_file.filename

            if not filename.lower().endswith(".pdf"):

                invalid_files.append(filename)

            else:

                valid_files.append(uploaded_file)

        print(
            "Valid PDF files:",
            len(valid_files),
        )

        # --------------------------------------------------
        # Reject non-PDF files
        # --------------------------------------------------

        if invalid_files:

            invalid_names = ", ".join(
                invalid_files
            )

            error = (
                "Only PDF resumes are supported. "
                f"Invalid file(s): {invalid_names}"
            )

            print("ERROR:", error)

            return render_template(
                "index.html",
                results=results,
                error=error,
                job_description=job_description,
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

        # ==================================================
        # PROCESS EACH RESUME
        # ==================================================

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

                uploaded_file.save(
                    temp_path
                )

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

                if file_size > MAX_RESUME_SIZE:

                    raise ValueError(
                        "PDF exceeds the maximum "
                        "allowed size of 5 MB."
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
                # Extract candidate name
                # ------------------------------------------

                candidate_name = (
                    extract_candidate_name(
                        resume_text
                    )
                )

                print(
                    "Candidate name:",
                    candidate_name,
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
                    result[
                        "skill_match_score"
                    ],
                )

                print(
                    "Text score:",
                    result[
                        "text_similarity_score"
                    ],
                )

                print(
                    "Overall score:",
                    result[
                        "overall_score"
                    ],
                )

                # ------------------------------------------
                # Store candidate information
                # ------------------------------------------

                result["candidate_name"] = (
                    candidate_name
                )

                result["resume_file"] = (
                    uploaded_file.filename
                )

                results.append(
                    result
                )

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
                # Remove temporary file
                # ------------------------------------------

                if (
                    temp_path
                    and os.path.exists(
                        temp_path
                    )
                ):

                    try:

                        os.remove(
                            temp_path
                        )

                    except OSError as cleanup_error:

                        print(
                            "WARNING: Could not remove "
                            f"temporary file {temp_path}: "
                            f"{cleanup_error}"
                        )

        # ==================================================
        # SORT RESULTS
        # ==================================================

        results.sort(
            key=lambda candidate:
            candidate["overall_score"],
            reverse=True,
        )

        # ==================================================
        # ASSIGN RANKING
        # ==================================================

        for position, result in enumerate(
            results,
            start=1,
        ):

            result["rank"] = position

        # ==================================================
        # STORE RESULTS FOR REPORT DOWNLOAD
        # ==================================================

        if results:

            session["ranking_results"] = (
                results
            )

            session["job_description"] = (
                job_description
            )

        else:

            session.pop(
                "ranking_results",
                None,
            )

            session.pop(
                "job_description",
                None,
            )

            if error is None:

                error = (
                    "None of the uploaded resumes "
                    "could be processed successfully."
                )

        print(
            "\nSuccessfully processed:",
            len(results),
            "resume(s)",
        )

        print("=" * 70)

    # ==================================================
    # RENDER WEB PAGE
    # ==================================================

    return render_template(
        "index.html",
        results=results,
        error=error,
        job_description=job_description,
    )


# ======================================================
# DOWNLOAD HR REPORT
# ======================================================

@app.route("/download-report")
def download_report():
    """
    Generate and download the latest HR report.
    """

    results = session.get(
        "ranking_results",
        [],
    )

    job_description = session.get(
        "job_description",
        "",
    )

    if not results:

        return (
            "No ranking results available. "
            "Please rank resumes first.",
            400,
        )

    report = generate_hr_report(
        results,
        job_description,
    )

    report_file = BytesIO(
        report.encode("utf-8")
    )

    report_file.seek(0)

    return send_file(
        report_file,
        mimetype="text/plain",
        as_attachment=True,
        download_name="resume_ranking_report.txt",
    )


# ======================================================
# DOWNLOAD PDF HR REPORT
# ======================================================

@app.route("/download-pdf-report")
def download_pdf_report():
    """
    Generate and download the latest HR report as a PDF.
    """

    results = session.get(
        "ranking_results",
        [],
    )

    job_description = session.get(
        "job_description",
        "",
    )

    if not results:

        return (
            "No ranking results available. "
            "Please rank resumes first.",
            400,
        )

    pdf_file = generate_pdf_report(
        results,
        job_description,
    )

    return send_file(
        pdf_file,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="resume_ranking_report.pdf",
    )


# ======================================================
# APPLICATION ENTRY POINT
# ======================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000,
    )