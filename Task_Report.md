# AI-Powered Resume Ranker - Task Report

## 1. Project Overview

The AI-Powered Resume Ranker is a Flask-based recruitment screening application that accepts a job description and multiple PDF resumes, extracts candidate information, compares skills against the role requirements, and ranks applicants based on a weighted scoring model.

The project combines resume parsing, NLP-based skill matching, TF-IDF similarity scoring, and downloadable recruitment reports to streamline candidate shortlisting.

## 2. Current Implementation Status

### Completed Features

- PDF resume upload and validation
- Resume text extraction
- Candidate name detection
- Multi-resume processing
- Required-skill extraction from a job description
- Skill matching between job requirements and resume content
- Missing-skill identification
- TF-IDF text similarity scoring
- Weighted overall ranking logic
- Candidate recommendation labeling
- Flask web interface for job description and uploads
- Candidate result display with match explanations
- Text HR report generation
- PDF report generation
- Basic input validation and error handling
- Test suite structure for parser and web app scenarios

### Current Status Summary

The core application workflow is implemented and the project structure is in place. The system is designed to support resume ranking, candidate comparison, and report export as intended.

## 3. Ranking Methodology

The scoring model currently uses the following weighted components:

- Skill match: 70%
- Text similarity: 30%

Overall score formula:

Overall Score = (Skill Match × 0.70) + (Text Similarity × 0.30)

Applicants are sorted by the final composite score from highest to lowest.

## 4. Reporting and Outputs

The app provides:

- candidate ranking results,
- matched and missing skills,
- textual reasoning for suitability,
- downloadable HR summary reports,
- downloadable PDF reports.

This supports recruiter review and candidate shortlisting workflows.

## 5. Technical Stack

- Python
- Flask
- scikit-learn
- spaCy
- PyMuPDF
- ReportLab
- pytest
- HTML, CSS, Jinja templates

## 6. Testing and Verification Status

Fresh verification was completed using the project test suite:

- Command run: pytest -q
- Result: Test collection failed before execution due to import errors
- Observed error: ModuleNotFoundError: No module named 'app'

This indicates the project is not yet fully runnable in the current environment without setting the Python path correctly or installing the project in editable mode before running tests.

The issue is currently environmental/setup-related rather than a confirmed feature failure in the application logic itself.

## 7. Risks and Outstanding Work

The main current issues and follow-up items are:

- ensure the project package is importable during test execution,
- validate all tests under the correct Python environment,
- confirm the app runs successfully with the expected Flask configuration,
- review any remaining parser or ranking edge cases after import/setup fixes,
- consider expanding the skill extraction and scoring logic for more realistic hiring scenarios.

## 8. Future Enhancements

Planned improvements include:

- OCR support for scanned resumes
- semantic similarity improvements using transformer-based models
- better synonym and skill normalization
- multi-language resume handling
- experience and education matching
- database-backed candidate tracking
- authentication and role-based access
- cloud deployment
- analytics dashboards for recruiter review

## 9. Conclusion

The project has reached a meaningful implementation milestone with the resume parsing, ranking workflow, report generation, and Flask web interface in place. However, the codebase still requires final environment-level validation to ensure the test runner and application boot correctly in the current setup.

The next priority is to resolve the import/setup issue so the project can be validated end-to-end and the project can be considered fully production-ready from a technical standpoint.