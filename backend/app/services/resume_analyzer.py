"""
Resume Analyzer Pipeline Service
Coordinates the end-to-end NLP evaluation between extracted resume text and target job description:
1. Skills extraction from both documents
2. Skill recall scoring (50%)
3. TF-IDF keyword cosine similarity (25%)
4. Text-wide document cosine similarity (25%)
5. Missing skills gap analysis with explanations
6. Actionable recommendations generation
7. Category breakdown matrix
"""

import math
import re
from collections import Counter
from typing import Dict, Any, List, Set, Tuple

from app.services.text_cleaner import clean_text, tokenize_for_nlp
from app.services.skill_extractor import (
    extract_skills,
    extract_skills_with_categories,
    compare_skills
)
from app.services.recommender import (
    generate_recommendations,
    generate_missing_skills_details
)
from app.utils.skills_taxonomy import SKILLS_TAXONOMY, get_skill_category

# Standard English stopwords to remove noise in text similarity calculations
ENGLISH_STOP_WORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than",
    "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've",
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was",
    "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what",
    "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's",
    "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd",
    "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
}


def get_match_tier(score: float) -> str:
    """Classifies a 0–100 numerical score into a standard human-readable tier."""
    if score >= 90.0:
        return "Excellent Match"
    elif score >= 75.0:
        return "Strong Match"
    elif score >= 60.0:
        return "Good Match"
    elif score >= 40.0:
        return "Needs Improvement"
    else:
        return "Poor Match"


def calculate_tfidf_similarity(text1: str, text2: str) -> float:
    """
    Computes mathematical TF-IDF Cosine Similarity between two texts.
    Returns:
        float: Similarity percentage bounded between 0.0 and 100.0.
    """
    if not text1 or not text2:
        return 0.0

    # Extract tokens filtering stopwords and single-char noise
    tokens1 = [w for w in re.findall(r"\b[a-z0-9+#.-]+\b", text1.lower()) if w not in ENGLISH_STOP_WORDS and len(w) > 1]
    tokens2 = [w for w in re.findall(r"\b[a-z0-9+#.-]+\b", text2.lower()) if w not in ENGLISH_STOP_WORDS and len(w) > 1]

    if not tokens1 or not tokens2:
        return 0.0

    vocab = sorted(list(set(tokens1 + tokens2)))
    if not vocab:
        return 0.0

    c1 = Counter(tokens1)
    c2 = Counter(tokens2)
    n_docs = 2

    vec1: List[float] = []
    vec2: List[float] = []

    for term in vocab:
        df = (1 if term in c1 else 0) + (1 if term in c2 else 0)
        idf = math.log((1 + n_docs) / (1 + df)) + 1.0

        tf1 = (1 + math.log(c1[term])) if c1[term] > 0 else 0.0
        tf2 = (1 + math.log(c2[term])) if c2[term] > 0 else 0.0

        vec1.append(tf1 * idf)
        vec2.append(tf2 * idf)

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))

    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0

    similarity = (dot_product / (norm1 * norm2)) * 100.0
    return max(0.0, min(100.0, round(similarity, 1)))


def calculate_category_breakdown(
    resume_skills: List[str],
    job_skills: List[str]
) -> Dict[str, Dict[str, int]]:
    """
    Calculates the count of skills present in resume vs required by job across each category.
    """
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    breakdown: Dict[str, Dict[str, int]] = {}

    for category, cat_skills in SKILLS_TAXONOMY.items():
        res_count = len([s for s in cat_skills if s in resume_set])
        job_count = len([s for s in cat_skills if s in job_set])
        if res_count > 0 or job_count > 0:
            breakdown[category] = {
                "resume": res_count,
                "job": job_count
            }

    return breakdown


def analyze_resume_against_job(resume_text: str, job_description: str) -> Dict[str, Any]:
    """
    Main analysis pipeline function.
    
    Args:
        resume_text: Extracted text of applicant resume.
        job_description: Target job posting text.
        
    Returns:
        Dict[str, Any]: Complete analysis metrics, scores, badges, and recommendations.
    """
    cleaned_resume = clean_text(resume_text)
    cleaned_job = clean_text(job_description)

    # 1. Extract skills from both texts
    resume_skills = extract_skills(cleaned_resume)
    job_skills = extract_skills(cleaned_job)

    # 2. Compare skills (intersection and difference)
    matching_skills, missing_skills = compare_skills(resume_skills, job_skills)

    # 3. Metric 1: Skill Recall Score (50% weight)
    if len(job_skills) > 0:
        skill_score = (len(matching_skills) / len(job_skills)) * 100.0
    else:
        skill_score = min(100.0, len(resume_skills) * 10.0) if resume_skills else 50.0
    skill_score = round(max(0.0, min(100.0, skill_score)), 1)

    # 4. Metric 2: Keyword Alignment Score (25% weight)
    # Evaluates TF-IDF similarity between technical skill terms
    resume_skill_terms = " ".join([s.lower() for s in resume_skills])
    job_skill_terms = " ".join([s.lower() for s in job_skills])
    keyword_score = calculate_tfidf_similarity(resume_skill_terms, job_skill_terms)

    # 5. Metric 3: Semantic / Full Document Similarity (25% weight)
    # Compare tokenized documents; calibrated for informational text retrieval
    raw_doc_similarity = calculate_tfidf_similarity(cleaned_resume, cleaned_job)
    semantic_score = round(min(100.0, raw_doc_similarity * 2.0), 1)

    # 6. Composite Match Score: 50% Skill + 25% Keyword + 25% Semantic
    composite_score = round(
        (0.50 * skill_score) + (0.25 * keyword_score) + (0.25 * semantic_score),
        1
    )
    composite_score = max(0.0, min(100.0, composite_score))

    # 7. Generate category matrix and explanations
    category_breakdown = calculate_category_breakdown(resume_skills, job_skills)
    missing_skills_details = generate_missing_skills_details(missing_skills)
    recommendations = generate_recommendations(
        match_score=composite_score,
        skill_score=skill_score,
        matching_skills=matching_skills,
        missing_skills=missing_skills,
        resume_text=cleaned_resume,
        job_description=cleaned_job
    )

    return {
        "match_score": composite_score,
        "match_tier": get_match_tier(composite_score),
        "skill_score": skill_score,
        "keyword_score": keyword_score,
        "semantic_score": semantic_score,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills_details,
        "raw_missing_skills": missing_skills,
        "recommendations": recommendations,
        "category_breakdown": category_breakdown
    }
