"""
Analysis API Router
Handles multi-metric resume evaluation against job postings, single-step direct uploads,
preloaded sample testing, and history filtering.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.analysis import Analysis
from app.schemas.analysis import (
    AnalysisCreate,
    AnalysisResponse,
    AnalysisListItem
)
from app.services.pdf_extractor import extract_text_from_pdf, PDFExtractionError
from app.services.resume_analyzer import analyze_resume_against_job, get_match_tier
from app.utils.sample_data import (
    SAMPLE_RESUME_TEXT,
    SAMPLE_JOB_TITLE,
    SAMPLE_COMPANY,
    SAMPLE_JOB_DESCRIPTION
)

router = APIRouter(prefix="/analysis", tags=["Analysis"])


def _format_analysis_response(analysis: Analysis) -> AnalysisResponse:
    """Helper to convert an Analysis ORM model into the AnalysisResponse schema."""
    job_title = analysis.job_description.title if analysis.job_description else "Untitled Position"
    company = analysis.job_description.company if analysis.job_description else ""

    return AnalysisResponse(
        id=analysis.id,
        match_score=analysis.match_score,
        match_tier=get_match_tier(analysis.match_score),
        skill_score=analysis.skill_score,
        keyword_score=analysis.keyword_score,
        semantic_score=analysis.semantic_score,
        job_title=job_title,
        company=company,
        matching_skills=analysis.matching_skills or [],
        missing_skills=analysis.missing_skills or [],
        recommendations=analysis.recommendations or [],
        category_breakdown=analysis.category_breakdown or {},
        created_at=analysis.created_at
    )


@router.post("", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
def create_analysis(
    analysis_in: AnalysisCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Performs NLP analysis between an existing resume and job description.
    """
    resume = db.query(Resume).filter(
        Resume.id == analysis_in.resume_id,
        Resume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume record not found.")

    job = db.query(JobDescription).filter(
        JobDescription.id == analysis_in.job_description_id,
        JobDescription.user_id == current_user.id
    ).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found.")

    # Execute the NLP analysis pipeline
    analysis_result = analyze_resume_against_job(
        resume_text=resume.extracted_text,
        job_description=job.description
    )

    new_analysis = Analysis(
        user_id=current_user.id,
        resume_id=resume.id,
        job_description_id=job.id,
        match_score=analysis_result["match_score"],
        skill_score=analysis_result["skill_score"],
        keyword_score=analysis_result["keyword_score"],
        semantic_score=analysis_result["semantic_score"],
        matching_skills=analysis_result["matching_skills"],
        missing_skills=analysis_result["missing_skills"],
        recommendations=analysis_result["recommendations"],
        category_breakdown=analysis_result["category_breakdown"]
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    return _format_analysis_response(new_analysis)


@router.post("/direct", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def direct_analysis(
    file: UploadFile = File(...),
    job_title: str = Form(...),
    company: str = Form(""),
    job_description: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Convenience endpoint for single-step analysis:
    Uploads PDF, records job posting, runs analysis, and saves everything seamlessly.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only PDF documents (.pdf) are supported."
        )

    if not job_title.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Job title cannot be empty.")

    if len(job_description.strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description must be at least 10 characters long."
        )

    # 1. Parse and validate PDF
    try:
        content = await file.read()
        extracted_text, page_count = extract_text_from_pdf(content, filename=file.filename)
    except PDFExtractionError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while reading the PDF file."
        )

    # 2. Persist resume
    resume_record = Resume(
        user_id=current_user.id,
        filename=file.filename,
        extracted_text=extracted_text
    )
    db.add(resume_record)

    # 3. Persist job description
    job_record = JobDescription(
        user_id=current_user.id,
        title=job_title.strip(),
        company=company.strip() if company else "",
        description=job_description.strip()
    )
    db.add(job_record)
    db.commit()
    db.refresh(resume_record)
    db.refresh(job_record)

    # 4. Run NLP pipeline
    analysis_result = analyze_resume_against_job(
        resume_text=extracted_text,
        job_description=job_description.strip()
    )

    analysis_record = Analysis(
        user_id=current_user.id,
        resume_id=resume_record.id,
        job_description_id=job_record.id,
        match_score=analysis_result["match_score"],
        skill_score=analysis_result["skill_score"],
        keyword_score=analysis_result["keyword_score"],
        semantic_score=analysis_result["semantic_score"],
        matching_skills=analysis_result["matching_skills"],
        missing_skills=analysis_result["missing_skills"],
        recommendations=analysis_result["recommendations"],
        category_breakdown=analysis_result["category_breakdown"]
    )
    db.add(analysis_record)
    db.commit()
    db.refresh(analysis_record)

    return _format_analysis_response(analysis_record)


@router.post("/sample", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
def sample_analysis(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Creates an instant analysis using the preloaded 'Junior Python Developer' sample data.
    Allows beginners and portfolio reviewers to evaluate the platform immediately.
    """
    resume_record = Resume(
        user_id=current_user.id,
        filename="Alex_Morgan_Junior_Python_Resume.pdf",
        extracted_text=SAMPLE_RESUME_TEXT
    )
    db.add(resume_record)

    job_record = JobDescription(
        user_id=current_user.id,
        title=SAMPLE_JOB_TITLE,
        company=SAMPLE_COMPANY,
        description=SAMPLE_JOB_DESCRIPTION
    )
    db.add(job_record)
    db.commit()
    db.refresh(resume_record)
    db.refresh(job_record)

    analysis_result = analyze_resume_against_job(
        resume_text=SAMPLE_RESUME_TEXT,
        job_description=SAMPLE_JOB_DESCRIPTION
    )

    analysis_record = Analysis(
        user_id=current_user.id,
        resume_id=resume_record.id,
        job_description_id=job_record.id,
        match_score=analysis_result["match_score"],
        skill_score=analysis_result["skill_score"],
        keyword_score=analysis_result["keyword_score"],
        semantic_score=analysis_result["semantic_score"],
        matching_skills=analysis_result["matching_skills"],
        missing_skills=analysis_result["missing_skills"],
        recommendations=analysis_result["recommendations"],
        category_breakdown=analysis_result["category_breakdown"]
    )
    db.add(analysis_record)
    db.commit()
    db.refresh(analysis_record)

    return _format_analysis_response(analysis_record)


@router.get("", response_model=List[AnalysisListItem])
def list_analyses(
    search: Optional[str] = Query(None, description="Search by job title or company"),
    sort_by: str = Query("date_desc", description="date_desc, date_asc, score_desc, score_asc"),
    min_score: Optional[float] = Query(None, ge=0.0, le=100.0),
    max_score: Optional[float] = Query(None, ge=0.0, le=100.0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns user analysis history with search, score filtering, and sorting options.
    """
    query = db.query(Analysis).join(JobDescription).filter(Analysis.user_id == current_user.id)

    # Search filter
    if search:
        search_term = f"%{search.strip().lower()}%"
        query = query.filter(
            (JobDescription.title.ilike(search_term)) |
            (JobDescription.company.ilike(search_term))
        )

    # Score bounds
    if min_score is not None:
        query = query.filter(Analysis.match_score >= min_score)
    if max_score is not None:
        query = query.filter(Analysis.match_score <= max_score)

    # Sorting
    if sort_by == "date_asc":
        query = query.order_by(Analysis.created_at.asc())
    elif sort_by == "score_desc":
        query = query.order_by(Analysis.match_score.desc())
    elif sort_by == "score_asc":
        query = query.order_by(Analysis.match_score.asc())
    else:  # default date_desc
        query = query.order_by(Analysis.created_at.desc())

    analyses = query.all()

    items = []
    for a in analyses:
        items.append(AnalysisListItem(
            id=a.id,
            job_title=a.job_description.title if a.job_description else "Untitled Role",
            company=a.job_description.company if a.job_description else "",
            match_score=a.match_score,
            match_tier=get_match_tier(a.match_score),
            matching_skills_count=len(a.matching_skills or []),
            missing_skills_count=len(a.missing_skills or []),
            created_at=a.created_at
        ))

    return items


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis_detail(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves complete results and breakdown for a single analysis.
    """
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis record not found.")

    return _format_analysis_response(analysis)


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deletes an analysis record.
    """
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis record not found.")

    db.delete(analysis)
    db.commit()
    return None
