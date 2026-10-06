from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Analysis(Base):
    """
    SQLAlchemy Model representing the NLP match results between a resume and job description.
    Stores multi-metric scores (composite, skill, keyword, semantic), matching/missing skills,
    category distributions, and personalized recommendations.
    """
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False, index=True)

    # Multi-metric score breakdown (all normalized 0.0 to 100.0)
    match_score = Column(Float, nullable=False)
    skill_score = Column(Float, nullable=False, default=0.0)
    keyword_score = Column(Float, nullable=False, default=0.0)
    semantic_score = Column(Float, nullable=False, default=0.0)

    # Detailed structured results stored as JSON
    matching_skills = Column(JSON, nullable=False, default=list)
    missing_skills = Column(JSON, nullable=False, default=list)
    recommendations = Column(JSON, nullable=False, default=list)
    category_breakdown = Column(JSON, nullable=False, default=dict)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="analyses")
    resume = relationship("Resume", back_populates="analyses")
    job_description = relationship("JobDescription", back_populates="analyses")

    def __repr__(self):
        return f"<Analysis(id={self.id}, user_id={self.user_id}, match_score={self.match_score}%)>"
