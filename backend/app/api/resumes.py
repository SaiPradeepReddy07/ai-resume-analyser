"""
Resume Management Router
Handles PDF upload, text extraction, validation, and storage.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.schemas.resume import ResumeResponse, ResumeUploadResponse
from app.services.pdf_extractor import extract_text_from_pdf, PDFExtractionError
from app.services.skill_extractor import extract_skills

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/upload", response_model=ResumeUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Uploads a resume PDF file:
    - Validates file type, size, and magic bytes
    - Extracts clean text via PyMuPDF
    - Identifies recognized technical skills
    - Stores the record in the database
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only PDF documents (.pdf) are supported."
        )

    try:
        content = await file.read()
        extracted_text, page_count = extract_text_from_pdf(content, filename=file.filename)
    except PDFExtractionError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while reading the PDF file."
        )

    # Detect skills immediately for user feedback
    detected_skills = extract_skills(extracted_text)

    # Save to database
    resume_record = Resume(
        user_id=current_user.id,
        filename=file.filename,
        extracted_text=extracted_text
    )
    db.add(resume_record)
    db.commit()
    db.refresh(resume_record)

    return {
        "id": resume_record.id,
        "filename": resume_record.filename,
        "char_count": len(extracted_text),
        "detected_skills": detected_skills,
        "created_at": resume_record.created_at
    }


@router.get("", response_model=List[ResumeResponse])
def list_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lists all resumes uploaded by the current user.
    """
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "filename": r.filename,
            "char_count": len(r.extracted_text),
            "created_at": r.created_at
        }
        for r in resumes
    ]


@router.get("/{resume_id}", response_model=ResumeUploadResponse)
def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves a single resume by ID.
    """
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found."
        )

    detected_skills = extract_skills(resume.extracted_text)
    return {
        "id": resume.id,
        "filename": resume.filename,
        "char_count": len(resume.extracted_text),
        "detected_skills": detected_skills,
        "created_at": resume.created_at
    }


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deletes a resume and cascades to associated analyses.
    """
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found."
        )

    db.delete(resume)
    db.commit()
    return None
