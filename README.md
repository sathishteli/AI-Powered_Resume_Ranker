# AI-Powered Resume Ranker

An AI-assisted resume screening application that compares uploaded PDF resumes against a job description and ranks candidates based on skill match and text similarity.

The project is a Flask-based web app designed to help recruiters shortlist candidates faster by extracting skills, comparing them to role requirements, and generating downloadable HR reports.

## Overview

This application allows a user to:

- paste a job description,
- upload multiple PDF resumes,
- extract resume text and candidate names,
- compare required skills with candidate skills,
- calculate a weighted ranking score,
- review matched and missing skills,
- download a text or PDF report for recruitment review.

## Features

- Multi-resume PDF upload
- Job description validation
- PDF text extraction
- Candidate name detection
- Skill extraction and matching
- TF-IDF similarity scoring
- Weighted overall ranking score
- Recommendation labels
- Candidate insights and explanations
- Downloadable HR reports in TXT and PDF format
- Flask web interface

## Tech Stack

- Python
- Flask
- scikit-learn
- spaCy
- PyMuPDF
- ReportLab
- pytest
- HTML, CSS, and Jinja templates

## Project Structure

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
│   ├── test_parser.py
│   ├── test_web_app.py
│   └── sample_resumes/
├── uploads/
└── app/static/
    ├── style.css
    ├── css/
    └── js/
```

## Installation

1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

Start the Flask application:

```bash
python app.py
```

Then open the app in a browser:

```text
http://127.0.0.1:5000
```

## How the Ranking Works

The scoring pipeline is:

1. Extract text from each uploaded PDF.
2. Detect the candidate name.
3. Extract skills from the resume and the job description.
4. Compare skills and compute a skill match percentage.
5. Run TF-IDF cosine similarity between resume text and the job description.
6. Combine the skill score and text similarity using a weighted formula.
7. Sort candidates by total score and show recommendations.

Default scoring weights:

- Skill match: 70%
- Text similarity: 30%

## Report Generation

The app can generate:

- a text HR summary report,
- a PDF report for download.

These reports summarize ranking results, matched skills, missing skills, and recommendation status.

## Configuration

The app supports environment variables such as:

```bash
FLASK_SECRET_KEY
FLASK_DEBUG
FLASK_HOST
FLASK_PORT
MAX_CONTENT_LENGTH_MB
MAX_RESUME_FILES
MAX_RESUME_SIZE_MB
```

## Running Tests

```bash
pytest
```

## Example Usage

- Paste a job description such as "Python Machine Learning Engineer".
- Upload several candidate resumes.
- Review the ranking results.
- Download the reports for recruiter screening.

## Notes

- Only PDF resumes are accepted.
- Total upload size and file count are limited.
- Temporary files are cleaned up after processing.

## Future Improvements

Possible enhancements include:

- better parser support for more resume formats,
- stronger domain-specific skill extraction,
- AI-based candidate scoring refinement,
- deployment to a cloud app server,
- support for structured job descriptions and candidate data exports.
