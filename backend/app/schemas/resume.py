from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class ResumeBase(BaseModel):
    filename: str


class ResumeResponse(ResumeBase):
    id: int
    char_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ResumeUploadResponse(ResumeResponse):
    detected_skills: List[str]
