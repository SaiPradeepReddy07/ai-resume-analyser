"""
Skill Extraction Service
Extracts and normalizes technical skills from resumes and job descriptions using
the extended skills taxonomy, regex boundary guards, and alias resolution.
"""

import re
from typing import Dict, List, Set, Tuple
from app.utils.skills_taxonomy import (
    SKILLS_TAXONOMY,
    SKILL_ALIASES,
    get_all_canonical_skills,
    get_skill_category
)

# Skills requiring strict case-sensitive matching to avoid false positives (e.g. "C", "R", "Go")
CASE_SENSITIVE_SKILLS = {"C", "R", "Go"}


def _compile_skill_pattern(skill: str, is_case_sensitive: bool = False) -> re.Pattern:
    """
    Compiles a robust regex pattern for a skill accounting for special characters
    like ++, #, ., -, and word boundaries.
    """
    escaped = re.escape(skill)

    # If skill starts with a word char, prefix with \b; otherwise use negative lookbehind
    if re.match(r"^\w", skill):
        prefix = r"(?<![A-Za-z0-9_])"
    else:
        prefix = r""

    # If skill ends with a word char, suffix with \b; otherwise use negative lookahead
    if re.match(r".*\w$", skill):
        suffix = r"(?![A-Za-z0-9_])"
    else:
        suffix = r""

    pattern_str = f"{prefix}{escaped}{suffix}"
    flags = 0 if is_case_sensitive else re.IGNORECASE
    return re.compile(pattern_str, flags)


# Precompile patterns for fast repeated execution
COMPILED_CANONICAL_PATTERNS = [
    (skill, _compile_skill_pattern(skill, is_case_sensitive=(skill in CASE_SENSITIVE_SKILLS)))
    for skill in get_all_canonical_skills()
]

COMPILED_ALIAS_PATTERNS = [
    (alias, canonical, _compile_skill_pattern(alias, is_case_sensitive=False))
    for alias, canonical in SKILL_ALIASES.items()
]


def extract_skills(text: str) -> List[str]:
    """
    Extracts all unique canonical skills detected in the given text string.
    Returns a sorted list of unique canonical skill names.
    """
    if not text:
        return []

    detected_skills: Set[str] = set()

    # 1. Match canonical skills
    for canonical_name, pattern in COMPILED_CANONICAL_PATTERNS:
        if pattern.search(text):
            detected_skills.add(canonical_name)

    # 2. Match aliases and map to canonical names
    for alias, canonical_name, pattern in COMPILED_ALIAS_PATTERNS:
        if pattern.search(text):
            detected_skills.add(canonical_name)

    return sorted(list(detected_skills))


def extract_skills_with_categories(text: str) -> Dict[str, List[str]]:
    """
    Extracts detected skills and organizes them by domain category.
    Only categories with at least one detected skill are included.
    """
    skills = extract_skills(text)
    categorized: Dict[str, List[str]] = {}

    for skill in skills:
        category = get_skill_category(skill)
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(skill)

    return categorized


def compare_skills(resume_skills: List[str], job_skills: List[str]) -> Tuple[List[str], List[str]]:
    """
    Compares resume skills against job requirements.
    
    Returns:
        Tuple[List[str], List[str]]: (matching_skills, missing_skills)
    """
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matching = sorted(list(resume_set.intersection(job_set)))
    missing = sorted(list(job_set.difference(resume_set)))

    return matching, missing
