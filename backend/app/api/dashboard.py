"""
Dashboard Metrics Router
Aggregates performance analytics, trends over time, score distributions,
and recurring skill gaps for the authenticated user.
"""

from collections import Counter
from typing import List, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.analysis import Analysis
from app.schemas.dashboard import (
    DashboardStatsResponse,
    FrequentlyMissingSkill,
    ScoreHistoryPoint
)
from app.schemas.analysis import AnalysisListItem
from app.services.resume_analyzer import get_match_tier
from app.utils.skills_taxonomy import get_skill_category

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Computes summary metrics, score timeline, and missing skill frequency for the user dashboard.
    """
    analyses = db.query(Analysis).filter(
        Analysis.user_id == current_user.id
    ).order_by(Analysis.created_at.asc()).all()

    total_analyses = len(analyses)

    if total_analyses == 0:
        return DashboardStatsResponse(
            total_analyses=0,
            average_score=0.0,
            highest_score=0.0,
            lowest_score=0.0,
            most_frequently_missing_skills=[],
            score_history=[],
            recent_analyses=[]
        )

    scores = [a.match_score for a in analyses]
    average_score = round(sum(scores) / total_analyses, 1)
    highest_score = round(max(scores), 1)
    lowest_score = round(min(scores), 1)

    # Count missing skills across all past analyses
    missing_skill_counter = Counter()
    for a in analyses:
        if a.missing_skills:
            for item in a.missing_skills:
                # Handle both dict objects and raw strings
                skill_name = item.get("skill") if isinstance(item, dict) else str(item)
                if skill_name:
                    missing_skill_counter[skill_name] += 1

    top_missing_list: List[FrequentlyMissingSkill] = []
    for skill_name, count in missing_skill_counter.most_common(6):
        top_missing_list.append(FrequentlyMissingSkill(
            skill=skill_name,
            category=get_skill_category(skill_name),
            count=count
        ))

    # Build chronological score history for Recharts
    score_history: List[ScoreHistoryPoint] = []
    for a in analyses:
        date_str = a.created_at.strftime("%b %d") if a.created_at else ""
        job_title = a.job_description.title if a.job_description else "Untitled Role"
        company = a.job_description.company if a.job_description else ""
        score_history.append(ScoreHistoryPoint(
            id=a.id,
            date=date_str,
            score=a.match_score,
            job_title=job_title,
            company=company
        ))

    # Recent 5 analyses (in reverse chronological order)
    recent_analyses: List[AnalysisListItem] = []
    for a in reversed(analyses[-5:]):
        job_title = a.job_description.title if a.job_description else "Untitled Role"
        company = a.job_description.company if a.job_description else ""
        recent_analyses.append(AnalysisListItem(
            id=a.id,
            job_title=job_title,
            company=company,
            match_score=a.match_score,
            match_tier=get_match_tier(a.match_score),
            matching_skills_count=len(a.matching_skills or []),
            missing_skills_count=len(a.missing_skills or []),
            created_at=a.created_at
        ))

    return DashboardStatsResponse(
        total_analyses=total_analyses,
        average_score=average_score,
        highest_score=highest_score,
        lowest_score=lowest_score,
        most_frequently_missing_skills=top_missing_list,
        score_history=score_history,
        recent_analyses=recent_analyses
    )
