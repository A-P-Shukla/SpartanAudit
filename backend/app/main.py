import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from typing import List, Optional

from . import crud, models, schemas
from .database import engine, get_db
from .utils import fetch_repo_metadata
from .service import generate_audit_report

load_dotenv()
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SpartanAudit API",
    description="Automated Code Quality & Relevancy Screener.",
    version="1.0.0"
)

# Parse CORS origins from environment variable
origins_env = os.getenv("CORS_ORIGINS", "")
origins = [origin.strip() for origin in origins_env.split(",") if origin.strip()] if origins_env else ["*"]

# Ensure localhost is always allowed for local dev if not strictly overridden
if "http://localhost:3000" not in origins and "*" not in origins:
     origins.append("http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/", methods=["GET", "HEAD"])
async def health_check():
    return {"status": "ok", "message": "SpartanAudit backend is running"}

@app.post("/audit/", response_model=schemas.AuditResponse, status_code=201)
def run_audit(req: schemas.AuditRequest):
    repo_url_str = str(req.repo_url)
    
    # --- CACHING CHECK (Short Session) ---
    if not req.force_reaudit:
        db = next(get_db())
        try:
            existing_audit = crud.get_audit_by_url(db, repo_url=repo_url_str)
            if existing_audit:
                return existing_audit
        finally:
            db.close()
    
    # Metadata gathering (Reconnaissance) - NO DB CONNECTION HELD
    metadata = fetch_repo_metadata(repo_url_str)
    
    # AI Assessment - NO DB CONNECTION HELD (Can take 30+ seconds)
    llm_result = generate_audit_report(metadata, req.job_description)
    
    audit_data = schemas.AuditCreate(
        repo_url=repo_url_str,
        job_description=req.job_description,
        engineering_score=llm_result["engineering_score"],
        match_score=llm_result.get("match_score"),
        critique=llm_result["critique"],
        verdict=llm_result["verdict"],
        found_files=metadata["found_files"],
        readme_content=metadata["readme_content"],
        tech_stack=llm_result.get("tech_stack_inferred", metadata["tech_stack"])
    )
    
    # --- COMMIT TO DB (Fresh Session) ---
    db = next(get_db())
    try:
        return crud.create_audit(db=db, audit_data=audit_data)
    finally:
        db.close()

@app.get("/history/", response_model=List[schemas.AuditResponse])
def get_history(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.get_audits(db=db, skip=skip, limit=limit)

@app.get("/audit/{audit_id}", response_model=schemas.AuditResponse)
def get_audit(audit_id: int, db: Session = Depends(get_db)):
    db_audit = crud.get_audit(db, audit_id=audit_id)
    if not db_audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return db_audit