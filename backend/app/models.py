from sqlalchemy import Column, Integer, String, JSON, Text, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class Audit(Base):
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True, index=True)
    repo_url = Column(String, index=True, nullable=False)
    job_description = Column(Text)
    
    # Audit Results
    engineering_score = Column(Float)
    match_score = Column(Float)
    critique = Column(Text)
    verdict = Column(String) # "HIRE THIS SPARTAN", etc.
    
    # Metadata and Reconnaissance data
    found_files = Column(JSON) # List of files detected (README, Dockerfile, etc.)
    readme_content = Column(Text)
    tech_stack = Column(JSON) # Detected languages/frameworks
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())