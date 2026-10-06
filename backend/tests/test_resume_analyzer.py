"""
Resume Analyzer Pipeline Test Suite
Verifies composite scoring mathematics, tier ratings, TF-IDF cosine similarity,
and ethical recommendation rules.
"""

from app.services.resume_analyzer import (
    analyze_resume_against_job,
    calculate_tfidf_similarity,
    get_match_tier
)


def test_match_tier_classification():
    assert get_match_tier(95.0) == "Excellent Match"
    assert get_match_tier(82.0) == "Strong Match"
    assert get_match_tier(68.0) == "Good Match"
    assert get_match_tier(45.0) == "Needs Improvement"
    assert get_match_tier(25.0) == "Poor Match"


def test_tfidf_similarity_identical_texts():
    text = "Python FastAPI PostgreSQL Docker Git"
    score = calculate_tfidf_similarity(text, text)
    assert score >= 99.0


def test_tfidf_similarity_orthogonal_texts():
    text1 = "Gardening flowers plants soil sunshine"
    text2 = "Kubernetes Docker Terraform AWS Cloud DevOps"
    score = calculate_tfidf_similarity(text1, text2)
    assert score <= 10.0


def test_analyze_resume_against_job_full_flow():
    resume = """
    Software Developer with experience in Python, FastAPI, and PostgreSQL.
    Created REST APIs and automated unit tests using pytest and Git.
    """
    job = """
    Seeking a Python Engineer with FastAPI, PostgreSQL, Git, and Docker experience.
    Must understand REST API design and unit testing.
    """
    result = analyze_resume_against_job(resume, job)

    assert 0.0 <= result["match_score"] <= 100.0
    assert "Python" in result["matching_skills"]
    assert "FastAPI" in result["matching_skills"]
    assert "PostgreSQL" in result["matching_skills"]
    assert "Docker" in result["raw_missing_skills"]

    # Recommendations must contain ethical guidance
    recs = result["recommendations"]
    assert any(r["type"] == "ethics" for r in recs)


def test_analysis_changes_when_target_role_changes():
    resume = """
    Software developer with Python, FastAPI, PostgreSQL, Docker, Git, and REST API experience.
    Built applications and automated unit testing with pytest.
    """
    python_role = """
    Python backend developer. Required skills: Python, FastAPI, PostgreSQL, Docker, Git,
    REST API design, and unit testing.
    """
    data_analyst_role = """
    Data analyst. Required skills: SQL, Python, Pandas, NumPy, Data Analysis,
    Matplotlib, and Tableau dashboards.
    """

    python_result = analyze_resume_against_job(resume, python_role)
    analyst_result = analyze_resume_against_job(resume, data_analyst_role)

    assert python_result["job_skills"] != analyst_result["job_skills"]
    assert python_result["matching_skills"] != analyst_result["matching_skills"]
    assert python_result["missing_skills"] != analyst_result["missing_skills"]
    assert python_result["match_score"] != analyst_result["match_score"]
