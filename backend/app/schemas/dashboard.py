from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.schemas.analysis import AnalysisListItem


class FrequentlyMissingSkill(BaseModel):
    skill: str
    category: str
    count: int


class ScoreHistoryPoint(BaseModel):
    id: int
    date: str
    score: float
    job_title: str
    company: str


class DashboardStatsResponse(BaseModel):
    total_analyses: int
    average_score: float
    highest_score: float
    lowest_score: float
    most_frequently_missing_skills: List[FrequentlyMissingSkill]
    score_history: List[ScoreHistoryPoint]
    recent_analyses: List[AnalysisListItem]
