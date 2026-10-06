"""
Skill Extractor Test Suite
Verifies canonical skill detection, alias resolution, boundary protection, and category assignment.
"""

from app.services.skill_extractor import (
    extract_skills,
    extract_skills_with_categories,
    compare_skills
)


def test_extract_skills_canonical_and_aliases():
    sample = "We use postgres, reactjs, k8s, and python3 for our cloud services."
    skills = extract_skills(sample)
    assert "PostgreSQL" in skills
    assert "React" in skills
    assert "Kubernetes" in skills
    assert "Python" in skills


def test_extract_skills_boundary_and_case_protection():
    # 'Good' or 'Going' must not trigger 'Go'
    sample1 = "Good morning, I am going to the store."
    assert "Go" not in extract_skills(sample1)

    # Actual 'Go' programming language mention
    sample2 = "Built microservices using Go and Docker."
    assert "Go" in extract_skills(sample2)

    # Special characters: C++ and C#
    sample3 = "Experienced in C++ and C# desktop applications."
    skills3 = extract_skills(sample3)
    assert "C++" in skills3
    assert "C#" in skills3


def test_compare_skills():
    resume_skills = ["Python", "FastAPI", "PostgreSQL", "Git"]
    job_skills = ["Python", "FastAPI", "Docker", "AWS", "PostgreSQL"]

    matching, missing = compare_skills(resume_skills, job_skills)
    assert sorted(matching) == ["FastAPI", "PostgreSQL", "Python"]
    assert sorted(missing) == ["AWS", "Docker"]


def test_extract_skills_with_categories():
    sample = "Proficient in Python, React, PostgreSQL, Docker, and PyTorch."
    categorized = extract_skills_with_categories(sample)

    assert "Programming" in categorized
    assert "Python" in categorized["Programming"]

    assert "Frontend" in categorized
    assert "React" in categorized["Frontend"]

    assert "Database" in categorized
    assert "PostgreSQL" in categorized["Database"]

    assert "Cloud & DevOps" in categorized
    assert "Docker" in categorized["Cloud & DevOps"]

    assert "AI / ML & Data" in categorized
    assert "PyTorch" in categorized["AI / ML & Data"]
