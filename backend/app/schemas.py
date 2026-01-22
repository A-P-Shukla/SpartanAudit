from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any, Optional
from datetime import datetime

# --- Request Models ---
class AuditRequest(BaseModel):
    repo_url: HttpUrl
    job_description: Optional[str] = None
    force_reaudit: Optional[bool] = False # Bypass cache if True

# --- Response Models ---
class AuditResponse(BaseModel):
    id: int
    repo_url: str
    job_description: Optional[str] = None
    engineering_score: float
    match_score: Optional[float] = None
    critique: str
    verdict: str
    found_files: List[str]
    tech_stack: List[str]
    created_at: datetime

    class Config:
        from_attributes = True

# --- Internal Data Models ---
class AuditCreate(BaseModel):
    repo_url: str
    job_description: Optional[str] = None
    engineering_score: float
    match_score: Optional[float] = None
    critique: str
    verdict: str
    found_files: List[str]
    readme_content: Optional[str] = None
    tech_stack: List[str]