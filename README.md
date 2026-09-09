# AI-Powered Resume Ranker

An AI-powered resume screening and ranking system that evaluates multiple PDF resumes against a job description using skill matching and TF-IDF-based text similarity.

The system ranks candidates, identifies matched and missing skills, provides candidate-specific insights, and generates HR evaluation reports in both TXT and PDF formats.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Objectives](#2-objectives)
3. [Key Features](#3-key-features)
4. [Technology Stack](#4-technology-stack)
5. [System Architecture](#5-system-architecture)
6. [Project Structure](#6-project-structure)
7. [How the Ranking Works](#7-how-the-ranking-works)
8. [Scoring Methodology](#8-scoring-methodology)
9. [Recommendation Categories](#9-recommendation-categories)
10. [Candidate Insights](#10-candidate-insights)
11. [Reports](#11-reports)
12. [Installation](#12-installation)
13. [Running the Web Application](#13-running-the-web-application)
14. [Running Batch Ranking](#14-running-batch-ranking)
15. [Running Tests](#15-running-tests)
16. [Configuration](#16-configuration)
17. [Input Validation](#17-input-validation)
18. [Example Results](#18-example-results)
19. [Advantages](#19-advantages)
20. [Limitations](#20-limitations)
21. [Future Enhancements](#21-future-enhancements)
22. [Testing and Validation](#22-testing-and-validation)
23. [Conclusion](#23-conclusion)
24. [Project Status](#24-project-status)

---

# 1. Project Overview

Recruiters often need to evaluate multiple resumes against a specific job description.

Manually comparing every resume with the required skills, responsibilities, and job requirements can be time-consuming and inconsistent.

The **AI-Powered Resume Ranker** automates this process by comparing uploaded PDF resumes with a supplied job description.

The system:

- Accepts a job description.
- Accepts multiple PDF resumes.
- Extracts text from resumes.
- Identifies candidate names.
- Extracts relevant skills.
- Matches candidate skills against job requirements.
- Calculates TF-IDF-based textual similarity.
- Calculates a weighted overall suitability score.
- Ranks candidates from highest to lowest.
- Identifies matched and missing skills.
- Generates candidate-specific insights.
- Generates HR evaluation reports.
- Generates downloadable PDF reports.

The project is designed as a decision-support system for resume screening and candidate evaluation.

---

# 2. Objectives

The main objectives of the project are:

- Automate the initial resume screening process.
- Reduce the manual effort required to compare resumes.
- Provide consistent candidate evaluation.
- Identify relevant skills present in each resume.
- Identify skills missing from each resume.
- Measure textual relevance between a resume and job description.
- Rank multiple candidates based on an overall suitability score.
- Provide understandable explanations for candidate rankings.
- Generate HR-friendly evaluation reports.
- Provide both web-based and batch-processing workflows.
- Validate the application using automated tests.

---

# 3. Key Features

## 3.1 Resume Processing

The system supports:

- PDF resume uploads.
- Multiple resume processing.
- PDF file validation.
- Resume text extraction.
- Candidate name extraction.
- Temporary-file handling.
- Temporary-file cleanup.
- Resume size validation.
- Maximum resume-count validation.

---

## 3.2 Skill Matching

The system compares skills found in the candidate resume against the skills required by the job description.

The result includes:

- Skill match percentage.
- Matched skills.
- Missing skills.

Examples of supported skills include:

- Python
- SQL
- Machine Learning
- Scikit-learn
- Logistic Regression
- Classification
- Regression
- Feature Engineering
- Model Evaluation
- Pandas
- NumPy
- Matplotlib
- Data Analysis
- Data Preprocessing
- Data Visualization
- Natural Language Processing
- spaCy
- NLTK
- TF-IDF
- Flask
- REST API
- Git
- GitHub

---

## 3.3 NLP-Based Text Similarity

The system uses TF-IDF-based text representation to compare:

- Resume text
- Job description text

Cosine similarity is used to calculate textual relevance.

The result is represented as a percentage.

---

## 3.4 Candidate Ranking

Each candidate receives:

- Skill Match Score
- Text Similarity Score
- Overall Score
- Recommendation

Candidates are then sorted from the highest overall score to the lowest.

---

## 3.5 Candidate Insights

The system generates explanations for each candidate based on:

- Skill match percentage.
- Number of missing skills.
- Textual relevance.
- Overall recommendation.

This makes the ranking easier to understand instead of presenting only numerical scores.

---

## 3.6 HR Reports

The system supports:

- HR text reports.
- PDF HR reports.

Reports contain detailed candidate evaluation information.

---

## 3.7 Web Interface

The Flask web application provides:

- Job description input.
- Multiple PDF upload.
- Candidate ranking table.
- Candidate score breakdown.
- Recommendation badges.
- Matched skill display.
- Missing skill display.
- Candidate insights.
- HR report download.
- PDF report download.
- Responsive layout.
- Accessibility-oriented form controls and focus states.

---

# 4. Technology Stack

## Backend

- Python
- Flask

## Natural Language Processing

- scikit-learn
- TF-IDF
- Cosine similarity

## PDF Processing

- PyPDF2

## Testing

- pytest

## PDF Reporting

- ReportLab

## Frontend

- HTML
- CSS
- Jinja Templates

## Version Control

- Git
- GitHub

---

# 5. System Architecture

The application follows a modular processing pipeline.

```text
                    ┌──────────────────────┐
                    │      HR / User       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Flask Web App    │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌───────────────────┐       ┌───────────────────┐
       │  Job Description  │       │    PDF Resumes    │
       └─────────┬─────────┘       └─────────┬─────────┘
                 │                           │
                 │                           ▼
                 │                 ┌───────────────────┐
                 │                 │  Resume Parser    │
                 │                 └─────────┬─────────┘
                 │                           │
                 │                           ▼
                 │                 ┌───────────────────┐
                 │                 │ Candidate Name +  │
                 │                 │ Resume Text       │
                 │                 └─────────┬─────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
                    ┌──────────────────────┐
                    │    Skill Matching    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  TF-IDF Similarity   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Weighted Scoring   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Candidate Ranking   │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
        ┌─────────────┐ ┌────────────┐ ┌────────────┐
        │   Web UI    │ │ TXT Report │ │ PDF Report │
        └─────────────┘ └────────────┘ └────────────┘

        ..