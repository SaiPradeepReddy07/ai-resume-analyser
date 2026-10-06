from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class MissingSkillDetail(BaseModel):
    skill: str
    category: str
    explanation: str


class RecommendationDetail(BaseModel):
    type: str  # e.g., 'skill_gap', 'quantification', 'formatting', 'ethics'
    title: str
    detail: str


class AnalysisCreate(BaseModel):
    resume_id: int
    job_description_id: int


class CategorySkillCount(BaseModel):
    resume: int = 0
    job: int = 0


class AnalysisResponse(BaseModel):
    id: int
    match_score: float
    match_tier: str
    skill_score: float
    keyword_score: float
    semantic_score: float
    job_title: str
    company: str
    matching_skills: List[str]
    missing_skills: List[MissingSkillDetail]
    recommendations: List[RecommendationDetail]
    category_breakdown: Dict[str, Dict[str, int]]
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalysisListItem(BaseModel):
    id: int
    job_title: str
    company: str
    match_score: float
    match_tier: str
    matching_skills_count: int
    missing_skills_count: int
    created_at: datetime

    model_config = {"from_attributes": True}
