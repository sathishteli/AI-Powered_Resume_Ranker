# AI-Powered Resume Ranker

A Flask-based resume screening application that compares uploaded PDF resumes against a job description, extracts candidate skills, and ranks applicants using a weighted combination of skill matching and text similarity.

The app is designed to help recruiters shortlist candidates faster by surfacing relevant experience, highlighting skill gaps, and generating downloadable HR reports.

## Overview

This project allows a recruiter to:

- paste or type a job description,
- upload multiple PDF resumes,
- extract text from each resume,
- detect a likely candidate name,
- compare candidate skills to required skills,
- score each resume with a weighted ranking model,
- review matched and missing skills,
- download a text or PDF summary report.

## Features

- Multi-resume PDF upload in a single request
- Job description validation and length checks
- PDF text extraction using PyMuPDF
- Candidate name detection from resume content
- Skill extraction with NLP heuristics and text normalization
- Skill match scoring against required role skills
- TF-IDF cosine similarity scoring against the job description
- Weighted overall score calculation
- Recommendation labels such as Highly Suitable, Suitable, and Low Match
- Human-readable candidate insights
- Downloadable HR reports in TXT and PDF formats
- Flask web interface with server-side session storage

## Tech Stack

- Python 3
- Flask
- scikit-learn
- spaCy
- PyMuPDF
- ReportLab
- pytest
- HTML, CSS, and Jinja templates

## Repository Structure

```text
AI-Powered_Resume_Ranker/
├── app.py
├── README.md
├── requirements.txt
├── Task_Report.md
├── app/
│   ├── __init__.py
│   ├── batch_ranker.py
│   ├── nlp_processor.py
│   ├── pdf_report_generator.py
│   ├── ranker.py
│   ├── report_generator.py
│   ├── resume_parser.py
│   ├── skill_matcher.py
│   └── web_app.py
├── data/
├── job_descriptions/
│   └── machine_learning_engineer.txt
├── models/
├── resumes/
├── tests/
│   ├── sample_resumes/
│   ├── test_parser.py
│   └── test_web_app.py
├── uploads/
└── app/static/
    ├── css/
    ├── js/
    └── style.css
```

## Installation

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

> The project includes the spaCy English model wheel in requirements.txt, so installation should resolve the core NLP dependencies in one step.

## Running the App

The app is created in [app/web_app.py](app/web_app.py), and the main Flask entry point is the `app` object defined there.

Start the app with:

```bash
python -m flask --app app.web_app run --debug
```

Or run it directly with:

```bash
python app/web_app.py
```

Then open the app in a browser:

```text
http://127.0.0.1:5000
```

## How Ranking Works

Each uploaded resume goes through this flow:

1. Extract text from the PDF.
2. Detect the candidate name from the extracted text.
3. Extract relevant skills from the resume and job description.
4. Compute a skill-match percentage.
5. Compute TF-IDF cosine similarity between the resume content and the job description.
6. Combine both scores using a weighted formula.
7. Sort candidates by overall score and assign a recommendation.

Default weights:

- Skill match: 70%
- Text similarity: 30%

## Report Generation

The app can generate:

- a plain-text recruitment report,
- a PDF HR evaluation report.

The generated reports include ranking information, candidate fit status, matched skills, missing skills, and recommendation details.

## Environment Variables

The app reads configuration from environment variables such as:

```bash
FLASK_SECRET_KEY
FLASK_DEBUG
FLASK_HOST
FLASK_PORT
MAX_CONTENT_LENGTH_MB
MAX_RESUME_FILES
MAX_RESUME_SIZE_MB
```

Default values are defined in [app/web_app.py](app/web_app.py).

## Running Tests

```bash
pytest
```

The test suite covers page loading, validation errors, report download behavior, and configuration defaults.

## Example Usage

- Paste a job description such as "Python Machine Learning Engineer".
- Upload several candidate PDF resumes.
- Review the ranking results in the web interface.
- Download either the text or PDF HR report.

## Notes

- Only PDF files are accepted for upload.
- The total upload size and number of uploaded resumes are limited.
- Temporary files are removed after each resume is processed.
- The app stores the latest ranking results in the Flask session for report downloads.

## Future Improvements

Potential enhancements include:

- broader resume-format support beyond PDF,
- stronger domain-specific skill extraction,
- better handling of edge-case resume layouts,
- more advanced candidate scoring logic,
- deployment to a cloud hosting environment,
- export support for structured candidate data and recruiting workflows.
