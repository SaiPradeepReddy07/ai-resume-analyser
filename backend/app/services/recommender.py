"""
Recommendation Engine
Generates tailored, actionable suggestions to help the applicant optimize their resume
for the target role while strictly adhering to ethical guidelines (never falsifying experience).
"""

from typing import List, Dict, Any
from app.utils.skills_taxonomy import get_skill_category


def generate_recommendations(
    match_score: float,
    skill_score: float,
    matching_skills: List[str],
    missing_skills: List[str],
    resume_text: str,
    job_description: str
) -> List[Dict[str, str]]:
    """
    Analyzes gaps and provides context-aware, structured resume improvement recommendations.
    """
    recommendations: List[Dict[str, str]] = []

    # 1. Critical Missing Skills Recommendation
    if missing_skills:
        top_missing = missing_skills[:4]
        missing_str = ", ".join(top_missing)
        recommendations.append({
            "type": "skill_gap",
            "title": "Address Key Missing Technologies",
            "detail": (
                f"The job posting emphasizes {missing_str}. If you have hands-on experience, academic coursework, "
                "or personal projects utilizing these technologies, explicitly mention them in your skills and project sections."
            )
        })

    # 2. Project Relevance & Domain Alignment
    if len(matching_skills) > 0:
        recommendations.append({
            "type": "project_alignment",
            "title": "Highlight Relevant Projects First",
            "detail": (
                f"Move projects showcasing your experience with {', '.join(matching_skills[:3])} to the top of your "
                "projects section. Hiring managers spend an average of 6 seconds skimming for direct alignment."
            )
        })

    # 3. Quantifiable Impact & Metrics Check
    # Check if numbers or percentages are present in resume text
    has_metrics = bool(any(char.isdigit() for char in resume_text))
    if not has_metrics or resume_text.count("%") < 2:
        recommendations.append({
            "type": "quantification",
            "title": "Quantify Achievements with Metrics",
            "detail": (
                "Transform passive duty statements into impact statements using the XYZ formula: 'Accomplished [X] "
                "as measured by [Y], by doing [Z]'. Example: 'Reduced API response times by 35% through Redis caching'."
            )
        })

    # 4. Action Verbs & Technical Specificity
    low_verbs = ["worked on", "responsible for", "helped with", "assisted in"]
    has_weak_verbs = any(wv in resume_text.lower() for wv in low_verbs)
    if has_weak_verbs:
        recommendations.append({
            "type": "action_verbs",
            "title": "Strengthen Action Verbs",
            "detail": (
                "Replace passive phrases like 'worked on' or 'responsible for' with assertive, high-impact verbs: "
                "'Architected', 'Spearheaded', 'Engineered', 'Optimized', or 'Automated'."
            )
        })

    # 5. Professional Summary / Objective Optimization
    if "summary" not in resume_text.lower() and "profile" not in resume_text.lower():
        recommendations.append({
            "type": "summary",
            "title": "Add a Tailored Professional Summary",
            "detail": (
                "Include a 2–3 sentence professional summary at the very top of your resume clearly stating your core "
                "stack, key strengths, and target role focus."
            )
        })

    # 6. Score-tier specific recommendation
    if match_score < 60:
        recommendations.append({
            "type": "strategic_pivot",
            "title": "Customize Terminology to Match the Job Posting",
            "detail": (
                "Ensure standard industry terms from the job posting are mirrored accurately. Applicant Tracking Systems "
                "(ATS) frequently scan for exact keyword tokens."
            )
        })

    # 7. Ethical Foundation Guarantee (Always Included)
    recommendations.append({
        "type": "ethics",
        "title": "Professional Integrity Note",
        "detail": (
            "Only add skills, tools, and libraries that you have genuine working familiarity with. If you lack a required "
            "skill, showcase fast adaptability by building a small GitHub demonstration project incorporating it."
        )
    })

    return recommendations


def generate_missing_skills_details(missing_skills: List[str]) -> List[Dict[str, str]]:
    """
    Constructs an informative explanation for every detected missing skill.
    """
    details = []
    for skill in missing_skills:
        category = get_skill_category(skill)
        details.append({
            "skill": skill,
            "category": category,
            "explanation": f"'{skill}' ({category}) appears in the job requirements but was not detected in your resume."
        })
    return details
