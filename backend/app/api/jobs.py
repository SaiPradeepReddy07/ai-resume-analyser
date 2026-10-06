"""
Job Descriptions Router
Manages creation, retrieval, and deletion of target job descriptions.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.job_description import JobDescription
from app.schemas.job_description import JobDescriptionCreate, JobDescriptionResponse

router = APIRouter(prefix="/jobs", tags=["Job Descriptions"])


@router.post("", response_model=JobDescriptionResponse, status_code=status.HTTP_201_CREATED)
def create_job_description(
    job_in: JobDescriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Creates a new target job description record.
    """
    job_record = JobDescription(
        user_id=current_user.id,
        title=job_in.title.strip(),
        company=job_in.company.strip() if job_in.company else "",
        description=job_in.description.strip()
    )
    db.add(job_record)
    db.commit()
    db.refresh(job_record)
    return job_record


@router.get("", response_model=List[JobDescriptionResponse])
def list_job_descriptions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lists all job descriptions saved by the current user.
    """
    jobs = db.query(JobDescription).filter(
        JobDescription.user_id == current_user.id
    ).order_by(JobDescription.created_at.desc()).all()
    return jobs


@router.get("/{job_id}", response_model=JobDescriptionResponse)
def get_job_description(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves a specific job description by ID.
    """
    job = db.query(JobDescription).filter(
        JobDescription.id == job_id,
        JobDescription.user_id == current_user.id
    ).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found."
        )
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_description(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deletes a job description and cascades to related analyses.
    """
    job = db.query(JobDescription).filter(
        JobDescription.id == job_id,
        JobDescription.user_id == current_user.id
    ).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found."
        )
    db.delete(job)
    db.commit()
    return None
