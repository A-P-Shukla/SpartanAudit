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
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
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

def get_all_directories_recursive(repo_url: str, path: str = "", depth: int = 0, max_depth: int = 2, max_total_dirs: int = 20):
    """
    Recursively fetches ALL directories in a repository up to max_depth.
    Returns a list of directory paths (e.g., ['', 'backend/', 'backend/app/', 'frontend/src/']).
    LIMITED to prevent timeouts on large repos.
    """
    if depth > max_depth:
        return []
    
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip("/").split("/")
    if len(path_parts) < 2:
        return []
    owner, repo = path_parts[0], path_parts[1]
    
    dirs = [path] if path else [""]  # Include current path
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    
    try:
        res = requests.get(api_url, timeout=3)  # Strict 3-second timeout
        if res.status_code == 200:
            contents = res.json()
            for item in contents:
                if item.get("type") == "dir":
                    # Stop if we've already found too many directories
                    if len(dirs) >= max_total_dirs:
                        return dirs
                    
                    subdir_path = f"{item['path']}/"
                    dirs.append(subdir_path)
                    # Recursively get nested directories
                    nested = get_all_directories_recursive(repo_url, item['path'], depth + 1, max_depth, max_total_dirs)
                    dirs.extend(nested)
                    
                    # Check again after recursion
                    if len(dirs) >= max_total_dirs:
                        return dirs
    except:
        pass
    
    return list(set(dirs))  # Remove duplicates

def fetch_repo_metadata(repo_url: str):
    """
    Checks for key 'Proof of Engineering' files without cloning.
    Recursively scans ALL subdirectories up to 2 levels deep.
    Supports variant filenames (e.g., requirements_ml.txt, requirements_backend.txt).
    """
    # Expanded file patterns with common variants
    files_to_check = {
        "readme": ["README.md", "readme.md", "README.markdown", "README.rst", "README.txt"],
        "infra": [
            "Dockerfile", "dockerfile", 
            "docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml",
            ".github/workflows/main.yml", ".github/workflows/ci.yml", ".github/workflows/build.yml",
            ".github/workflows/test.yml", ".github/workflows/deploy.yml",
            "Makefile", "makefile",
            ".gitlab-ci.yml", "Jenkinsfile", "azure-pipelines.yml",
            "vercel.json", "netlify.toml", "render.yaml"
        ],
        "stack": [
            # Python variants
            "requirements.txt", "requirements-dev.txt", "requirements_dev.txt",
            "requirements-ml.txt", "requirements_ml.txt", "requirements-backend.txt", "requirements_backend.txt",
            "requirements-prod.txt", "requirements_prod.txt", "pyproject.toml", "setup.py", "Pipfile",
            # JS/TS
            "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
            # Other languages
            "go.mod", "go.sum", "Cargo.toml", "Cargo.lock",
            "pom.xml", "build.gradle", "build.gradle.kts",
            "Gemfile", "Gemfile.lock", "composer.json", "composer.lock"
        ],
        "tests": [
            "pytest.ini", "setup.cfg", "tox.ini", "jest.config.js", "jest.config.ts",
            "vitest.config.ts", ".eslintrc", ".eslintrc.js", ".prettierrc"
        ],
        "ml_artifacts": [
            # Jupyter Notebooks
            "*.ipynb", "notebook.ipynb", "analysis.ipynb", "exploration.ipynb",
            # Model files
            "*.h5", "*.pkl", "*.pickle", "*.pt", "*.pth", "*.onnx", "*.pb", "*.joblib",
            "model.h5", "best_model.pt", "final_model.pkl",
            # Dataset indicators (common filenames)
            "train.csv", "test.csv", "data.csv", "dataset.csv", "*.parquet",
            "train.json", "test.json", "data.json",
            # ML config files
            "config.yaml", "config.yml", "mlflow.yml", "dvc.yaml", "params.yaml"
        ]
    }
    
    # Recursively fetch ALL subdirectories (up to 3 levels deep)
    all_dirs = get_all_directories_recursive(repo_url)
    
    found_files = []
    readme_content = ""
    tech_stack = []
    ml_artifacts = []  # Track ML/DS specific files
    
    # Try 'main' then 'master' branches
    for branch in ["main", "master"]:
        current_found = []
        for dir_path in all_dirs:
            for category, filenames in files_to_check.items():
                for filename in filenames:
                    # Skip .github paths if we're not at root (they're always at root)
                    if filename.startswith(".github") and dir_path:
                        continue
                    
                    full_path = f"{dir_path}{filename}"
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
                            if category == "ml_artifacts":
                                ml_artifacts.append(full_path)
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
        "tech_stack": tech_stack,
        "ml_artifacts": ml_artifacts
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
    - ML/Data Science Artifacts: {ml_artifacts}
    - README Content: {readme_content}

    CRITICAL EVALUATION RULES:
    
    **For ML/Data Science Projects:**
    - Jupyter notebooks (.ipynb) are LEGITIMATE tools for exploration and analysis, NOT tutorial markers.
    - Presence of trained models (.h5, .pkl, .pt, .onnx) indicates ACTUAL work, not copy-paste.
    - Dataset files (train.csv, test.csv, *.parquet) show real data handling.
    - ML project structure is different from web apps; don't penalize for lack of Dockerfile if there are notebooks and models.
    - Score HIGHER if: custom models, data pipelines, experimentation notebooks, MLOps configs (mlflow, dvc).
    - Score LOWER if: only a single "hello world" notebook with no datasets or models.
    
    **For Web/Backend Projects:**
    - Dockerfiles, CI/CD workflows, and multi-tier architecture are strong indicators.
    - Multiple dependency files (frontend + backend) show real full-stack work.
    - Score HIGHER if: production configs, environment management, deployment manifests.
    - Score LOWER if: single README, no infra, or just boilerplate create-react-app.
    
    **General Red Flags (Tutorial Hell):**
    - README is 90% setup instructions with no actual code evidence.
    - Only package.json/requirements.txt with no actual source files detected.
    - Claims of "ML pipeline" but no notebooks, models, or datasets found.
    
    **General Green Flags (Production-Grade):**
    - Multiple proof points: tests + infra + dependencies.
    - Evidence of iteration: multiple model versions, data preprocessing scripts.
    - Real deployment artifacts: Docker, CI/CD, or cloud configs.

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
        "ml_artifacts": metadata.get("ml_artifacts", []),
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
    
    # --- CACHING: Check if we already audited this repo ---
    if not req.force_reaudit:
        existing_audit = crud.get_audit_by_url(db, repo_url=repo_url_str)
        if existing_audit:
            return existing_audit
    
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