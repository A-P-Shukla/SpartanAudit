import os
import json
import requests
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from typing import List, Optional
from urllib.parse import urlparse

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from . import crud, models, schemas
from .database import engine, get_db

load_dotenv()
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SpartanAudit API",
    description="Automated Code Quality & Relevancy Screener.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_github_raw_url(repo_url: str, file_path: str, branch: str = "main"):
    """Converts a GitHub repo URL into a raw content URL."""
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip("/").split("/")
    if len(path_parts) < 2:
        return None
    owner, repo = path_parts[0], path_parts[1]
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"

def fetch_repo_metadata(repo_url: str):
    """
    Checks for key 'Proof of Engineering' files without cloning.
    Scans root and common monorepo subdirectories.
    """
    files_to_check = {
        "readme": ["README.md", "readme.md", "README.markdown"],
        "infra": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml", ".github/workflows/main.yml", ".github/workflows/ci.yml"],
        "stack": ["package.json", "requirements.txt", "go.mod", "Cargo.toml", "pom.xml", "build.gradle", "Composer.json"]
    }
    
    # Common monorepo subdirectory prefixes
    subdir_prefixes = ["", "backend/", "frontend/", "server/", "client/", "api/", "app/", "src/"]
    
    found_files = []
    readme_content = ""
    tech_stack = []
    
    # Try 'main' then 'master' branches
    for branch in ["main", "master"]:
        current_found = []
        for prefix in subdir_prefixes:
            for category, filenames in files_to_check.items():
                for filename in filenames:
                    full_path = f"{prefix}{filename}"
                    raw_url = get_github_raw_url(repo_url, full_path, branch)
                    if not raw_url: continue
                    
                    try:
                        res = requests.get(raw_url, timeout=5)
                        if res.status_code == 200:
                            current_found.append(full_path)
                            # Prefer root README, but take subdir if not found
                            if category == "readme" and not readme_content:
                                readme_content = res.text[:5000]
                            if category == "stack":
                                tech_stack.append(full_path)
                    except:
                        pass
        
        if current_found:
            found_files = list(set(current_found))
            break
            
    if not readme_content and not found_files:
        raise HTTPException(status_code=404, detail="Repository not found or lacks a README. Spartans don't audit ghosts.")
        
    return {
        "found_files": found_files,
        "readme_content": readme_content,
        "tech_stack": tech_stack
    }

def generate_audit_report(metadata: dict, jd: Optional[str]):
    llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest", google_api_key=os.getenv("GEMINI_API_KEY"), temperature=0.7)
    
    prompt_template = """
    You are a Cynical Staff Engineer at a high-growth startup. Your job is to audit a candidate's GitHub repository.
    Be ruthless, efficient, and uncompromising. You see through "Tutorial Hell" projects.

    MISSION:
    1. Determine if this is "Production-Grade Engineering" or "Spaghetti Code/Tutorial".
    2. Provide a 0-10 Engineering Score.
    3. (Optional) If a Job Description is provided, calculate a 0-100% Relevancy Match.
    4. Provide a brutal one-paragraph critique.
    5. Assign a Verdict: "HIRE THIS SPARTAN" (High Quality+Match), "GOOD DEV, WRONG FIT" (High Quality, Low Match), or "TUTORIAL HELL" (Low Quality).

    DATA FOUND:
    - Files detected: {found_files}
    - Tech stack identified: {tech_stack}
    - README Content: {readme_content}

    {jd_section}

    RESPONSE FORMAT: Respond with ONLY raw JSON. No markdown prefix.
    {{
        "engineering_score": float,
        "match_score": float (null if no JD),
        "critique": "string (brutal paragraph)",
        "verdict": "string",
        "tech_stack_inferred": ["string"]
    }}
    """
    
    jd_section = f"JOB DESCRIPTION FOR RELEVANCY CHECK:\n{jd}" if jd else "No Job Description provided. Skip Relevancy Match."
    
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm | StrOutputParser()
    
    response_str = chain.invoke({
        "found_files": metadata["found_files"],
        "tech_stack": metadata["tech_stack"],
        "readme_content": metadata["readme_content"],
        "jd_section": jd_section
    })
    
    try:
        clean_json_str = response_str.strip().lstrip("```json").rstrip("```")
        return json.loads(clean_json_str)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="The AI brain glitched. Result: " + response_str)

@app.post("/audit/", response_model=schemas.AuditResponse, status_code=201)
def run_audit(req: schemas.AuditRequest, db: Session = Depends(get_db)):
    repo_url_str = str(req.repo_url)
    
    # Metadata gathering (Reconnaissance)
    metadata = fetch_repo_metadata(repo_url_str)
    
    # AI Assessment
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
    
    return crud.create_audit(db=db, audit_data=audit_data)

@app.get("/history/", response_model=List[schemas.AuditResponse])
def get_audit_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieves previous audits."""
    return crud.get_audits(db, skip=skip, limit=limit)