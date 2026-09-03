

## 1. Project Title

AI-Powered Resume Ranker

## 2. Project Objective

To develop an automated resume screening system that compares multiple PDF resumes against a job description and ranks candidates according to their skills and textual relevance.

## 3. Completed Work

### Resume Processing
- PDF resume upload and validation.
- Resume text extraction.
- Candidate name extraction.
- Multiple resume processing.
- Temporary-file cleanup.
- Resume size and upload-count validation.

### Resume Ranking
- Required skill extraction.
- Candidate skill matching.
- Matched and missing skill identification.
- TF-IDF-based text similarity.
- Weighted overall candidate scoring.
- Candidate ranking.
- Recommendation generation.

### Candidate Insights
- Skill-match explanations.
- Missing-skill analysis.
- Textual relevance assessment.
- Overall suitability explanations.

### Web Application
- Flask-based web interface.
- Job description input.
- Multiple PDF resume upload.
- Candidate ranking display.
- Candidate analysis display.
- HR report download.
- PDF report download.
- Input validation and error handling.
- UI and accessibility improvements.

### Reporting
- HR text report generation.
- PDF HR report generation.
- Candidate score breakdown.
- Matched and missing skill reporting.

### Testing
- Automated testing using pytest.
- Parser tests.
- Ranking-related tests.
- Web application tests.
- Input validation tests.
- Report-related validation.
- Flask configuration tests.

## 4. Ranking Methodology

The final candidate score uses two components:

- Skill Match: 70%
- Text Similarity: 30%

The overall score is calculated as:

Overall Score = (Skill Match × 0.70) + (Text Similarity × 0.30)

Candidates are ranked from the highest overall score to the lowest.

## 5. Recommendation Categories

| Overall Score | Recommendation |
|---:|---|
| 80–100% | Highly Suitable |
| 60–79.99% | Suitable |
| 40–59.99% | Moderately Suitable |
| 0–39.99% | Low Match |

## 6. Validation Results

The final automated test suite contains:

**52 tests passed**

Final regression ranking:

| Rank | Candidate | Skill Match | Text Similarity | Overall |
|---:|---|---:|---:|---:|
| 1 | Alex Johnson | 100.00% | 56.39% | 86.92% |
| 2 | Priya Sharma | 68.00% | 56.86% | 64.66% |
| 3 | Ananya Reddy | 36.00% | 27.30% | 33.39% |
| 4 | Rahul Kumar | 24.00% | 11.37% | 20.21% |

## 7. Technologies Used

- Python
- Flask
- scikit-learn
- TF-IDF
- PyPDF2
- ReportLab
- HTML
- CSS
- Jinja Templates
- pytest
- Git

## 8. Current Status

The core implementation, testing, reporting, web interface, configuration, documentation, and integration validation have been completed.

The project repository is maintained using Git and the final validated working tree is clean.

## 9. Future Scope


- OCR support for scanned resumes.
- Transformer-based semantic similarity.
- Improved skill synonym detection.
- Experience and education matching.
- Candidate filtering and search.
- Database integration.
- Authentication and role-based access.
- Cloud deployment.
- Advanced analytics and dashboards.
- Multi-language resume support.

## 10. Conclusion

The AI-Powered Resume Ranker successfully automates the initial resume screening process by combining skill matching and NLP-based textual similarity.

The system processes multiple PDF resumes, ranks candidates, identifies skill gaps, provides candidate insights, and generates HR evaluation reports.

The completed implementation has been validated using automated tests and full integration testing.