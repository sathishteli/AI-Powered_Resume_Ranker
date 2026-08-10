"""
NLP processing and skill extraction for the AI Resume Ranker.

Uses spaCy for basic NLP processing and a configurable skill
dictionary for technical skill extraction.
"""

import re

import spacy


# Load spaCy English language model
nlp = spacy.load("en_core_web_sm")


# Configurable technical skill dictionary
SKILL_DICTIONARY = {
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c#",
    "sql",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "computer vision",

    "scikit-learn",
    "sklearn",
    "tensorflow",
    "keras",
    "pytorch",

    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "plotly",

    "spacy",
    "nltk",
    "tf-idf",
    "tfidf",
    "cosine similarity",

    "flask",
    "fastapi",
    "django",
    "rest api",

    "html",
    "css",
    "react",
    "node.js",
    "node",

    "mysql",
    "postgresql",
    "mongodb",

    "git",
    "github",
    "docker",

    "data analysis",
    "data preprocessing",
    "data cleaning",
    "data visualization",
    "exploratory data analysis",
    "feature engineering",

    "logistic regression",
    "linear regression",
    "knn",
    "classification",
    "regression",
    "model evaluation",
}


def clean_text(text: str) -> str:
    """
    Clean extracted resume text.

    Parameters
    ----------
    text : str
        Raw text extracted from a resume.

    Returns
    -------
    str
        Cleaned text.
    """

    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove unnecessary leading/trailing whitespace
    text = text.strip()

    return text


def preprocess_text(text: str) -> str:
    """
    Apply basic spaCy NLP preprocessing.

    Removes punctuation and stop words while keeping
    meaningful tokens.

    Parameters
    ----------
    text : str
        Resume text.

    Returns
    -------
    str
        Processed text.
    """

    cleaned_text = clean_text(text)

    doc = nlp(cleaned_text)

    tokens = [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop
        and not token.is_punct
        and not token.is_space
    ]

    return " ".join(tokens)


def extract_skills(text: str) -> list[str]:
    """
    Extract technical skills from resume text.

    Matching is case-insensitive.

    Parameters
    ----------
    text : str
        Resume text.

    Returns
    -------
    list[str]
        Unique skills detected in the resume.
    """

    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")

    text_lower = text.lower()

    found_skills = []

    # Sort longer skills first so phrases such as
    # "machine learning" are checked before "learning".
    sorted_skills = sorted(
        SKILL_DICTIONARY,
        key=len,
        reverse=True
    )

    for skill in sorted_skills:

        # Escape special regex characters
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(set(found_skills))


def analyze_resume(text: str) -> dict:
    """
    Perform complete NLP analysis on resume text.

    Returns cleaned text, processed text, and extracted skills.
    """

    cleaned = clean_text(text)
    processed = preprocess_text(cleaned)
    skills = extract_skills(cleaned)

    return {
        "cleaned_text": cleaned,
        "processed_text": processed,
        "skills": skills,
    }


if __name__ == "__main__":

    # Test the NLP processor using the sample resume
    from resume_parser import extract_text_from_pdf

    sample_pdf = "tests/sample_resumes/sample_resume.pdf"

    resume_text = extract_text_from_pdf(sample_pdf)

    result = analyze_resume(resume_text)

    print("=" * 60)
    print("NLP PROCESSING TEST")
    print("=" * 60)

    print("\nExtracted Skills:")

    for skill in result["skills"]:
        print(f"- {skill}")

    print("\nTotal Skills:", len(result["skills"]))

    print("\nProcessed Text Preview:")
    print(result["processed_text"][:1000])