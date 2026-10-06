from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class JobDescriptionBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=200, description="Job title, e.g. Senior Backend Engineer")
    company: Optional[str] = Field(default="", max_length=200, description="Hiring company or organization")
    description: str = Field(..., min_length=10, description="Full job description text with requirements")


class JobDescriptionCreate(JobDescriptionBase):
    pass


class JobDescriptionResponse(JobDescriptionBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
